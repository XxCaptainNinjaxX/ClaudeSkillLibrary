---
name: patch
description: Use ONLY when the user types /patch as the first thing in a message. Packages a claude.ai failure (a Project instruction, ! command, skill, preference or memory line that produced the wrong behavior) into one self-contained patch report for a separate chat to fix. Not for continuing work (that is handoff) and not for fixing anything in this chat.
metadata:
  version: "1.0"
---

# /patch: failure report builder

The user saw Claude do something wrong in this chat. Build a report that lets a
different chat, one that has never seen this conversation, find and fix the
instruction responsible. You are a witness, not the fixer.

## Hard rules

- Trigger only when `/patch` is the first thing in the message.
- Do not redo, continue or correct the original task. Do not apologize. Do not
  edit any instructions, memory or files other than the report.
- While /patch runs, no other skill triggers on the conversation's content. If
  the failure involved a skill, quote it; don't run it.
- Verbatim means character for character. Never paraphrase quoted instructions
  or outputs. If you can't see the full text, mark it INCOMPLETE. Never rebuild
  it from memory.
- The concern and the wanted behavior come only from the user's own words. Never
  infer what they want.
- Nothing account-level goes inside the report: no openers, sign-offs or prompt
  notes. Those stay outside the file or are skipped.

## Step 1: Get the issue (may STOP)

1. The /patch message describes what went wrong and what should happen instead
   → use it verbatim.
2. Otherwise, earlier user messages in this chat state it (a correction, "don't
   do X", "I wanted Y") → quote those verbatim and note their turn numbers.
3. Otherwise, or if the wanted behavior is still missing → send exactly:
   "What did it do wrong, and what should it do instead?" then STOP and wait.

## Step 2: Find the failure

Scan the whole conversation and identify:

- the first turn where the wrong behavior appeared, and every recurrence after it
- each correction the user made, and whether the next turn complied, partly
  complied or repeated the error
- every instruction source that governed that behavior. Check all of these:
  Project custom instructions, Project knowledge files, skills loaded this chat
  (their SKILL.md), user preferences, memory, style, tool descriptions and
  system-level defaults.

Relevance test: include a turn or line only if leaving it out would make the
failure harder to diagnose.

## Step 3: Pull the instructions

- Copy the full governing unit verbatim: the whole ! command (signature through
  revision loop), the whole SKILL.md, or the whole relevant section of the
  Project instructions. Add any shared rules it inherits, such as a COMMANDS
  header.
- Copy every other line, from any source, that conflicts or interacts with it,
  verbatim and labeled with its source.
- For a loaded skill: if file tools are available, read its SKILL.md from disk;
  otherwise copy it from context.
- If a source can't be seen in full (truncated, not in context, a knowledge file
  that was never opened) → mark that slot INCOMPLETE and say exactly what the
  user must attach.

## Step 4: Diagnose (hypothesis only)

- Classify the failure as one of:
  - GAP: no instruction covers it
  - MISREAD: an instruction covers it and wasn't followed
  - CONFLICT: two instructions disagree. Name which one won and why.
  - TRIGGER: the wrong skill or command fired, or the right one didn't
  - TOOL: a needed tool was missing, failed or was misused
  - OTHER
- Quote the line(s) you actually followed. For a GAP, state what you assumed.
- In one line, say what you would have needed to be told.
- Do NOT write replacement instruction text. The fix is written elsewhere,
  against the full rule set.

## Step 5: Write the report

File name: `patch-<target-name>-<YYYY-MM-DD>.md`. Use this structure exactly.
The XML tags keep quoted markdown headers and code fences from breaking the
report.

```
# PATCH REPORT
target: <name> · type: <project instructions | ! command | account skill | plugin skill | user preference | memory | style | other>
project: <Project name, or "unknown"> · model: <model running this chat> · date: <YYYY-MM-DD>

## 1. Issue (user's words)
<concern turn="n">verbatim</concern>
<wanted turn="n">verbatim</wanted>

## 2. Environment
tools available this chat: <list>
skills available: <list>
tools/skills used in failing turns: <list, or "none">

## 3. Evidence
<turn n="#" role="user|assistant" note="first failure | correction | recurrence | trigger">
verbatim text. Trim only unrelated spans, as [... trimmed N lines: what they were]
</turn>
correction outcomes: <turn # → complied | partial | repeated>

## 4. Governing instructions
<source name="<name>" location="<project instructions | knowledge file X | skill path | preferences | memory path | other>" complete="yes|INCOMPLETE">
verbatim
</source>
<interacting source="..." location="..." why="conflicts | modifies | triggers">
verbatim line(s)
</interacting>

## 5. Diagnosis (hypothesis)
class: <GAP | MISREAD | CONFLICT | TRIGGER | TOOL | OTHER>
followed: <quote, or "GAP: assumed ...">
needed to be told: <one line>

## 6. Completeness check
turns included: <N> (first failure #<n>; recurrences #<list>)
sources quoted: <N> complete, <N> INCOMPLETE → user must attach: <list, or "nothing">
issue from user's words: <yes, turn #> · wanted from user's words: <yes, turn #>
empty sections: <list, or "none">
```

Fill section 6 with the real counts, not a pass/fail claim.

## Step 6: Deliver

- File tools available → write the file and send it. Then reply with one line
  only: "Paste or attach this alone in a new chat in your prompt-design Project."
- File tools unavailable → output the report in one block fenced with `~~~~`
  (four tildes, so the ``` fences inside quoted text don't close it), with
  nothing else inside the block, followed by the same one line.

## Revision loop

If the user corrects the report ("you missed the second output", "the issue is
actually..."), regenerate the whole report with the same file name and resend
it. Don't send a diff.
