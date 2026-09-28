# EmpCo Screener

Part of [EmpCo Skills](../../README.md) — free agent skills from The Landbanking Group. See the repo root for the pitch and install options; this file covers how the skill is put together.

## What it does

Hand it existing material and it returns a claims register: every environmental or social claim it finds, risk-classified under EU EmpCo. To turn flagged claims into lower-risk directions, pair it with [empco-claim-writer](../empco-claim-writer/).

| Input | How it's read | Setup |
| --- | --- | --- |
| Webpage URL | Fetched by the agent, one page per run — Firecrawl if a key is set | None (Firecrawl key optional) |
| Pasted text or a single claim | Directly | None |
| PDF — report, brochure, packaging | Agent's file reader | None |
| Image — ad, social post, packaging photo | Agent looks at it, text and visuals | None |
| .docx, slides, video | Export to PDF, or transcript + screenshots | None |

## Layout

```
empco-screener/
  SKILL.md                     identify input → read → assess → output → hand off to the writer
  references/
    inputs.md                  how to read each input type
    empco-screening.md         the rubric (synced from shared/ — don't edit here)
  assets/report-template.md    quick-check and full-register formats
  scripts/fetch_page.py        single-page fetch: Firecrawl with a key, plain HTTP without
  tests/test_fetch_page.py     smoke tests, no network
```

The agent loads `SKILL.md` first and pulls in the reference files only when the task needs them.

## Design choices

- **One item per run.** One URL, one document, one ad. For several pages, run it once per page. A batch/crawl mode was tried and cut: it added rate-limit failures, keyword-prefilter recall gaps, and subagent overhead without improving accuracy.
- **The agent reads, no extractor script.** A regex or keyword filter can't tell a substantive claim from filler that shares its words. Reading one item directly is more reliable and fits comfortably in context.
- **Screens, doesn't rewrite.** Rewriting is a different job with a different user; it lives in empco-claim-writer.
- **Honest coverage.** Every report says what was actually reviewed — text only or visuals too, which pages — and never implies more.

See [SETUP.md](SETUP.md) for the optional Firecrawl key and tests.

## Disclaimer

Automated, first-pass risk screening — not legal advice, not legal clearance. See [LICENSE](../../LICENSE).
