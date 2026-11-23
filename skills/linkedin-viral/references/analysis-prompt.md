# Structured analysis prompt

Use this against the user's post export (after computing an engagement score and splitting into top/bottom cohorts).

## Goal
Explain *why* the top cohort outperformed the bottom cohort for THIS account, in patterns concrete enough to reproduce.

## Analyze each post on these dimensions
- **Hook (line 1):** type — question / bold claim / contrarian / story-open / stat / "I did X" confession. Length in words.
- **Length:** total chars; short (<400) / medium / long-form.
- **Structure:** single block vs. short lines; bullet/numbered lists; presence of a "see more" fold break.
- **Angle:** story · contrarian/hot-take · how-to/framework · data/insight · vulnerability/personal · curation.
- **Formatting:** emoji count, line-break density, ALL-CAPS, arrows/symbols.
- **CTA:** none / question to audience / "comment X" / link / DM.
- **Topic cluster:** group into 4–8 themes.
- **Timing:** day-of-week / hour if available.

## Output (report)
1. **Top correlates** — ranked list: "Posts that did X scored N× higher (n=…)." Flag low-sample patterns honestly.
2. **Anti-patterns** — what the bottom cohort shares.
3. **Account voice notes** — recurring phrasings, vocabulary, tone the audience rewards.
4. **3–6 reusable recipes to extract** — name each; these feed `recipe-template.md`.

Keep it specific and evidence-based. Cite counts. Avoid generic "post consistently" advice unless the data shows it.
