---
name: empco-claims
description: Screen environmental and social claims for greenwashing risk under the EU EmpCo framework (Empowering Consumers Directive 2024/825), and rewrite flagged claims into safer alternatives. Use for any green-claim or sustainability-claim check, whatever the format — a live webpage URL, pasted copy or a single claim, a PDF (report, brochure, packaging artwork), an ad or social post (image or text), or a draft before publication. Also use when the user mentions greenwashing, eco-claims, "carbon neutral", "sustainable", "eco-friendly", sustainability labels, or asks how to reword a claim so it holds up.
compatibility: No setup for text, PDF, or image input. Live webpage input needs a free Firecrawl API key (FIRECRAWL_API_KEY) or a Firecrawl MCP connection.
metadata:
  author: The Landbanking Group
  version: "1.0.0"
---

# EmpCo claims

Risk-screen environmental and social claims under the EU EmpCo framework, whatever form they arrive in, and help rewrite the ones that get flagged. This is risk screening, not legal advice or legal clearance — say so in every output.

## 1. Identify the input and confirm scope

Work out what the user has given you:

| Input | Examples | How to read it |
| --- | --- | --- |
| Webpage URL | product page, campaign page, landing page | `references/inputs.md` → Webpage |
| Text | a single claim, pasted copy, a draft, ad copy without visuals | read it directly — see `references/inputs.md` → Text |
| PDF | sustainability report, brochure, spec sheet, packaging artwork | `references/inputs.md` → PDF |
| Image | ad creative, social post, packaging photo, page screenshot | `references/inputs.md` → Image |
| Anything else | .docx, slide deck, video | `references/inputs.md` → Other formats |

Before doing anything that costs time or credits, confirm:

1. **The exact item.** One URL per run. For long PDFs, which pages or sections.
2. **The audience.** Default to EU consumers. EmpCo governs business-to-consumer communication; if the material looks investor- or B2B-facing, say so rather than assuming it's in scope.
3. **What they want.** Screening (the default), rewrites, or both.

If the user pastes a single claim and asks a direct question, skip the confirmation and answer.

## 2. Get the content

Follow the section of `references/inputs.md` for the input type. Keep track of what you actually reviewed — text only, or visuals too; which pages; any fetch failures — because it goes in the output.

## 3. Assess

Read `references/empco-screening.md` for the rubric. Then read the content yourself, in one pass. Do not write an extraction or keyword script: a heuristic can't tell a substantive claim from filler that happens to contain the same words, and reading one item directly is well within a normal context window.

**A. Relevant material.** Everything that describes or promotes the product, brand, or business — the full candidate set a claims reviewer would look at, not just what turns out to be a claim. Skip structural chrome: navigation, breadcrumbs, buttons, price lines, review-widget labels, size charts, icon-font strings. Keep titles, meta descriptions, headings, body copy, spec and material lines, badge and label text, small print, and promotional lines (note non-environmental ones like "Bestseller" as out of scope rather than dropping them silently). Keep customer reviews only if claim-adjacent, labeled as third-party content. For visual inputs, include claim-relevant visuals as well as text.

Quote text exactly, in its original language, with a translation if useful.

**B. Assessment** of every item that could plausibly be an environmental or social claim — explicit or implied benefit, characteristic, superiority, target, label, certification, or impact. For each:

- exact wording (or a precise description, for a visual);
- bucket: potential prohibited pattern, context-dependent issue, or insufficient information;
- risk category and priority (high/medium/low);
- factual reason, grounded in the exact text or visual;
- evidence or qualification visible nearby, or "none visible in the reviewed material";
- missing information — phrased as absence of evidence in what you reviewed, never as evidence of absence;
- recommended next action;
- confidence, and whether human review is required.

If nothing qualifies as a claim, say so plainly and show what you checked and ruled out (a colorway called "Forest Green", a material fact with no environmental benefit attached). A clean result is a valid result, not a reason to stretch for findings.

## Coverage

Screen explicit and implied claims, generic environmental language, product and business names, sustainability labels and badges, greenhouse-gas claims, future commitments, whole-product and whole-business scope, comparisons, durability and repairability, methodology links, and qualifications. For visual inputs, also screen implied claims from imagery — leaves, globes, green palettes, nature scenes paired with the product — since EmpCo looks at the overall presentation, not just the words.

For nature claims, distinguish habitat extent from biodiversity improvement, detected practices from regenerative status, measured change from causal attribution, mapped-land results from whole-product claims, and supplier evidence from SKU linkage.

## 4. Output

Use `assets/report-template.md`, choosing the form by size:

- **Quick check** — a single claim, or a short ad or post.
- **Full register** — a webpage, a PDF, or copy with several claims.

Always state what the input was, how it was read, any failures or retries, and what was not reviewed (imagery on a text-only fetch, pages outside the confirmed range, other locales). Don't imply full coverage.

## 5. Rewrite

If the user asked for rewrites — or after a screening that flagged anything, as an offer — follow `references/rewrite.md`.
