# prompt,project,skill-creator

Instructions for a Project that designs prompts and instructions. The user dumps a rough, wordy request, and the Project turns it into something tight: a prompt ready for a single high-stakes run, a full Project instruction set, a `!` command for a specific Project, or a fix built from a patch report. It asks its questions first and holds the output until every one is answered.

| Category | Version | Works in |
|---|---|---|
| other | — | Claude chat (Project); Gemini Gem or custom GPT with fallbacks |

## What it does

| Mode | When | Output |
|---|---|---|
| 1. Tighten a prompt | A rough task to escalate to a stronger model for one high-stakes response | TIGHTENED PROMPT · MODEL CALL (Sonnet / Opus / Fable rubric) · MISSING PIECES (≤10) · TOOLS |
| 2. Draft Project/system instructions | A persistent instruction set for a new Project, for the user or someone else | DRAFT INSTRUCTIONS · DESIGN NOTES (2–4 bullets) · SCOPE CHECK |
| 3. Build a command | A `!name` command for a specific Project | Fit check, then COMMAND BLOCK · DECISIONS · TOOLS · MODEL CALL, plus a recommended test run |
| 4. Apply a patch report | The message is, or attaches, a file starting `# PATCH REPORT` | ROOT CAUSE · EDITS (LOCATION / FIND / REPLACE WITH / WHY) · SIDE EFFECTS · TEST · REPO |

Before writing a tightened prompt or a command, it runs a **capability pass** over its live tool and skill list. It writes the tools that help into the prompt and rejects the ones that don't earn their place.

## How it's triggered

There's no keyword. The mode is picked from context, and if the request is genuinely ambiguous, the Project asks which mode is meant. Mode 4 fires on any message that is, or attaches, a `# PATCH REPORT`, the format produced by the [patch skill](<../../skills/patch/README.md>).

## Inputs

- **Mode 1:** the rough task.
- **Mode 2:** the audience, the repeated task, the output format, and any hard constraints. It asks for whatever is missing.
- **Mode 3:** the target Project and its current instructions, which connectors, skills and web search are on, the command name and parameters, what's pasted each run, the steps and stops, the output format for each step, the revision loop, and hard constraints.
- **Mode 4:** the patch report, plus any source it marks INCOMPLETE.

## Output format

Each mode returns exactly the numbered sections in the table above, in that order. Command blocks are paste-ready, written in second person, and use hard STOPs. Tools appear as runtime rules ("X unavailable → do Y"). Patch edits give the exact FIND text and paste-ready REPLACE WITH text, each in its own fenced block. The style is fast and blunt.

## Dependencies

- None required.
- **Uses when present:** the live tool and skill list (for the capability pass), Project knowledge search, and web research.
- **Related:** the [patch skill](<../../skills/patch/README.md>) produces the reports that Mode 4 consumes.

## How to use

### Claude chat (Project)

1. Create a Project and paste the full text of [instructions.md](<instructions.md>) into its instructions.
2. Optional: install the [patch skill](<../../skills/patch/README.md>) to generate patch reports from other chats.
3. Paste a rough prompt, or describe the Project or command you want.

### Other LLMs (Gemini Gem, custom GPT)

Paste [instructions.md](<instructions.md>) as the Gem or GPT instructions.

| Claude-only feature | What to do instead |
|---|---|
| Model rubric (Sonnet / Opus / Fable) | Swap in your own model tiers, or ignore the MODEL CALL line |
| Capability pass over the live tool and skill list | List the tools your platform has in the chat, or skip the pass |
| `!` commands and skills inside Mode 3's output | They're written for claude.ai Projects; on other platforms, paste the command block as plain instructions |
| Patch reports (Mode 4) | Paste any bug write-up in the same layout: what failed, the quoted instructions, and the evidence |
