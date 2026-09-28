# EmpCo Skills

<img width="1600" height="900" alt="empco-skills-cover" src="https://github.com/user-attachments/assets/fa7d50d7-1f14-4468-bfaa-c14ac61150cd" />

Free [Agent Skills](https://agentskills.io) from The Landbanking Group for teams shipping product, marketing, and campaign copy under the EU's Empowering Consumers ("EmpCo") rules, which apply from **27 September 2026**. Find the risky environmental and social claims in a page, a PDF, or an ad — then turn them, or anything you'd like to say, into lower-risk directions with the evidence each one needs. Built for marketers, legal and compliance reviewers, and founders who want a fast first pass before copy ships, or before it goes to real legal review.

Works in Claude, ChatGPT, Gemini, Copilot, and coding agents like Claude Code, Codex, and Cursor — see [Installation](#installation).

**Why free:** this is a taste of the claims work TLG does at full depth — multi-page, tied to real evidence, sign-off-ready. Run it, see if it's useful, and if you need more than a first pass, see [Need more?](#need-more) below.

## Available skills

| Skill | What it does | Setup |
|---|---|---|
| [empco-screener](skills/empco-screener/) | Finds and risk-classifies the claims in existing material — a webpage, PDF, ad or social post, pasted copy — and returns a claims register. | None. For webpages, attach a PDF or screenshots, or add a free Firecrawl key in a coding agent |
| [empco-claim-writer](skills/empco-claim-writer/) | Turns a fact, an aspiration, or a flagged claim into two to four lower-risk directions, each with the evidence it needs, plus a data checklist for your teams. | None |

## Installation

**Easiest:** give your AI agent the repo link and ask it to install the skills.

```
Install the skills from https://github.com/nicolamaglio-tlg/empco-skills
```

Coding agents like Claude Code, Codex, and Cursor can do the rest. Their instructions are in [AGENTS.md](AGENTS.md). Using a chat app like Claude.ai or ChatGPT instead? Jump to [Option 7](#option-7-claudeai) or [Option 8](#option-8-any-other-chat-app).

### Option 1: CLI install (recommended)

Use [npx skills](https://github.com/vercel-labs/skills) to install skills directly:

```bash
# Install both skills
npx skills add nicolamaglio-tlg/empco-skills

# Install one skill
npx skills add nicolamaglio-tlg/empco-skills --skill empco-claim-writer

# List available skills
npx skills add nicolamaglio-tlg/empco-skills --list
```

The CLI detects which agents you have installed and asks where to install. For Claude Code it installs into `.claude/skills/`; universal agents share `.agents/skills/`.

> [!TIP]
> If you run the command from **inside** an agent session (e.g., asking Claude Code to install the skills for you), the CLI runs non-interactively and may only install to the universal `.agents/skills/` directory, which Claude Code does not read. Pass the agent explicitly:
>
> ```bash
> npx skills add nicolamaglio-tlg/empco-skills -a claude-code
> ```

### Option 2: Claude Code plugin

Install via Claude Code's built-in plugin system:

```bash
# Add the marketplace
/plugin marketplace add nicolamaglio-tlg/empco-skills

# Install both skills
/plugin install empco-skills
```

### Option 3: Clone and copy

Clone the repo and copy the skills folder:

```bash
git clone https://github.com/nicolamaglio-tlg/empco-skills.git
cp -r empco-skills/skills/* .agents/skills/
```

For Claude Code, copy into `.claude/skills/` instead (or `~/.claude/skills/` for all projects).

### Option 4: Git submodule

Add as a submodule for easy updates:

```bash
git submodule add https://github.com/nicolamaglio-tlg/empco-skills.git .agents/empco-skills
```

Then reference skills from `.agents/empco-skills/skills/`.

### Option 5: Fork and customize

1. Fork this repository
2. Customize the skills for your needs — for example, add your brand's evidence sources or house style to the claim writer
3. Clone your fork into your projects

### Option 6: SkillKit (multi-agent)

Use [SkillKit](https://github.com/rohitg00/skillkit) to install skills across multiple AI agents (Claude Code, Cursor, Copilot, etc.):

```bash
# Install both skills
npx skillkit install nicolamaglio-tlg/empco-skills

# Install one skill
npx skillkit install nicolamaglio-tlg/empco-skills --skill empco-claim-writer
```

### Option 7: Claude.ai

For claude.ai and the Claude desktop app:

1. Download both skills: **[empco-screener.zip](https://github.com/nicolamaglio-tlg/empco-skills/releases/latest/download/empco-screener.zip)** and **[empco-claim-writer.zip](https://github.com/nicolamaglio-tlg/empco-skills/releases/latest/download/empco-claim-writer.zip)**.
2. In Claude, go to **Customize → Skills** and upload each zip as it is — don't unzip it.

Use these links, not GitHub's green **Code → Download ZIP** button: that bundles both skills into one zip, which Claude rejects. If you don't see Skills, check that code execution is turned on in your Claude settings.

### Option 8: Any other chat app

For ChatGPT, Gemini, Copilot, and anything else that accepts a file:

1. Download **[empco-screener.md](https://github.com/nicolamaglio-tlg/empco-skills/releases/latest/download/empco-screener.md)** (checks existing material) or **[empco-claim-writer.md](https://github.com/nicolamaglio-tlg/empco-skills/releases/latest/download/empco-claim-writer.md)** (helps you write claims).
2. Attach it to a chat and ask: *"Follow the attached instructions. Is 'our packaging is 100% eco-friendly' OK under EmpCo?"*
3. Using it often? Add the files to a project, custom GPT, or Gem so they're always there.

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
