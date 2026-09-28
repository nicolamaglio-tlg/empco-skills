# EmpCo Skills

<img width="1600" height="900" alt="empco-skills-cover" src="https://github.com/user-attachments/assets/fa7d50d7-1f14-4468-bfaa-c14ac61150cd" />

Free [Agent Skills](https://agentskills.io) from The Landbanking Group for teams shipping product, marketing, and campaign copy under the EU's Empowering Consumers ("EmpCo") rules, which apply from **27 September 2026**. Find the risky environmental and social claims in a page, a PDF, or an ad — then turn them, or anything you'd like to say, into lower-risk directions with the evidence each one needs. Built for marketers, legal and compliance reviewers, and founders who want a fast first pass before copy ships, or before it goes to real legal review.

Works in Claude, ChatGPT, Gemini, Copilot, and coding agents like Claude Code, Codex, and Cursor — see [Get started](#get-started).

**Why free:** this is a taste of the claims work TLG does at full depth — multi-page, tied to real evidence, sign-off-ready. Run it, see if it's useful, and if you need more than a first pass, see [Need more?](#need-more) below.

## Available skills

| Skill | What it does | Setup |
|---|---|---|
| [empco-screener](empco-screener/) | Finds and risk-classifies the claims in existing material — a webpage, PDF, ad or social post, pasted copy — and returns a claims register. | None. For webpages, attach a PDF or screenshots, or add a free Firecrawl key in a coding agent |
| [empco-claim-writer](empco-claim-writer/) | Turns a fact, an aspiration, or a flagged claim into two to four lower-risk directions, each with the evidence it needs, plus a data checklist for your teams. | None |

## Get started

Pick where you use AI. Each option takes about a minute, and none needs an account beyond the one you already have.

| You use | Do this |
|---|---|
| **Claude** (claude.ai or the desktop app) | [Upload two zips](#claude) |
| **ChatGPT, Gemini, Copilot, or any other chat app** | [Attach an instruction file](#any-other-chat-app) |
| **Claude Code, Codex, Cursor, or another coding agent** | [Run one command](#coding-agents) |

### Claude

1. Download both skills: **[empco-screener.zip](https://github.com/nicolamaglio-tlg/empco-skills/releases/latest/download/empco-screener.zip)** and **[empco-claim-writer.zip](https://github.com/nicolamaglio-tlg/empco-skills/releases/latest/download/empco-claim-writer.zip)**.
2. In Claude, go to **Customize → Skills** and upload each zip as it is — don't unzip it.
3. Ask: *"Is 'our packaging is 100% eco-friendly' OK under EmpCo?"*

Use the links above, not GitHub's green **Code → Download ZIP** button: that bundles both skills into one zip, which Claude rejects. If you don't see Skills, check that code execution is turned on in your Claude settings.

### Any other chat app

1. Download the instruction files: **[empco-screener.md](https://github.com/nicolamaglio-tlg/empco-skills/releases/latest/download/empco-screener.md)** (checks existing material) and **[empco-claim-writer.md](https://github.com/nicolamaglio-tlg/empco-skills/releases/latest/download/empco-claim-writer.md)** (helps you write claims).
2. Start a chat, attach the file you need, and ask: *"Follow the attached instructions. Is 'our packaging is 100% eco-friendly' OK under EmpCo?"*
3. Using it often? Add the files to a project, custom GPT, or Gem so they're always there.

### Coding agents

Using [npx skills](https://github.com/vercel-labs/skills):

```bash
npx skills add nicolamaglio-tlg/empco-skills
```

It detects your agent and installs both skills in the right place. For one skill only, add `--skill empco-claim-writer`. Or copy them by hand:

```bash
git clone https://github.com/nicolamaglio-tlg/empco-skills.git
cp -r empco-skills/empco-screener empco-skills/empco-claim-writer ~/.claude/skills/
```

## Screening live webpages

Everything above works with no extra setup. For a webpage, the simplest route works anywhere:

- **Save the page as a PDF** (in your browser: Print → Save as PDF) or **take screenshots**, and attach them. Screenshots also let the screener check the imagery.

In a coding agent, the screener can also fetch a URL itself with a free [Firecrawl](https://www.firecrawl.dev/app/api-keys) key (no credit card, 1,000 pages/month):

1. Get a key at https://www.firecrawl.dev/app/api-keys
2. Add `FIRECRAWL_API_KEY=fc-...` to your shell environment or a gitignored `.env` in your project folder. Never paste it into chat.
3. Check it from your project folder (costs nothing): `python3 path/to/empco-screener/scripts/fetch_page.py --check`

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

To publish new downloads, push a version tag (`git tag v1.1.0 && git push --tags`). A workflow builds the per-skill zips and single-file versions (`scripts/build_dist.py`) and attaches them to a GitHub release, so the download links above always point to the latest.

## Support

Found a bug or have a suggestion? [Open an issue](https://github.com/nicolamaglio-tlg/empco-skills/issues).

## License

[MIT](LICENSE), with a screening-specific disclaimer — use this however you want, but read the disclaimer before you rely on its output.
