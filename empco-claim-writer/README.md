# EmpCo Claim Writer

Part of [EmpCo Skills](../README.md) — free agent skills from The Landbanking Group. See the repo root for the pitch and install options; this file covers how the skill is put together.

## What it does

Give it what you want to say — a fact, an aspiration, or a claim that got flagged — and it returns a claim brief: two to four lower-risk directions, from most conservative to most ambitious, each with the evidence it needs, plus a data checklist to take to your sustainability, product, and supply-chain teams.

No setup. Pairs with [empco-screener](../empco-screener/), which finds and flags claims in existing material.

## Layout

```
empco-claim-writer/
  SKILL.md                     starting point → what's off the table → directions → brief
  references/
    writing-guide.md           direction shapes, rules, evidence by claim type, nature claims
    empco-screening.md         the rubric (synced from shared/ — don't edit here)
  assets/brief-template.md     the claim brief format
```

## Design choices

- **Directions, not copy.** The output is a brief a marketer and a legal reviewer work from, never "compliant" wording.
- **Evidence first.** Every direction says what it needs to be substantiated; a direction nobody can back isn't safer.
- **No invented facts.** Figures, certifications, and methods the user hasn't supplied appear as placeholders.

## Disclaimer

Drafts for legal review — not legal advice, not cleared copy. See [LICENSE](../LICENSE).
