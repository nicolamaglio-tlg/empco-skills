#!/usr/bin/env python3
"""Fetch one webpage as text. Uses Firecrawl if FIRECRAWL_API_KEY is set, otherwise a plain HTTP fetch."""
from __future__ import annotations
import argparse, html, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request
from html.parser import HTMLParser
from pathlib import Path

API_URL = "https://api.firecrawl.dev/v2/scrape"
CREDIT_USAGE_URL = "https://api.firecrawl.dev/v2/team/credit-usage"
SKILL_DIR = Path(__file__).resolve().parents[1]
MISSING_KEY = (
    "FIRECRAWL_API_KEY is not set. It's optional: without it, pages are fetched over plain HTTP. "
    "For JavaScript-heavy or protected pages, get a free key (no credit card) at "
    "https://www.firecrawl.dev/app/api-keys and export it in your shell or add "
    "FIRECRAWL_API_KEY=fc-... to a .env file in your project folder (keep it gitignored)."
)
USER_AGENT = "empco-screener/1.2 (+https://github.com/nicolamaglio-tlg/empco-skills)"
THIN_PAGE_CHARS = 500
FALLBACK_HINT = "Use your own web tool if you have one, or ask the user for a PDF, screenshots, or the copy."


def _find_dotenv() -> Path | None:
    """Nearest .env in the working directory or its ancestors, else one in this skill's folder."""
    d = Path.cwd()
    for _ in range(8):
        if (d / ".env").exists():
            return d / ".env"
        if d.parent == d:
            break
        d = d.parent
    f = SKILL_DIR / ".env"
    return f if f.exists() else None


def _load_dotenv() -> None:
    """Load KEY=VALUE pairs from the .env found by _find_dotenv; never overrides an already-set env var."""
    f = _find_dotenv()
    if not f:
        return
    for line in f.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def check_key() -> dict:
    """Validate FIRECRAWL_API_KEY via the credit-usage endpoint. Costs zero credits."""
    _load_dotenv()
    key = os.getenv("FIRECRAWL_API_KEY")
    if not key:
        raise RuntimeError(MISSING_KEY)
    req = urllib.request.Request(
        CREDIT_USAGE_URL,
        headers={"Authorization": f"Bearer {key}", "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Key check failed (HTTP {e.code}): {e.read().decode(errors='replace')[:300]}") from e
    data = body.get("data", body)
    return data


def fetch(url: str, retries: int = 4) -> dict:
    p = urllib.parse.urlparse(url)
    if p.scheme not in {"http", "https"} or not p.netloc:
        raise ValueError(f"Invalid URL: {url}")
    _load_dotenv()
    key = os.getenv("FIRECRAWL_API_KEY")
    return firecrawl_fetch(url, key, retries) if key else plain_fetch(url)


def firecrawl_fetch(url: str, key: str, retries: int = 4) -> dict:
    payload = json.dumps({"url": url, "formats": ["markdown"], "onlyMainContent": True}).encode()
    req = urllib.request.Request(
        API_URL, data=payload,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    last_err = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                body = json.loads(r.read().decode())
            data = body.get("data", body)
            meta = data.get("metadata", {})
            return {
                "url": url,
                "method": "Firecrawl",
                "title": meta.get("title"),
                "description": meta.get("description") or meta.get("ogDescription"),
                "markdown": data.get("markdown", ""),
                "warnings": [],
            }
        except urllib.error.HTTPError as e:
            last_err = f"HTTP {e.code}: {e.read().decode(errors='replace')[:300]}"
            # 429 = rate limit, 5xx = Firecrawl-side proxy fault. Both are transient; back off and retry.
            if e.code == 429 or e.code >= 500:
                time.sleep(min(30, 2 ** attempt * 5))
                continue
            raise RuntimeError(last_err) from e
    raise RuntimeError(f"Gave up after {retries} attempts. Last error: {last_err}")


class _TextExtractor(HTMLParser):
    SKIP = {"script", "style", "noscript", "template", "svg", "iframe"}
    BLOCK = {"p", "div", "section", "article", "header", "footer", "main", "aside", "nav", "ul", "ol",
             "li", "tr", "td", "th", "dt", "dd", "blockquote", "figcaption", "br", "hr", "form", "button", "label"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lines: list[str] = []
        self.buf: list[str] = []
        self.skip_depth = 0
        self.in_title = False
        self.title = ""
        self.description = None
        self.heading = 0

    def _flush(self) -> None:
        text = re.sub(r"\s+", " ", "".join(self.buf)).strip()
        self.buf = []
        if text:
            self.lines.append(("#" * self.heading + " " if self.heading else "") + text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in self.SKIP:
            self.skip_depth += 1
        elif tag == "title" and not self.title:
            self.in_title = True
        elif tag == "meta" and self.description is None:
            if (a.get("name") or a.get("property") or "").lower() in {"description", "og:description"}:
                self.description = (a.get("content") or "").strip() or None
        elif tag == "img" and not self.skip_depth and (a.get("alt") or "").strip():
            self._flush()
            self.lines.append(f"[image: {a['alt'].strip()}]")
        elif re.fullmatch(r"h[1-6]", tag):
            self._flush()
            self.heading = int(tag[1])
        elif tag in self.BLOCK:
            self._flush()

    def handle_endtag(self, tag):
        if tag in self.SKIP:
            self.skip_depth = max(0, self.skip_depth - 1)
        elif tag == "title":
            self.in_title = False
        elif re.fullmatch(r"h[1-6]", tag):
            self._flush()
            self.heading = 0
        elif tag in self.BLOCK:
            self._flush()

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        elif not self.skip_depth:
            self.buf.append(data)


def html_to_text(page: str) -> dict:
    x = _TextExtractor()
    x.feed(page)
    x.close()
    x._flush()
    lines = [l for i, l in enumerate(x.lines) if i == 0 or l != x.lines[i - 1]]
    return {"title": html.unescape(x.title).strip() or None, "description": x.description, "text": "\n\n".join(lines)}


def plain_fetch(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            ctype = r.headers.get("Content-Type", "")
            charset = r.headers.get_content_charset() or "utf-8"
            raw = r.read()
    except urllib.error.HTTPError as e:
        if e.code in {401, 403, 429, 503}:
            raise RuntimeError(f"HTTP {e.code}: the site refused the fetch, probably bot protection. "
                               "Don't try to get around it with other tools or requests: ask the user for a PDF "
                               "of the page, screenshots, or the copy.") from e
        raise RuntimeError(f"HTTP {e.code} fetching the page.") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Couldn't reach the page ({e.reason}). {FALLBACK_HINT}") from e
    if "html" not in ctype.lower():
        raise RuntimeError(f"The URL returned {ctype or 'an unknown type'}, not a webpage. "
                           "If it's a PDF, download it and read it as a PDF.")
    page = html_to_text(raw.decode(charset, errors="replace"))
    warnings = ["Fetched over plain HTTP without Firecrawl: content that loads with JavaScript "
                "(carousels, tabs, reviews, some product details) may be missing."]
    if len(page["text"]) < THIN_PAGE_CHARS:
        warnings.append(f"Very little text came back ({len(page['text'])} chars): the page probably renders "
                        f"with JavaScript. Don't screen from this alone. {FALLBACK_HINT} "
                        "A Firecrawl key would also handle it.")
    return {"url": url, "method": "plain HTTP (no Firecrawl key)", "title": page["title"],
            "description": page["description"], "markdown": page["text"], "warnings": warnings}


def render(result: dict) -> str:
    """Page metadata first — the meta description often carries claims but isn't in the Markdown body."""
    header = [f"URL: {result['url']}", f"Fetched with: {result.get('method', 'Firecrawl')}"]
    if result.get("title"):
        header.append(f"Page title: {result['title']}")
    if result.get("description"):
        header.append(f"Meta description: {result['description']}")
    header += [f"Warning: {w}" for w in result.get("warnings", [])]
    return "\n".join(header) + "\n\n---\n\n" + result["markdown"]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("url", nargs="?", help="Single page URL to fetch.")
    ap.add_argument("--output", help="Write Markdown to this file instead of stdout.")
    ap.add_argument("--check", action="store_true", help="Check the optional FIRECRAWL_API_KEY and exit (costs zero credits).")
    args = ap.parse_args()

    if args.check:
        _load_dotenv()
        if not os.getenv("FIRECRAWL_API_KEY"):
            print("No Firecrawl key set. That's fine: pages will be fetched over plain HTTP. "
                  "A free key (https://www.firecrawl.dev/app/api-keys) handles JavaScript-heavy and protected pages better.")
            return 0
        try:
            data = check_key()
        except Exception as exc:
            print(f"Key check failed: {exc}", file=sys.stderr)
            return 1
        remaining = data.get("remainingCredits", data.get("remaining_credits", "unknown"))
        print(f"Firecrawl key is valid. Remaining credits this period: {remaining}")
        return 0

    if not args.url:
        ap.error("url is required unless --check is given")

    try:
        result = fetch(args.url)
    except Exception as exc:
        print(f"Fetch failed: {exc}", file=sys.stderr)
        return 1
    text = render(result)
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
        print(f"Saved {len(text)} chars to {args.output} via {result['method']} (title: {result['title']!r})", file=sys.stderr)
        for w in result.get("warnings", []):
            print(f"Warning: {w}", file=sys.stderr)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
