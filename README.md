# EmpCo Skills

<img width="1600" height="900" alt="empco-skills-cover" src="https://github.com/user-attachments/assets/fa7d50d7-1f14-4468-bfaa-c14ac61150cd" />

Free [Agent Skills](https://agentskills.io) from The Landbanking Group for teams shipping product, marketing, and campaign copy under the EU's Empowering Consumers ("EmpCo") rules, which apply from **27 September 2026**. Find the risky environmental and social claims in a page, a PDF, or an ad — then turn them, or anything you'd like to say, into lower-risk directions with the evidence each one needs. Built for marketers, legal and compliance reviewers, and founders who want a fast first pass before copy ships, or before it goes to real legal review.

Works with Claude Code, Claude.ai (Customize → Skills), and any other agent that reads the Agent Skills format.

**Why free:** this is a taste of the claims work TLG does at full depth — multi-page, tied to real evidence, sign-off-ready. Run it, see if it's useful, and if you need more than a first pass, see [Need more?](#need-more) below.

## Available skills

| Skill | What it does | Setup |
|---|---|---|
| [empco-screener](empco-screener/) | Finds and risk-classifies the claims in existing material — a webpage, PDF, ad or social post, pasted copy — and returns a claims register. | None, except a free Firecrawl key for live webpages |
| [empco-claim-writer](empco-claim-writer/) | Turns a fact, an aspiration, or a flagged claim into two to four lower-risk directions, each with the evidence it needs, plus a data checklist for your teams. | None |

## How they work together

```
  page / PDF / ad / copy                 "we want to say…" / a fact
            │                                        │
            ▼                                        │
    ┌────────────────┐    flagged claims    ┌────────▼───────────┐
    │ empco-screener │ ───────────────────▶ │ empco-claim-writer │
    └───────┬────────┘                      └────────┬───────────┘
            ▼                                        ▼
     claims register                claim directions + evidence needed
   (risk, bucket, why,                  + data checklist for your
    missing evidence)                     sustainability team
```

Each skill works on its own. Both use the same EmpCo rubric.

## Quickstart

Install (below), then just ask. Everything works immediately except live webpages:

```
"Is 'our packaging is 100% eco-friendly' OK under EmpCo?"
```

To screen **live webpages**, add a free Firecrawl key (no credit card, 1,000 pages/month):

1. Get one at https://www.firecrawl.dev/app/api-keys
2. Set `FIRECRAWL_API_KEY=fc-...` in your environment or a gitignored `.env` file — never paste it into chat.
3. Check it (zero credits): `python3 empco-screener/scripts/fetch_page.py --check`

No key, or the page is bot-protected? Save it as a PDF or screenshot and screen that instead.

## Install

### Option 1: CLI install (recommended)

Using [npx skills](https://github.com/vercel-labs/skills):

```bash
npx skills add nicolamaglio-tlg/empco-skills
```

Or just one skill:

```bash
npx skills add nicolamaglio-tlg/empco-skills --skill empco-claim-writer
```

The CLI detects your agent and installs to the right place (`.claude/skills/` for Claude Code, `.agents/skills/` for universal agents).

### Option 2: Clone and copy

```bash
git clone https://github.com/nicolamaglio-tlg/empco-skills.git
cp -r empco-skills/empco-screener empco-skills/empco-claim-writer ~/.claude/skills/
```

### Option 3: Claude.ai

Zip each skill folder separately and upload it under **Customize → Skills**.

## Usage

**Screening existing material** — empco-screener:

```
"Audit https://example.com/product-page for EmpCo risk"
→ fetches the page once and returns a full claims register

"Check this ad before we run it"  [attach image]
→ reads the text and the visuals, including small print and
  implied claims from imagery

"Screen the consumer-facing claims in pages 4–9 of this report"  [attach PDF]
→ full register for those pages, and flags anything that's
  investor-facing rather than consumer-facing
```

**Writing claims** — empco-claim-writer:

```
"We switched to 70% recycled polyester. How can we talk about it?"
→ directions from conservative to ambitious, each with the
  evidence it needs

"We say 'climate neutral shipping' — what can we say instead?"
→ explains why offset-based neutrality is off the table, then
  directions built on what was actually reduced

"We fund restoration on 400 ha near our sourcing region. Can we say
 our range is nature positive?"
→ separates activity from outcome and landscape from product,
  and lists the data needed to go further
```

Every result says what was actually reviewed, and nothing is ever labeled "compliant".

## Scope and limits

- First-pass risk screening and drafting, not legal advice or legal clearance — see [LICENSE](LICENSE).
- The screener takes one item per run: one page, one document, one ad. No crawling or batch mode.
- Video and audio need a transcript plus screenshots.
- The writer never invents figures or certifications — it leaves placeholders for you to fill in.
- Webpages are fetched fairly: bot-protection blocks are reported, not routed around.

## Need more?

Want a full multi-page audit, measured evidence behind your nature claims, or an actual legal sign-off? Talk to The Landbanking Group — https://www.thelandbankinggroup.com/contact

## Contributing

Issues and pull requests welcome.

The EmpCo rubric lives once in [`shared/`](shared/) and is copied into each skill so every skill installs standalone. Edit the shared copy, then run:

```bash
python3 scripts/sync_shared.py
```

CI fails if a skill's copy has drifted from `shared/`.

## Support

Found a bug or have a suggestion? [Open an issue](https://github.com/nicolamaglio-tlg/empco-skills/issues).

## License

[MIT](LICENSE), with a screening-specific disclaimer — use this however you want, but read the disclaimer before you rely on its output.
