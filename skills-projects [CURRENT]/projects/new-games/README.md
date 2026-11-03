# new-games

Instructions for a gaming Project. It picks what to play from the user's backlog, judges whether a deal is worth buying now or waiting for, finds new releases that fit, and keeps the user's game library file accurate. It works solo (PC/Steam) by default, or for a 4-person cross-platform group when asked. Every game fact comes from `library.json`, and every price comes cited from a store or price tracker.

| Category | Version | Works in |
|---|---|---|
| other | — | Claude chat (Project); Gemini Gem or custom GPT with fallbacks |

## What it does

| Command | What it returns |
|---|---|
| `!mood <vibe> [filter] [group]` | 3 ranked backlog games for a mood (filter: `unplayed`, `installed` or `general`), each with a tag, a why line and a risk line, plus a top pick |
| `!check <game>` (also `!item`, `!game`) | The game's full library.json profile, live prices and the all-time low (ATL) if it isn't owned, warnings, and a verdict |
| `!wish` | A Steam wishlist screenshot turned into a verdict table (BUY first), the expected sale price for each WAIT, and a list of skipped items |
| `!new [mood/genre] [group]` | Up to 5 releases from the past and next 14 days that fit the taste profile and aren't already in the library |
| `!log <game> <status>` | One Claude Code prompt that makes targeted edits to library.json (status, buckets, counts, queues, notes) |
| Freeform | 3 ranked picks, leading with backlog |

- **Price rule:** BUY only at or within 10% of the ATL. Otherwise it gives `WAIT → <next sale>` and `COLLECT NOW → <store>`.
- **Warnings, not blocks:** taste dislikes and non-Steam titles get a warning and then full help. The only hard blocks are subscriptions and the group crossplay requirement.

## How it's triggered

A command keyword as the first thing in the message. Commands run solo unless the message includes `group`. Anything else is a freeform request, and if solo vs. group is unclear, it asks "Solo or group?"

## Inputs

- **`library.json`** in Project knowledge: ownership, status, genre, mood, input, playtime, flags, progress, and `meta.rules`.
- **`OVERVIEW.md`** in Project knowledge: the field map for library.json, including the valid `status` values.
- `!wish`: a Steam wishlist screenshot or pasted text.
- `!mood installed`: a list of installed games, if library.json has no `installed` field.

## Output format

Each response uses the tags `[OWNED — $0]`, `[FAMILY — $0]`, `[BUY — $X, Y% off]`, `[WATCH — $X now, target $Y]`, `[REBUY — $X]`, `[KEY — $X at <store>]`, `[GREY — $X at <store>]` and `[NOT ON STEAM]`. Data problems are flagged with ⚠️ and never fixed silently. Every response ends with a 1–3 line PROMPT NOTE, except bare commands.

## Dependencies

- **`library.json`** (required). The only source of truth for game facts, uploaded to Project knowledge. It isn't in this repo; you supply your own.
- **`OVERVIEW.md`** (required by `!log` and for field meanings). It isn't in this repo.
- **Web search**, for prices, ATLs, sale dates, new releases and crossplay checks. Price sources must be stores or price trackers (SteamDB, IsThereAnyDeal, GG.deals and so on).
- **Past-chat search** inside the Project (Claude only), used once per run to personalize answers.
- **Claude Code** (or any code agent), to run the `!log` prompt against your local library.json. The Project can't edit its own knowledge files.

## How to use

### Claude chat (Project)

1. Create a Project and paste the full text of [instructions.md](<instructions.md>) into its instructions.
2. Upload your `library.json` and `OVERVIEW.md` to the Project's knowledge.
3. Turn on web search and past-chat search (memory) for the Project.
4. **Make it yours:** replace the CONSTRAINTS (hardware, group consoles and subscriptions, budget), TASTE PROFILE and controller note with your own.
5. After a `!log`, run the prompt it gives you in Claude Code against your local library.json, then re-upload the file.

### Other LLMs (Gemini Gem, custom GPT)

Paste [instructions.md](<instructions.md>) as the Gem or GPT instructions and attach `library.json` and `OVERVIEW.md` as knowledge files.

| Claude-only feature | What to do instead |
|---|---|
| Past-chat search | Built-in fallback: nothing relevant found → say nothing. Optionally paste notes about recent plays |
| Project knowledge (`library.json`) | Attach it as a knowledge file, or paste the relevant entries |
| `!log` output as a Claude Code prompt | Give the prompt to any code agent, or apply the listed edits to the JSON by hand |
| Live web search for prices and crossplay | Use a model with browsing turned on, or paste prices yourself |
