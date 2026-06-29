---
name: linkedin-viral
description: Analyze your own past LinkedIn posts to find what drives engagement, then draft new posts that reuse those winning patterns. Use when the user wants to analyze LinkedIn performance, extract viral/content patterns from their posts, turn a high-performing post into a reusable recipe, or draft a new LinkedIn post in their proven style.
license: MIT
---

# LinkedIn Viral Content Engine

Turn your own LinkedIn history into a repeatable content system: **extract → analyze → patternize → draft**. Based on the `linked-auto` workflow.

The value is *strategic*, not speed: this does not write posts faster, it makes them land more reliably by grounding each draft in what already worked for *this specific account*.

## When to use
- "Analyze my LinkedIn posts" / "왜 이 글이 잘 됐는지 분석해줘"
- "Find the patterns in my best posts"
- "Turn this viral post into a reusable recipe"
- "Draft a LinkedIn post like my best ones"

## Inputs
- A CSV/Excel export of the user's posts (text + engagement metrics: reactions, comments, reposts, impressions if available).
  - If the user has no export: tell them to run the **Apify "LinkedIn Profile Posts"** actor on their profile URL (~1,000 posts ≈ a few dollars) and download CSV. Do not scrape LinkedIn directly.
- For drafting: a topic/angle the user wants to post about.

## Workflow

### Step 1 — Analyze performance
1. Load the export. Identify the metric columns and compute an engagement proxy (e.g. `reactions + 2*comments + 3*reposts`, normalized by impressions when present).
2. Rank posts; take the top ~15% and bottom ~15%.
3. Run the structured analysis in `references/analysis-prompt.md` to produce a report covering: hook types, post length, formatting (line breaks/lists/emoji), angle (story / contrarian / how-to / data / vulnerability), CTA style, topic, and posting cadence.
4. Output a short, ranked list of **what correlates with high engagement for THIS account** — not generic LinkedIn advice.

### Step 2 — Patternize (make it reusable)
For each winning pattern worth keeping, fill `references/recipe-template.md` to capture it as a concrete, re-runnable recipe (hook formula, structure, do/don't, example). Save one file per recipe under the user's project (e.g. `recipes/`).

### Step 3 — Draft
When asked to write a new post:
1. Pick the recipe(s) matching the user's topic/goal.
2. Draft 2–3 variants, each explicitly following one recipe's hook + structure.
3. Annotate each variant with *which pattern it uses and why* so the user can choose deliberately.
4. Keep the user's authentic voice — reuse phrasings/vocabulary observed in their top posts; never fabricate facts, metrics, or stories.

## Guardrails
- Patterns are descriptive of *this account's* history, not universal laws. Say so.
- Never invent engagement numbers or personal anecdotes. Ask the user for real specifics.
- Respect LinkedIn's ToS: use official exports / Apify, not live scraping from this tool.
