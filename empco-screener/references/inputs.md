# Reading each input type

## Webpage

One URL per run. If the user wants several pages, run once per page — there is deliberately no crawl or batch mode. It was cut because it added failure modes (rate limits, keyword-prefilter recall gaps, subagent overhead) without improving accuracy or speed at this scale.

**Credentials.** Fetching uses Firecrawl via `FIRECRAWL_API_KEY`, set as an environment variable or in a private `.env` file in the working directory. Never ask the user to paste the key into chat. If it isn't set, tell them they can get a free key (no credit card, 1,000 credits/month) at https://www.firecrawl.dev/app/api-keys, and offer the alternatives below in the meantime. To confirm a key works without spending credits:

```bash
python3 scripts/fetch_page.py --check
```

If a Firecrawl MCP connection is available instead, use its scrape tool for the single URL (Markdown, main content only).

**Fetch.**

```bash
python3 scripts/fetch_page.py "https://example.com/page" --output page.md
```

This makes exactly one Firecrawl request and writes the page to `page.md`: a short header with the URL, page title, and meta description, then the page's Markdown. The meta description is page copy search results and social previews show — screen it like any other text. It retries automatically on rate limits (429) and Firecrawl-side errors (5xx), which are transient. Any other error: stop and report it, don't retry.

**Bot protection.** A 403, or a "security issue identified"/bot-detection page instead of real content, means the site's WAF (Akamai Bot Manager, Cloudflare Bot Fight Mode, etc.) blocked the fetch — this can happen even to the site's owner. Report it. Do not try to route around it. The fix on the owner's side is allowlisting Firecrawl; the fix right now is the alternatives below.

**Alternatives when the page can't be fetched** — no key, a block, or an environment where the script can't run or reach the network: ask the user to save the page as a PDF, upload screenshots, or paste the copy, and continue with that input type. Screenshots have a bonus: they let you review the imagery too.

**What a fetch covers.** Markdown captures text and image alt text, not the images themselves. Say that imagery wasn't reviewed unless the user also provides screenshots.

**Fetch artifacts.**

- *Repeated blocks.* Carousels and sliders often come through as the same block several times, word for word. Treat it as one item and note the duplication once in Limitations.
- *Footnotes and tooltips.* Markers like `*` or `+` whose text never appears usually point to content shown on hover or click, which a fetch can't capture. Don't assume the footnote says nothing: record it as missing information on the claim it qualifies, and suggest the user screenshot it if the claim is medium or high priority.
- *Unrelated fragments* (blocked-tracker messages, cookie banners): ignore them and note them in Limitations.

## Text

A single claim, pasted copy, a draft, or ad copy without its visuals. Read it directly.

A claim on its own lacks its context: a qualification nearby, the placement, the product it sits next to, or substantiation linked from the same page can all change the assessment. Say so, and note what context would change the result.

## PDF

Read it with your file-reading tool — most agents read PDFs natively, often including the page images. If yours can't, try `pdftotext -layout file.pdf out.txt` if it's installed; otherwise ask the user for the text.

For long documents (more than ~20 pages), confirm which pages or sections to cover before starting.

Mind the audience. A sustainability or CSRD report written for investors and regulators is largely outside EmpCo, which governs communication with consumers — but any of its claims that are reused in consumer marketing, on packaging, or on product pages are in scope. Flag the question rather than assume either way.

If you can see the page images, include charts, logos, badges, and imagery in the review, and record that you did.

## Image

Ad creative, social posts, packaging photos, page screenshots. Look at the image itself.

1. Transcribe every piece of text exactly: headline, body, CTA, small print, disclaimers, label and badge text.
2. Describe the claim-relevant visuals: nature imagery, green palettes, globes and leaves, certification-style marks, before/after comparisons.
3. Note prominence. A qualification in small print that's hard to read, or placed away from the claim it qualifies, may not travel with the claim in the way EmpCo expects.

If the user gives only the ad copy, treat it as text and say that the visuals weren't reviewed.

## Other formats

- **.docx, slide decks:** read with whatever tools are available, or ask the user to export a PDF.
- **Video or audio:** can't be reviewed directly. Ask for a transcript plus screenshots of key frames (especially any on-screen text, end cards, and badges), then treat them as text and images.
