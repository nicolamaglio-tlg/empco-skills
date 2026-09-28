# Reading each input type

## Webpage

One URL per run. If the user wants several pages, run once per page — there is deliberately no crawl or batch mode. It was cut because it added failure modes (rate limits, keyword-prefilter recall gaps, subagent overhead) without improving accuracy or speed at this scale.

Get the page's text the first way that works, in this order, and say in the report which one you used.

1. **The fetch script**, if you can run commands. Run it from the user's working directory, calling it by its path inside this skill's folder (below, `<skill>`), so a `.env` in their project is found:

   ```bash
   python3 <skill>/scripts/fetch_page.py "https://example.com/page" --output page.md
   ```

   No setup is needed. It uses Firecrawl if a `FIRECRAWL_API_KEY` is set and otherwise fetches the page over plain HTTP. Either way it writes `page.md`: a header with the URL, how it was fetched, the page title, the meta description, and any warnings, then the page text. The meta description is copy that search results and social previews show — screen it like any other text.

   - **Read the warnings.** A plain fetch can miss content that loads with JavaScript (carousels, tabs, reviews). If the header says very little text came back, don't screen from it; go to option 2.
   - **Errors.** With Firecrawl, rate limits and Firecrawl-side errors are retried automatically. Any other error: stop and report it, don't retry.

2. **Your own web tool**, if you can't run the script or it came back thin, and you have a tool that reads webpages (a web fetch or browsing tool, or a Firecrawl MCP connection). Ask it for the page's full text, verbatim. Some web tools return a summary rather than the page. You can't quote exact wording from a summary, so if that's all you get, say so and treat the wording as unverified, or go to option 3.

3. **Ask the user** for a PDF of the page (in a browser: Print → Save as PDF), screenshots, or the copy pasted in, and continue with that input type. Screenshots have a bonus: they let you review the imagery too.

**Bot protection.** A 403, or a "security issue identified"/bot-detection page instead of real content, means the site blocked the fetch — this can happen even to the site's owner. Don't try to get past it: no other tools, disguised requests, or workarounds. Report it and go straight to option 3. If the user owns the site, the lasting fix is allowlisting the crawler in their WAF.

**Firecrawl is optional.** It handles JavaScript-heavy and protected pages better than a plain fetch. When a page needs it, you can tell the user a free key (no credit card, 1,000 pages/month) is at https://www.firecrawl.dev/app/api-keys, set as `FIRECRAWL_API_KEY` in their environment or a gitignored `.env` in their project folder. Never ask them to paste the key into chat. To confirm a key works, at no cost:

```bash
python3 <skill>/scripts/fetch_page.py --check
```

**What a fetch covers.** Any fetch captures text and image alt text, not the images themselves. Say that imagery wasn't reviewed unless the user also provides screenshots.

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
