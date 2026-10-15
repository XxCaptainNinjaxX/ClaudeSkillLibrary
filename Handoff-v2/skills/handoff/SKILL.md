---
name: "handoff"
description: "Compress the current chat into a handoff a new chat (Claude, Gemini, or ChatGPT) can continue from — state, decisions, rules, next step. Use on /handoff, \"handoff\", \"continue this in a new chat\", \"carry this over\", or a request to summarize the chat so another chat can pick it up. Also /handoff overview (or !overview) for an AI-ready context overview used to refine a prompt or write project instructions, and /handoff overview prompt to print the portable overview prompt for pasting elsewhere."
---

# Handoff

Three modes. Pick by the user's message:

| Invocation | Mode | Output |
|---|---|---|
| `/handoff`, "make a handoff", "continue this in a new chat" | **Full handoff** | `.md` file a new chat continues from |
| `/handoff overview`, `!overview`, "give me an overview for a prompt/instructions" | **Overview** | Compact AI-parsed context block, in chat |
| `/handoff overview prompt`, `!overview prompt` | **Portable prompt** | The OVERVIEW PROMPT below, verbatim, nothing else |

The next reader may be Claude, Gemini, or ChatGPT. Never write anything that only works on Claude without marking it optional.

---

## MODE A — Full handoff

One `.md` file the user pastes or uploads into a new chat. Success test: the new chat's first reply feels like the next turn of the old chat. Same mode, same formatting, no re-explaining, no lost gaps.

A handoff is **not a summary**. A summary says what happened. A handoff tells the next assistant *how to act* and *what it would otherwise get wrong*.

### Step 1 — Read the whole chat, then classify it

Go through every turn still in context, from the first message to the latest. Before writing, decide:

1. **Primary topic type** from the Topic modules section (study, research/planning, technical, decision/purchase, creative, casual). If two are mixed, use the dominant one and borrow a section or two from the other.
2. **Where the chat stands.** The last open thread: the unanswered question, the undone step, the next quiz item.
3. **Whether early turns are missing.** If the start looks compressed or cut (references you can't resolve, a summary block in place of early turns), say so under "Context gaps". Never invent what you can't see.

### Step 2 — Extract, in this priority order

Keep an item only if the next chat would behave differently, or worse, without it.

1. **Instructions and formatting rules.** Every time the user said how to answer ("drop the prompt note", "don't call me X", "5 analogies per topic", "quiz me one at a time"), capture it as a direct rule, in its final form if later changed. **Include rules from Project instructions and saved preferences too**, unless the user says the new chat will be in the same Project on the same platform. A duplicate costs one line; a missing rule breaks the handoff.
2. **Corrections.** Each time the user corrected the assistant ("no, that's wrong", "I meant X", "stop doing Y"), record the correct version. These are the most expensive things to lose.
3. **Resume point.** The exact next action, phrased so it can be done immediately.
4. **Decisions made**, with a one-line reason each, so the next chat doesn't relitigate them.
5. **Rejected options**, with why, so the next chat doesn't re-suggest them.
6. **Core facts and data.** Exact numbers, names, dates, specs, scores, quotes. Never round or paraphrase numbers.
7. **Open questions**, split into user-must-answer vs. assistant-should-look-up.
8. **Topic-specific sections** from Topic modules.

### Step 3 — Write using the template

- **Zero-context reader.** No "as discussed", "the thing from earlier", or "that option". Name things.
- **Attribute correctly.** "User chose X" only if the user said so. Otherwise "Assistant suggested X — user hasn't confirmed."
- **Mark confidence.** Looked-up or estimated facts not verified get `(unverified)`.
- **Compress, don't drop.** Long back-and-forth becomes one line of outcome.
- **Date-stamp** prices, stock, deadlines, "currently" statements: `(as of YYYY-MM-DD)`.
- **Files don't travel.** List every uploaded or produced file under "Files to re-attach", with what it was used for.
- **No length cap.** A 20-turn chat might be 40 lines; a 200-turn review might be 250. Every line must earn its place.
- **Platform-specific steps** (Projects, memory, skills, artifacts) are marked `(Claude only)` so another model skips them cleanly.

### Step 4 — Deliver

1. Filename: `handoff-<short-topic-slug>-<YYYY-MM-DD>.md` (e.g. `handoff-acct-midterm-review-2026-10-15.md`).
2. Write it to `/mnt/user-data/outputs/` if that exists, otherwise the working directory, and send it with the available file tool (`present_files` or `SendUserFile`). If none exists, put the whole file in one fenced markdown block.
3. After the file, **at most 3 lines** in chat: topic type used, anything in Context gaps, files to re-attach. Don't repeat contents.

### Template

Fill every section that applies. Delete empty sections entirely; no "N/A". Keep the order: the top is read first and weighted most.

```markdown
# Handoff — <Topic, in plain words>

> **To the next assistant:** This file continues a previous chat. Treat everything
> below as established context. Do not re-introduce yourself, re-explain covered
> material, or ask for info already listed here. Follow "How to respond" exactly;
> it overrides your defaults. Items marked (Claude only) can be skipped on other
> platforms. Start by doing the Resume point.

_Handoff created: <YYYY-MM-DD> · Topic type: <study | research/planning | technical | decision | creative | casual> · Source chat length: <rough turn count>_

## How to respond
<!-- Rules from the chat, Project instructions, and preferences, as direct commands.
Note when a rule overrides a default. -->
- <e.g. Do NOT add the end-of-response prompt note.>
- <e.g. Teach with 5 analogies per concept, plain explanation first.>

## Resume point
<e.g. Ask practice question 14 (accrual vs. cash basis). User has missed this twice.>

## Goal
<1–2 lines: what the user is trying to get done, and by when.>

## Current state
<Bullets, exact values.>

## Decisions made
- <Decision> — <why>

## Suggested but not confirmed

## Rejected / ruled out
- <Option> — <why>

## Corrections to remember
- <Wrong assumption> → <correct version>

## Key facts & data
<Exact values. (unverified) and (as of YYYY-MM-DD) where relevant.>

## <Topic-specific sections>

## Open questions
**User needs to answer:**
-
**Assistant should look up / verify:**
-

## Files to re-attach
- `<filename>` — <what it is, what it was used for>

## Reference archive
<Past info not active. Compact, outcome over transcript.>

## Context gaps
<Early turns cut from context, anything ambiguous. Omit if none.>
```

### Topic modules

**Study / academic review**
- Course & exam: name, assessment, date, format (MC, written, open-note), chapters in scope.
- Session mode: explaining, active recall, practice exam, flashcards, cheat sheet; note any skill in use (e.g. slide-breakdown, exam-review).
- Coverage map: ✅ covered · 🟡 partial · ⬜ not yet.
- Weak spots: concept, the specific mistake, the correct answer, repeat count ("missed 2×").
- Strong spots: don't re-drill.
- Score log (e.g. "Ch 4 recall: 7/10").
- Question queue: already asked + next planned.
- Materials (also under Files to re-attach).

**Research / career / planning**
- Question being answered, stated sharply.
- Findings with source link and date; (unverified) where needed.
- Options × criteria table if one was built.
- Criteria & constraints the user stated (budget, location, timeline, values).
- Action items with deadlines.
- Contacts / names and their relevance.

**Technical / code / build**
- Project & stack: repo, language, framework, environment.
- Working / broken per component.
- Changes made: files touched, what changed (short critical snippets only).
- Errors in play: exact message text + what's been tried.
- Constraints (no new deps, don't touch X, style rules).
- Next steps, ordered.

**Decision / purchase**
- Item & situation: exact model/config/price.
- Comparison table: price, warranty, key specs, risks.
- Deadlines (return windows, sale ends) with actual dates computed.
- Decision rule: "if X by date Y, then Z".

**Creative (writing, design, music)**
- Piece & purpose: audience, tone.
- Current draft state or file to re-attach.
- Style rules, likes/dislikes from past drafts.
- Feedback log in order.

**Casual / hobby**
- What the user is doing and where they're at (level, episode, build).
- Preferences expressed; recommendations given and reactions.
- Keep to ~30 lines.

### Things that break handoffs

- Narrative recap ("First we talked about..."). State, not story.
- Losing formatting rules. Most common failure, and the one the user cares most about.
- Collapsing "assistant suggested" into "user decided".
- A vague resume point. "Continue the review" fails; "Ask question 14: accrual vs. cash basis, missed twice" works.
- Including private details irrelevant to the task.

---

## MODE B — Overview

Run the OVERVIEW PROMPT below on the current conversation and output only its result, in chat. No file unless the user asks. Purpose: feed the output to an AI to refine a prompt, write project/system instructions, or continue the work.

## MODE C — Portable prompt

Output the OVERVIEW PROMPT below verbatim in a single code block. Nothing else: no greeting, no commentary, no prompt note. The user will paste it into another chat, another model, or send it to someone else.

### OVERVIEW PROMPT

```
Produce a context handoff of this conversation. Another AI will read it to refine a prompt, write project/system instructions, or continue the work. Optimize for machine parsing, not human readability. Target under 800 words; go longer only if the material demands it.

SOURCES: Scan everything you can access: this conversation, attached files, and, if your platform provides them, project files, saved memory, custom instructions, and past-chat search. Never guess at what you can't see.

RULES:
- Tag every fact [stated] (user said it) or [inferred] (you concluded it).
- No invention. Empty section = "none".
- Quote verbatim only where exact wording matters (constraints, required formats, names, numbers). Paraphrase the rest.
- Record decisions, not advice. Your own suggestions the user didn't accept are not decisions.
- If you can't disclose instructions verbatim, summarize them and say so.
- No preamble or closing. Output the handoff only, in one markdown code block.

FORMAT:
# CONTEXT HANDOFF
## Meta
- Platform/model:
- Date:
- Sources scanned:
- Sources NOT visible: (referenced but inaccessible)
## Goal
One line: the user's end goal. Then the deliverable type: prompt | project instructions | other (specify).
## Request history
Chronological, one line per user turn: what was asked + how it changed the task. Flag scope changes and corrections.
## Existing instructions
System/project/custom instructions, saved preferences, memory that shape behavior. Verbatim if permitted.
## Context & knowledge
Files and key facts, one line each: name — contents — why it matters.
## Constraints
Hard (must/never) vs soft (preferences): format, length, tone, tools, audience, platform.
## Decisions
What's settled + one-line reason. Include rejected options and why.
## Failures & corrections
Outputs the user pushed back on and what they wanted instead.
## Open questions
Unresolved items blocking the next step.
## Gaps
What a prompt or instruction writer would need that isn't here.
```