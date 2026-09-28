#!/usr/bin/env python3
"""Smoke tests for scripts/fetch_page.py. No network calls, no test framework required — the HTTP layer is mocked."""
from __future__ import annotations
import io
import json
import os
import sys
import urllib.error
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import fetch_page  # noqa: E402


class _FakeResponse(io.BytesIO):
    def __init__(self, body: bytes, ctype: str = "text/html; charset=utf-8"):
        super().__init__(body)
        from email.message import Message
        self.headers = Message()
        self.headers["Content-Type"] = ctype


PAGE = b"""<html><head><title>EcoRun &amp; Co</title>
<meta name="description" content="Our greenest shoe ever.">
<script>var tracking = "Made with recycled materials";</script><style>.x{}</style></head>
<body><nav>Home</nav><h1>EcoRun 2</h1><p>Made with <b>recycled</b> materials.</p>
<img src="a.png" alt="Certified Planet Friendly badge"><ul><li>100% carbon neutral</li></ul>
""" + b"<p>" + b"Filler copy. " * 60 + b"</p></body></html>"


def test_no_key_falls_back_to_plain_fetch():
    seen = {}

    def fake_urlopen(req, timeout=30):
        seen["url"], seen["ua"] = req.full_url, req.get_header("User-agent")
        return _FakeResponse(PAGE)

    with mock.patch.dict(os.environ, {}, clear=True), mock.patch.object(fetch_page, "_load_dotenv", lambda: None), \
         mock.patch.object(fetch_page.urllib.request, "urlopen", fake_urlopen):
        r = fetch_page.fetch("https://example.com/page")
    assert seen["url"] == "https://example.com/page" and "empco-screener" in seen["ua"]
    assert r["method"].startswith("plain HTTP")
    assert r["title"] == "EcoRun & Co" and r["description"] == "Our greenest shoe ever."
    assert "# EcoRun 2" in r["markdown"] and "Made with recycled materials." in r["markdown"]
    assert "[image: Certified Planet Friendly badge]" in r["markdown"] and "100% carbon neutral" in r["markdown"]
    assert "tracking" not in r["markdown"], "script contents must be dropped"
    assert len(r["warnings"]) == 1, "a normal page gets only the JavaScript caveat"


def test_thin_page_warns_about_javascript():
    shell = b"<html><head><title>App</title></head><body><div id='root'></div></body></html>"
    with mock.patch.dict(os.environ, {}, clear=True), mock.patch.object(fetch_page, "_load_dotenv", lambda: None), \
         mock.patch.object(fetch_page.urllib.request, "urlopen", lambda req, timeout=30: _FakeResponse(shell)):
        r = fetch_page.fetch("https://example.com/app")
    assert any("Very little text" in w for w in r["warnings"])
    assert "Warning: Very little text" in fetch_page.render(r)


def test_plain_fetch_blocked_says_not_to_bypass():
    def blocked(req, timeout=30):
        raise urllib.error.HTTPError(req.full_url, 403, "Forbidden", {}, io.BytesIO(b""))

    with mock.patch.dict(os.environ, {}, clear=True), mock.patch.object(fetch_page, "_load_dotenv", lambda: None), \
         mock.patch.object(fetch_page.urllib.request, "urlopen", blocked):
        try:
            fetch_page.fetch("https://example.com/page")
            raise AssertionError("expected RuntimeError")
        except RuntimeError as e:
            assert "Don't try to get around it" in str(e) and "PDF" in str(e)
            assert "web tool" not in str(e), "a block must not suggest trying another tool"


def test_check_without_key_is_ok(capsys=None):
    with mock.patch.dict(os.environ, {}, clear=True), mock.patch.object(fetch_page, "_load_dotenv", lambda: None), \
         mock.patch.object(sys, "argv", ["fetch_page.py", "--check"]):
        assert fetch_page.main() == 0


def test_invalid_url():
    with mock.patch.dict(os.environ, {}, clear=True), mock.patch.object(fetch_page, "_load_dotenv", lambda: None):
        try:
            fetch_page.fetch("not-a-url")
            raise AssertionError("expected ValueError")
        except ValueError:
            pass


def test_check_key_missing_key():
    with mock.patch.dict(os.environ, {}, clear=True), mock.patch.object(fetch_page, "_load_dotenv", lambda: None):
        try:
            fetch_page.check_key()
            raise AssertionError("expected RuntimeError")
        except RuntimeError as e:
            assert "FIRECRAWL_API_KEY" in str(e)


def test_check_key_valid():
    body = json.dumps({"data": {"remainingCredits": 987}}).encode()

    def fake_urlopen(req, timeout=30):
        return io.BytesIO(body)

    with mock.patch.dict(os.environ, {"FIRECRAWL_API_KEY": "test-key"}), \
         mock.patch.object(fetch_page.urllib.request, "urlopen", fake_urlopen):
        data = fetch_page.check_key()

    assert data["remainingCredits"] == 987


def test_retries_on_429_then_succeeds():
    calls = {"n": 0}
    success_body = json.dumps({"data": {"markdown": "# Hello", "metadata": {"title": "Hello"}}}).encode()

    def fake_urlopen(req, timeout=120):
        calls["n"] += 1
        if calls["n"] < 2:
            raise urllib.error.HTTPError(req.full_url, 429, "rate limited", {}, io.BytesIO(b"{}"))
        return io.BytesIO(success_body)

    with mock.patch.dict(os.environ, {"FIRECRAWL_API_KEY": "test-key"}), \
         mock.patch.object(fetch_page.time, "sleep", lambda *_: None), \
         mock.patch.object(fetch_page.urllib.request, "urlopen", fake_urlopen):
        result = fetch_page.fetch("https://example.com/page")

    assert calls["n"] == 2
    assert result["markdown"] == "# Hello"
    assert result["title"] == "Hello"


def test_render_includes_meta_description():
    body = json.dumps({"data": {"markdown": "# Body", "metadata": {"title": "T", "description": "We are shifting our business."}}}).encode()
    with mock.patch.dict(os.environ, {"FIRECRAWL_API_KEY": "test-key"}), \
         mock.patch.object(fetch_page.urllib.request, "urlopen", lambda req, timeout=120: io.BytesIO(body)):
        text = fetch_page.render(fetch_page.fetch("https://example.com/page"))
    assert "Meta description: We are shifting our business." in text
    assert "Page title: T" in text
    assert text.rstrip().endswith("# Body")


def test_dotenv_found_from_project_or_skill_folder():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        project, skill = Path(tmp, "project"), Path(tmp, "skill")
        project.mkdir(); skill.mkdir()
        with mock.patch.object(fetch_page.Path, "cwd", lambda: project), \
             mock.patch.object(fetch_page, "SKILL_DIR", skill):
            assert fetch_page._find_dotenv() is None
            (skill / ".env").write_text("FIRECRAWL_API_KEY=from-skill")
            assert fetch_page._find_dotenv() == skill / ".env"
            (project / ".env").write_text("FIRECRAWL_API_KEY=from-project")
            assert fetch_page._find_dotenv() == project / ".env"


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"ok: {name}")
    print("All smoke tests passed.")
