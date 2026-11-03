# research-items

Instructions for a shopping research Project. Give it an item you're looking to buy, from any store or website, and it returns a ranked, cross-referenced shortlist first. It only goes on to availability, where to buy, and direct links when you say you're ready. It never assumes a retailer or category, and it says so plainly when a listing looks like a scam.

| Category | Version | Works in |
|---|---|---|
| other | — | Claude chat (Project), Gemini, any |

## What it does

| Stage | When | Output |
|---|---|---|
| 0. Questions | Budget, use or must-haves are missing, or the request is too vague | One short question, then it waits |
| 1. Ranked list | Always first | 5–10 distinct options, ranked. Each says what it is, why it qualifies, and why it beat the one below and lost to the one above. Then a cheapest reliable alternative and a most reliable alternative |
| 2. Breakdown | Only on "I'm ready" or "give me the breakdown" | Availability, in-person stores or online retailers, a direct link for every online claim, and any changes since Stage 1 |
| Last stage | At the end of the research | An overview chart by scenario (best for budget, most reliable, and so on) with cost, what each item offers, and why it made the list |

## How it's triggered

Any request to research or compare an item to buy. Stage 2 only runs once you say you're ready.

## Inputs

- What you're looking for.
- Budget, what it's for, and any must-haves or dealbreakers. It asks for these if they're missing.

## Output format

Plain everyday language with no spec-sheet dumps. Every claim (price, rating, durability, specs) is cross-checked against more than one source, and conflicts between sources are stated. Near-duplicates are noted instead of listed twice. Time-sensitive prices and stock are flagged.

## Dependencies

- **Web search**, for listings, reviews and links. Without it, paste the listings you're comparing.

## How to use

### Claude chat (Project)

1. Create a Project and paste the full text of [instructions.md](<instructions.md>) into its instructions.
2. Turn on web search.
3. Describe what you want to buy, with a budget if you have one.

### Other LLMs (Gemini Gem, custom GPT, plain prompt)

Paste [instructions.md](<instructions.md>) as the Gem or GPT instructions, or as the first message of a chat. Nothing in it is Claude-only, except that line 23 names "Claude" as the one picking the most reliable option, which works fine on any model.

| Claude-only feature | What to do instead |
|---|---|
| None | Use a model with browsing turned on for live prices and links |
