#!/usr/bin/env python3
"""Fetch one URL's Markdown via Firecrawl. Single page in, Markdown out — nothing else."""
from __future__ import annotations
import argparse, json, os, sys, time, urllib.error, urllib.parse, urllib.request
from pathlib import Path

API_URL = "https://api.firecrawl.dev/v2/scrape"
CREDIT_USAGE_URL = "https://api.firecrawl.dev/v2/team/credit-usage"


def _load_dotenv() -> None:
    """Load KEY=VALUE pairs from the nearest .env (cwd or an ancestor); never overrides an already-set env var."""
    d = Path.cwd()
    for _ in range(8):
        f = d / ".env"
        if f.exists():
            for line in f.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
            return
        if d.parent == d:
            break
        d = d.parent


def check_key() -> dict:
    """Validate FIRECRAWL_API_KEY via the credit-usage endpoint. Costs zero credits."""
    _load_dotenv()
    key = os.getenv("FIRECRAWL_API_KEY")
    if not key:
        raise RuntimeError(
            "FIRECRAWL_API_KEY is not set. Get a free key (no credit card) at "
            "https://www.firecrawl.dev/app/api-keys, then put it in a .env file here: "
            'FIRECRAWL_API_KEY=fc-...'
        )
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
    _load_dotenv()
    key = os.getenv("FIRECRAWL_API_KEY")
    if not key:
        raise RuntimeError(
            "FIRECRAWL_API_KEY is not set. Get a free key (no credit card) at "
            "https://www.firecrawl.dev/app/api-keys, then put it in a .env file here: "
            'FIRECRAWL_API_KEY=fc-...'
        )
    p = urllib.parse.urlparse(url)
    if p.scheme not in {"http", "https"} or not p.netloc:
        raise ValueError(f"Invalid URL: {url}")

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
                "title": meta.get("title"),
                "description": meta.get("description") or meta.get("ogDescription"),
                "markdown": data.get("markdown", ""),
            }
        except urllib.error.HTTPError as e:
            last_err = f"HTTP {e.code}: {e.read().decode(errors='replace')[:300]}"
            # 429 = rate limit, 5xx = Firecrawl-side proxy fault. Both are transient; back off and retry.
            if e.code == 429 or e.code >= 500:
                time.sleep(min(30, 2 ** attempt * 5))
                continue
            raise RuntimeError(last_err) from e
    raise RuntimeError(f"Gave up after {retries} attempts. Last error: {last_err}")


def render(result: dict) -> str:
    """Page metadata first — the meta description often carries claims but isn't in the Markdown body."""
    header = [f"URL: {result['url']}"]
    if result.get("title"):
        header.append(f"Page title: {result['title']}")
    if result.get("description"):
        header.append(f"Meta description: {result['description']}")
    return "\n".join(header) + "\n\n---\n\n" + result["markdown"]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("url", nargs="?", help="Single page URL to fetch.")
    ap.add_argument("--output", help="Write Markdown to this file instead of stdout.")
    ap.add_argument("--check", action="store_true", help="Validate FIRECRAWL_API_KEY and exit (costs zero credits).")
    args = ap.parse_args()

    if args.check:
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
        print(f"Saved {len(text)} chars to {args.output} (title: {result['title']!r})", file=sys.stderr)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
