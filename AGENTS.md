# AGENTS.md

Guidance for AI agents. If a user gave you this repository's link and asked you to install it, start with the first section.

## Installing these skills for a user

This repo contains two [Agent Skills](https://agentskills.io): `empco-screener` and `empco-claim-writer`. Install both unless the user asks for one.

**If you can run shell commands** (Claude Code, Codex, Cursor, and other coding agents):

```bash
npx skills add nicolamaglio-tlg/empco-skills -a <your-agent> -y
```

- Replace `<your-agent>` with your own agent id, e.g. `claude-code`, `codex`, `cursor`. Always pass `-a`: run from inside an agent session without it, the CLI may install only to `.agents/skills/`, which some agents (including Claude Code) don't read.
- This installs into the current project. Add `-g` if the user wants the skills in all their projects.
- No Node.js? Clone and copy instead:
  ```bash
  git clone --depth 1 https://github.com/nicolamaglio-tlg/empco-skills.git /tmp/empco-skills
  cp -r /tmp/empco-skills/skills/* <your agent's skills directory>
  ```
  For Claude Code that's `.claude/skills/` in the project, or `~/.claude/skills/` for all projects.

**If the user prefers the Claude Code plugin:** slash commands have to be typed by the user, so tell them to run `/plugin marketplace add nicolamaglio-tlg/empco-skills`, then `/plugin install empco-skills`.

**If you can't run commands** (a chat app such as Claude.ai or ChatGPT): don't attempt an install. Point the user to Options 7 and 8 in the README's Installation section, which are one-click downloads.

**After installing:**

1. Check that both skill folders exist where you installed them. If the skills don't show up in your session, tell the user to start a new one.
2. Suggest a first prompt: *"Is 'our packaging is 100% eco-friendly' OK under EmpCo?"*
3. Mention that everything works without setup except fetching live webpages. For that, the user can attach a PDF or screenshots of the page, or add a free Firecrawl key (https://www.firecrawl.dev/app/api-keys) as `FIRECRAWL_API_KEY` in their environment or a gitignored `.env`. Never ask the user to paste the key into chat.

## Repository structure

```
empco-skills/
├── .claude-plugin/        Claude Code plugin marketplace + plugin manifest
├── skills/
│   ├── empco-screener/    finds and risk-classifies claims in existing material
│   └── empco-claim-writer/ turns a claim idea into lower-risk directions + evidence
├── shared/                the EmpCo rubric, copied into each skill
├── scripts/
│   ├── sync_shared.py     copies shared/ into the skills; --check for CI
│   └── build_dist.py      builds the release downloads into dist/
└── .github/workflows/     CI checks, and releases on version tags
```

## Working on the skills

- **Skills are content.** Each is a folder with a `SKILL.md` whose frontmatter `name` matches the folder (lowercase, hyphens, max 64 characters) and whose `description` is 1–1024 characters. `scripts/build_dist.py` checks both.
- **The rubric lives in `shared/`.** Edit it there, then run `python3 scripts/sync_shared.py`. Never edit the copies in `skills/*/references/empco-screening.md`; CI fails if they drift.
- **Tests:** `python3 skills/empco-screener/tests/test_fetch_page.py` (no network).
- **Releases:** bump `version` in `.claude-plugin/*.json`, then push a tag like `v1.2.0`. The release workflow builds the per-skill zips and single-file versions and attaches them to a GitHub release.
- **Tone of outputs:** first-pass screening, never legal advice. Neither skill ever calls a claim "compliant".
