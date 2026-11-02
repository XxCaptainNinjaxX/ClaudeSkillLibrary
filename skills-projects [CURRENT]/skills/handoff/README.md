# handoff

Compresses the current chat into a handoff that a new chat (Claude, Gemini or ChatGPT) can continue from. A handoff isn't a summary: it tells the next assistant how to act and what it would otherwise get wrong.

| Category | Version | Works in |
|---|---|---|
| other | 2.0 | Claude chat, Claude Code, Gemini, any |

## What it does

Three modes:

| Mode | Invocation | Output |
|---|---|---|
| Full handoff | `/handoff`, "make a handoff", "continue this in a new chat" | A `.md` file a new chat continues from |
| Overview | `/handoff overview`, `!overview` | A compact, machine-parsable context block, in chat |
| Portable prompt | `/handoff overview prompt`, `!overview prompt` | The OVERVIEW PROMPT, verbatim, for pasting into any other chat or model |

The full handoff captures, in priority order: the user's formatting and behavior rules (including Project instructions and saved preferences), corrections, the exact resume point, decisions with reasons, rejected options, exact facts and numbers, and open questions. It adds extra sections for the chat's type (study, research/planning, technical, decision/purchase, creative, casual). Anything that only works on Claude is marked `(Claude only)`.

## How it's triggered

`/handoff`, "handoff", "continue this in a new chat", "carry this over", or a request to summarize the chat so another chat can pick it up. `/handoff overview` (or `!overview`) and `/handoff overview prompt` (or `!overview prompt`) select the other two modes.

## Inputs

- The current conversation: every turn still in context. If early turns were cut, it says so under "Context gaps" and doesn't invent them.
- Files attached or produced in the chat. They're listed under "Files to re-attach", because files don't travel with the handoff.
- Project instructions and saved preferences, when the platform exposes them.

## Output format

- **Full handoff:** `handoff-<short-topic-slug>-<YYYY-MM-DD>.md`. It opens with a "To the next assistant" note, then these sections in order: How to respond, Resume point, Goal, Current state, Decisions made, Suggested but not confirmed, Rejected / ruled out, Corrections to remember, Key facts & data, topic-specific sections, Open questions, Files to re-attach, Reference archive, Context gaps. Empty sections are left out. After the file, at most 3 lines in chat.
- **Overview:** one markdown code block headed `# CONTEXT HANDOFF`, with Meta, Goal, Request history, Existing instructions, Context & knowledge, Constraints, Decisions, Failures & corrections, Open questions and Gaps. Facts are tagged `[stated]` or `[inferred]`; the target is under 800 words.
- **Portable prompt:** the OVERVIEW PROMPT in a single code block, nothing else.

## Dependencies

- None. A file tool (`present_files` or `SendUserFile`) is used when available. Otherwise the file goes to the working directory, or the whole handoff comes back in one fenced markdown block.
- `references/template.md` and `references/topic-modules.md` are older copies of the template and topic modules. SKILL.md doesn't load them; the current versions are inline in SKILL.md.

## How to use

### Claude Code

From the repo root:

```bash
mkdir -p ~/.claude/skills
ln -s "$PWD/skills-projects [CURRENT]/skills/handoff" ~/.claude/skills/handoff
```

On Windows, Git Bash's `ln -s` copies the folder instead of linking it (unless native symlinks are turned on), so later edits won't reach Claude Code. Use a junction from PowerShell instead, also from the repo root (`mklink` is used because PowerShell's `New-Item` misreads the `[ ]` in the path):

```powershell
New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
cmd /c mklink /J "$HOME\.claude\skills\handoff" "$PWD\skills-projects [CURRENT]\skills\handoff"
```

In Claude Code, the handoff file is written to the working directory.

### Claude chat

Zip the folder so the zip contains `handoff/SKILL.md`. README.md and CHANGELOG.md are for people, so leave them out. From the repo's `skills-projects [CURRENT]/skills/` folder:

```bash
# macOS / Linux
zip -r handoff.zip handoff -x "handoff/README.md" "handoff/CHANGELOG.md"
```

```powershell
# Windows
tar -a -cf handoff.zip --exclude=README.md --exclude=CHANGELOG.md handoff
```

Upload the zip as a custom skill in Claude's settings (skills need code execution and file creation turned on).

### Other LLMs (Gemini, ChatGPT, plain prompt)

Paste the SKILL.md body (everything after the closing `---` of the frontmatter) as custom instructions, a Gem, or a system prompt, then say "handoff" or "handoff overview". The skill was written to work across models.

| Claude-only feature | What to do instead |
|---|---|
| Slash commands (`/handoff`) | Say "handoff", "handoff overview" or "handoff overview prompt" |
| Saving and presenting the file (`/mnt/user-data/outputs/`, `present_files`, `SendUserFile`) | Built-in fallback: the handoff comes back in one fenced markdown block; save it as a `.md` file |
| Project, memory and skill references inside a handoff | Marked `(Claude only)`, so another model can skip them |

For the overview alone, copy the OVERVIEW PROMPT block from SKILL.md and paste it into any chat.
