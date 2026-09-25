# EmpCo Skills

Free [Agent Skills](https://agentskills.io) from The Landbanking Group for teams shipping product, marketing, and campaign copy under the EU's Empowering Consumers ("EmpCo") rules, which apply from **27 September 2026**. Hand an agent a page, a PDF, an ad, or a single claim and get a risk-screened claims register back — plus safer rewrites of anything flagged. Built for marketers, legal and compliance reviewers, and founders who want a fast first pass before copy ships, or before it goes to real legal review.

Works with Claude Code, Claude.ai (Customize → Skills), and any other agent that reads the Agent Skills format.

**Why free:** this is a taste of the claims work TLG does at full depth — multi-page, tied to real evidence, sign-off-ready. Run it, see if it's useful, and if you need more than a first pass, see [Need more?](#need-more) below.

## Available skills

| Skill | Description |
|---|---|
| [empco-claims](empco-claims/) | Screen environmental and social claims for EmpCo greenwashing risk — from a webpage, pasted copy, a PDF, an ad or social post, or a single claim — and rewrite flagged claims into safer alternatives. |

## Quickstart

Install (below), then just ask. Text, PDFs, and images work immediately with no setup:

```
"Is 'our packaging is 100% eco-friendly' OK under EmpCo?"
```

To screen **live webpages**, add a free Firecrawl key (no credit card, 1,000 pages/month):

1. Get one at https://www.firecrawl.dev/app/api-keys
2. Set `FIRECRAWL_API_KEY=fc-...` in your environment or a gitignored `.env` file — never paste it into chat.
3. Check it (zero credits): `python3 empco-claims/scripts/fetch_page.py --check`

## Install

### Option 1: CLI install (recommended)

Using [npx skills](https://github.com/vercel-labs/skills):

```bash
npx skills add nicolamaglio-tlg/empco-skills
```

The CLI detects your agent and installs to the right place (`.claude/skills/` for Claude Code, `.agents/skills/` for universal agents).

### Option 2: Clone and copy

```bash
git clone https://github.com/nicolamaglio-tlg/empco-skills.git
cp -r empco-skills/empco-claims ~/.claude/skills/
```

### Option 3: Claude.ai

Zip the `empco-claims/` folder and upload it under **Customize → Skills**.

## Usage

One skill, whatever you've got:

```
"Audit https://example.com/product-page for EmpCo risk"
→ fetches the page once and returns a full claims register

"Check this ad before we run it"  [attach image]
→ reads the text and the visuals, including small print and
  implied claims from imagery

"Screen the consumer-facing claims in pages 4–9 of this report"  [attach PDF]
→ full register for those pages, and flags anything that's
  investor-facing rather than consumer-facing

"We say 'climate neutral shipping' — can we keep it? Suggest alternatives"
→ quick check, then two or three rewrites, each with the
  evidence it would need
```

Every result says what was actually reviewed (text only or visuals too, which pages) and never implies more.

## Scope and limits

- First-pass risk screening, not legal advice or legal clearance — see [LICENSE](LICENSE).
- One item per run: one page, one document, one ad. No crawling or batch mode.
- Video and audio need a transcript plus screenshots.
- Rewrites never invent figures or certifications — they leave placeholders for you to fill in.
- Webpages are fetched fairly: bot-protection blocks are reported, not routed around.

## Need more?

Want a full multi-page audit, ongoing monitoring, or an actual legal sign-off? Talk to The Landbanking Group — *[add your contact/landing-page link here before publishing]*.

## Support

Found a bug or have a suggestion? [Open an issue](https://github.com/nicolamaglio-tlg/empco-skills/issues).

## License

[MIT](LICENSE), with a screening-specific disclaimer — use this however you want, but read the disclaimer before you rely on its output.
