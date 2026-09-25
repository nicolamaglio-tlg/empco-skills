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


def test_missing_api_key():
    with mock.patch.dict(os.environ, {}, clear=True), mock.patch.object(fetch_page, "_load_dotenv", lambda: None):
        try:
            fetch_page.fetch("https://example.com/page")
            raise AssertionError("expected RuntimeError")
        except RuntimeError as e:
            assert "FIRECRAWL_API_KEY" in str(e)


def test_invalid_url():
    with mock.patch.dict(os.environ, {"FIRECRAWL_API_KEY": "test-key"}):
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


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"ok: {name}")
    print("All smoke tests passed.")
