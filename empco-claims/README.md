# EmpCo Claims

Part of [EmpCo Skills](../README.md) — free agent skills from The Landbanking Group. See the repo root for the pitch and install options; this file covers how the skill is put together.

## What it does

Hand it anything with environmental or social claims in it and it returns a claims register screened against EU EmpCo — then, if you want, rewrites the flagged claims into safer alternatives.

| Input | How it's read | Setup |
| --- | --- | --- |
| Webpage URL | Firecrawl, one page per run | Free Firecrawl key |
| Pasted text or a single claim | Directly | None |
| PDF — report, brochure, packaging | Agent's file reader | None |
| Image — ad, social post, packaging photo | Agent looks at it, text and visuals | None |
| .docx, slides, video | Export to PDF, or transcript + screenshots | None |

## Layout

```
empco-claims/
  SKILL.md                     the router: identify input → read → assess → output → rewrite
  references/
    inputs.md                  how to read each input type
    empco-screening.md         the rubric: definitions, blacklisted practices, context-dependent issues
    rewrite.md                 how to rewrite flagged claims without inventing evidence
  assets/report-template.md    quick-check and full-register formats
  scripts/fetch_page.py        single-page Firecrawl fetch (webpage input only)
  tests/test_fetch_page.py     smoke tests, no network
```

The agent loads `SKILL.md` first and pulls in the reference files only when the task needs them.

## Design choices

- **One item per run.** One URL, one document, one ad. For several pages, run it once per page. A batch/crawl mode was tried and cut: it added rate-limit failures, keyword-prefilter recall gaps, and subagent overhead without improving accuracy.
- **The agent reads, no extractor script.** A regex or keyword filter can't tell a substantive claim from filler that shares its words. Reading one item directly is more reliable and fits comfortably in context.
- **Honest coverage.** Every report says what was actually reviewed — text only or visuals too, which pages — and never implies more.

See [SETUP.md](SETUP.md) for Firecrawl and tests.

## Disclaimer

Automated, first-pass risk screening — not legal advice, not legal clearance. See [LICENSE](../LICENSE).
