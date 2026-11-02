# patch

Packages a claude.ai failure (a Project's custom instructions, a `!` command, a skill, a preference or a memory line that misfired) into one self-contained report that a separate chat can use to find and fix the instruction responsible. It reports only; it never fixes anything in the broken chat, because the model that misbehaved tends to patch symptoms, not causes.

| Category | Version | Works in |
|---|---|---|
| other | 1.0 | Claude chat |

## What it does

In the chat where Claude got something wrong, it collects your issue in your own words, the relevant turns quoted verbatim, the full governing instructions, any conflicting rules, which tools were live, and a hypothesis about the cause. It writes all of that into one report file.

## How it's triggered

Only when `/patch` is the first thing in a message. It doesn't fire on the chat's content, and it isn't for continuing work (that is handoff).

## Inputs

- `/patch`, optionally followed by what went wrong and what it should do instead.
- If you leave that out and haven't said it earlier in the chat, it asks once: "What did it do wrong, and what should it do instead?"
- The current conversation and whatever instructions are visible in it. Anything it can't see in full is marked INCOMPLETE and listed for you to attach.

## Output format

`patch-<target>-<YYYY-MM-DD>.md`, with these sections in order: Issue (your words), Environment, Evidence, Governing instructions, Diagnosis (hypothesis only, with a class: GAP, MISREAD, CONFLICT, TRIGGER, TOOL or OTHER), and Completeness check. After the file, one line tells you to paste or attach it alone in a new chat in the Project that maintains your instructions. That chat returns the edits and a test message.

If you correct the report, it regenerates the whole report with the same file name.

## Dependencies

None. Without file tools, it outputs the report in a `~~~~` fenced block instead of a file.

## How to use

### Claude Code

Not intended for Claude Code: `patch` diagnoses claude.ai failures (Projects, `!` commands, preferences, memory), which Claude Code doesn't have. If you still want it there, from the repo root:

```bash
mkdir -p ~/.claude/skills
ln -s "$PWD/skills-projects [CURRENT]/skills/patch" ~/.claude/skills/patch
```

On Windows, Git Bash's `ln -s` copies the folder instead of linking it (unless native symlinks are turned on), so later edits won't reach Claude Code. Use a junction from PowerShell instead, also from the repo root (`mklink` is used because PowerShell's `New-Item` misreads the `[ ]` in the path):

```powershell
New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
cmd /c mklink /J "$HOME\.claude\skills\patch" "$PWD\skills-projects [CURRENT]\skills\patch"
```

### Claude chat

Zip the folder so the zip contains `patch/SKILL.md`. README.md and CHANGELOG.md are for people, so leave them out. From the repo's `skills-projects [CURRENT]/skills/` folder:

```bash
# macOS / Linux
zip -r patch.zip patch -x "patch/README.md" "patch/CHANGELOG.md"
```

```powershell
# Windows
tar -a -cf patch.zip --exclude=README.md --exclude=CHANGELOG.md patch
```

Upload the zip as a custom skill in claude.ai skill settings (skills need code execution and file creation turned on).

### Other LLMs (Gemini, ChatGPT, plain prompt)

Paste the SKILL.md body (everything after the closing `---` of the frontmatter) as custom instructions, a Gem, or a system prompt, then say "patch" with what went wrong. It was written for claude.ai, so the failure sources it looks for may not exist elsewhere.

| Claude-only feature | What to do instead |
|---|---|
| Slash command (`/patch`) | Say "patch" as the first thing in a message |
| Project instructions, `!` commands, memory, preferences and loaded skills as failure sources | Paste the instruction text you think misfired into the chat, so it can be quoted |
| Writing and sending the report file | Built-in fallback: the report comes back in one `~~~~` fenced block; save it as a `.md` file |
