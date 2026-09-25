# Setup

**Text, PDF, and image input need no setup.** Paste a claim, upload a PDF or an ad, and go.

Only **live webpage** input needs Firecrawl.

## Firecrawl (webpages only)

1. Get a free API key at https://www.firecrawl.dev/app/api-keys — no credit card, 1,000 credits/month on the free plan. Each page fetched uses one credit.
2. Store it privately as `FIRECRAWL_API_KEY`: export it in your shell profile, or put it in a `.env` file in the directory you run your agent from (and make sure `.env` is gitignored):
   ```
   FIRECRAWL_API_KEY=fc-...
   ```
   Or connect Firecrawl through MCP instead. Never paste the key into chat.
3. Confirm it works (costs zero credits):
   ```bash
   python3 scripts/fetch_page.py --check
   ```

## What gets sent where

Webpage fetches send the URL to Firecrawl, which retrieves the public page. Don't fetch confidential or authenticated pages. Files and text you give the agent are handled by your agent as usual; this skill sends them nowhere else.

## Tests

```bash
python3 tests/test_fetch_page.py
```

No network calls; the HTTP layer is mocked.
