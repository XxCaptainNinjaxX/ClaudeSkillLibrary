---
description: Manage the skill library. Add a skill from IDEAS.md, fix a skill or its wiring, delete or retire an item, or clean up the repo.
argument-hint: add <idea> [eval] | fix <name> "<problem>" | fix <name> wiring | remove|delete <name> [retire] | retire <name> | cleanup
---

# /command: skill-library management

Arguments for this run: `$ARGUMENTS`

You manage this repo's skills, projects and prompts. `.claude/CLAUDE.md` is the rulebook. Its Baseline rules, Library conventions, Formats, Known duplication pairs and SAFETY CHECK apply to every step below. This file does not restate them, so read them from CLAUDE.md on every run.

## Shared rules

- The first word of the arguments is the action. Actions and parameters are case-insensitive. `remove` and `delete` are the same action.
- No action, or an unknown action: print the usage table from `Refrence-command.md` and STOP.
- Missing required parameter: ask for it and STOP. Never fill it from memory or guess.
- `<name>` must exactly match a folder, or a `### <name>` entry in IDEAS.md or PROMPTS.md. No exact match: list the closest names, ask which one, and STOP.
- Item kinds:
  - skill: `skills-projects [CURRENT]/skills/<name>/`
  - project: `skills-projects [CURRENT]/projects/<name>/`
  - prompt: a `### <name>` entry in PROMPTS.md
  - `add` handles skills only. Every other action handles all three kinds.
- During a run, invoke no skill except `skill-creator` (in `add`).
- Files:
  - Move with plain `mv`.
  - Delete with `rm` on named files and `rmdir` on emptied folders, deepest folder first. Never `rm -rf`.
  - Quote every path, because the folder names contain spaces and brackets.
- Git: read-only commands only (`status`, `log`, `ls-files`, `diff`). Never stage, `git mv`, commit, push, checkout or stash.
- Never invent content. Descriptions, triggers, categories and every other detail come from IDEAS.md or from the owner's answers in this run.
- An edit to one side of a duplication pair (CLAUDE.md list) also checks the other side, and the report says whether the other side changed.
- PLAN gate: every step marked PLAN proposes its plan in Claude Code plan mode, then STOPs until the owner approves.
  - Load the `EnterPlanMode` tool (through ToolSearch if it is deferred).
  - `EnterPlanMode` unavailable: write the plan in chat under a `PLAN` header and STOP.
  - No file changes before approval.
- Edits inside another item's content always go through a PLAN step and are never applied silently. Example: removing a link to a retired skill from a different skill's SKILL.md.
- The owner's next message after a STOP continues the current run.
- Reports go in chat. If the owner asks to save one, write it to `hidden/` as CLAUDE.md describes.
- Every run ends with a final report in this order:
  1. Anything skipped, failed or unverified, at the TOP.
  2. Files created, changed, moved and deleted, as paths.
  3. The line: "Nothing was staged or committed."

## Wiring check

Used by add, fix, retire and cleanup. For one item, record pass or fail and the evidence for each line:

- W1 location: the item is in the right `[CURRENT]` or `[RETIRED]` subfolder, and its name is kebab-case.
- W2 frontmatter:
  - `name` matches the folder name.
  - Only the allowed top-level keys appear.
  - `metadata.version` is a quoted `"x.y"`.
- W3 files: SKILL.md, README.md and CHANGELOG.md are present.
- W4 versions: `metadata.version` = newest CHANGELOG heading = the Version column in the root README.
- W5 root README:
  - A current item has a row in its category table. A retired item is listed under `## Retired`.
  - The link path resolves.
  - "What it does" is 15 words or fewer. Show the word count.
- W6 IDEAS.md:
  - The entry is under the right category.
  - `type` and `status` are correct.
  - `spec` links to the item's current path.
- W7 skill README: follows the `handoff/README.md` layout. List any missing sections by name.
- W8 links:
  - Every relative link in the item resolves.
  - Every relative link to the item resolves.
  - List the files that reference the item.
- W9 folder READMEs:
  - The four leaf folders each have a README.md.
  - The `[RETIRED]` READMEs list the retired items.

Projects and prompts: apply only the lines that fit, and name the lines skipped.

## add

`/command add <idea> [eval]`

- `<idea>` (required): the kebab name of an IDEAS.md entry with `type: skill`.
- `eval` (optional): run skill-creator's test and eval loop. Without it, skip that loop.

Before Step 1:

- `<idea>` missing: list the IDEAS.md entries with `type: skill` and status `idea` or `designed`, ask which one, and STOP.
- Entry has `type: prompt`: say that add handles skills only, and STOP.
- No entry: ask whether to create one, with the owner supplying the description. STOP.
- Folder already exists: say so, suggest `/command fix <name> wiring`, and STOP.

### Step 1: Gap questions (STOP)

Read the entry. Check it for each spec field:

- purpose
- triggers
- inputs
- exact output format
- edge cases
- dependencies
- target surfaces
- category (`education`, `career-planning`, `programming` or `other`)

Always ask whether this is an account skill (claude.ai upload) or a Claude Code skill, even if the entry says.

For every missing or unclear field, write one numbered question with one line on why it matters and a proposed default. Put all the questions in one message, then STOP.

Repeat this step until every field has an answer. Apply defaults only to the questions the owner answers with "default" or "defaults".

### Step 2: Spec and build plan (PLAN, STOP)

The plan shows:

- the full spec text for the IDEAS.md `spec:` field
- the status path `idea` → `designed` → `built`
- every file to create
- the root README row, with its "What it does" word count
- every IDEAS.md change

STOP for approval.

### Step 3: Build

1. Write the approved spec into IDEAS.md and set the status to `designed`.
2. Invoke the user-level `skill-creator`. Tell it:
   - The target folder is `skills-projects [CURRENT]/skills/<name>/`, not `~/.claude/skills/`.
   - Build from the approved spec.
   - Follow the CLAUDE.md frontmatter rules.
   - Skip the eval and benchmark loop unless `eval` was passed.
3. `skill-creator` unavailable: build by the CLAUDE.md Library conventions instead, and say so at the top of the final report.
4. Write README.md in the `handoff/README.md` layout.
5. Write CHANGELOG.md with the entry `## 1.0 — <today>` / `- Created.`
6. Set `metadata.version: "1.0"`.

### Step 4: Wire

1. Add the root README row.
2. In IDEAS.md, set the status to `built` and point `spec` at the new folder.
3. Run the Wiring check.
4. Fix any failure in files created this run. Report all other failures without fixing them.

### Step 5: Safety check (STOP)

1. Run the CLAUDE.md SAFETY CHECK on every file created or changed.
2. Output its table.
3. Ask which numbers to apply, and STOP.
4. Apply only the chosen numbers.

### Step 6: Report

1. The shared final report.
2. One install line for the chosen surface, taken from the skill's README:
   - account skill: the zip steps
   - Claude Code skill: the junction command

## fix

`/command fix <name> "<problem>"` repairs behavior.
`/command fix <name> wiring` checks links, folders, README and IDEAS only.

- `<name>` missing: ask for it and STOP.
- `<name>` given with neither a problem nor `wiring`: ask which one, and STOP.

### Problem fix

**Step 1: Diagnose and plan (PLAN, STOP).**

Read every file of the item and every duplication-pair counterpart. The plan gives:

- the problem, restated in one line
- the root cause, with `file:line` evidence
- the edits for each file, with exact text where it is short
- the version bump (minor for wording, major for behavior)
- the CHANGELOG line
- the root README and duplication-pair sync

Problem unclear: ask instead, and STOP.

**Step 2: Apply.**

1. Apply only the approved edits.
2. If the IDEAS.md status was `needs-edit`, set it to `built`.

**Step 3: Wiring check.** Run it on the item and report the results.

**Step 4: Safety check (STOP).** Run it as in add Step 5, on the changed files.

**Step 5: Report.**

### Wiring fix

**Step 1: Check.**

1. Run the Wiring check.
2. Output the table `# | Check | Result | Evidence | Proposed fix`.
3. If every line passes, say so, give the final report and end.

**Step 2: Fix plan (PLAN, STOP).**

- Propose fixes for the failures.
- A fix that needs an owner fact (category, description, target surface) asks for that fact inside the plan. Never pick the fact yourself.
- STOP for approval.

**Step 3: Apply and re-check.**

1. Apply only the approved fixes.
2. Re-run the Wiring check.
3. Show the pass count before → after.

**Step 4: Report.**

## remove / delete

`/command remove <name> [retire]` and `/command delete <name> [retire]` are identical.

- `<name>` (required): the item to remove.
- `retire` (optional): run the retire flow below instead of deleting.

### Step 1: Caution (STOP)

Print exactly this line:

`⚠️CAUTION are you SURE you want to fully delete skill from entire repository with NO trace left. or did you mean [retire] and move it to skills-projects [RETIRED]⚠️`

Then STOP and handle the reply:

- `retire`: run the retire flow.
- A clear yes: go to Step 2.
- Anything else: cancel and change nothing.

### Step 2: Removal list (PLAN, STOP)

List:

- every file to delete, one path per line
- every line to remove from the root README, IDEAS.md, PROMPTS.md and the `[RETIRED]` READMEs
- every other file that references the item, as `file:line`, with its proposed edit
- any link in `~/.claude/skills/<name>` that points into this repo. That folder is outside the repo, so only list it, and remove the link only if the owner says so. Never remove the link's target.

Give one line on why each item is safe to remove. Note that git history keeps old commits, and history is not rewritten.

End with the line: "Type `delete` to confirm." Then STOP.

Any reply other than the exact word `delete` cancels the run and changes nothing.

### Step 3: Delete

1. `rm` the named files, then `rmdir` the emptied folders, deepest first.
2. Remove the README rows and any other listed lines.
3. Remove the IDEAS.md entry entirely.
4. Apply the approved reference edits.
5. Where a section is now empty, restore its empty text: "No skills yet." in the README, "No items yet." in IDEAS.md.

### Step 4: Verify and report

1. Search the repo for the name.
2. Show the remaining hit count, which should be 0, and list any hits.
3. Give the final report.

## retire

`/command retire <name>`. `/command remove <name> retire` is the same flow.

### Step 1: Plan (PLAN, STOP)

If the destination already exists, STOP and ask. Otherwise the plan shows:

- the move:
  - skill or project: `mv` the folder to `skills-projects [RETIRED]/skills/<name>/` or `skills-projects [RETIRED]/projects/<name>/`
  - prompt: move the entry to a `## Retired` section at the end of PROMPTS.md, creating that section if it is missing
- root README:
  - remove the row from its category table
  - list the item under `## Retired`, replacing "Nothing retired yet."
- the matching `[RETIRED]` README: list the item, replacing "None yet."
- IDEAS.md: set the status to `retired` and point `spec` at the new path
- every other file that references the item, with its proposed edit
- any link in `~/.claude/skills/` that would break

STOP for approval.

### Step 2: Apply

1. Apply only the approved changes.
2. If a category table is now empty, write "No skills yet." there.

### Step 3: Check and report

1. Run Wiring check lines W1, W5, W6, W8 and W9 on the retired item.
2. Give the final report.

## cleanup

`/command cleanup` takes no parameters.

This is a surface-level check only. It never:

- suggests changes to what a skill does or how it is written
- compares the synced copies in `~/.claude/skills/synced/` against the repo
- runs the SAFETY CHECK (that runs separately)

### Step 1: Scan (STOP)

1. Run the Wiring check on every item in `[CURRENT]` and `[RETIRED]`.
2. Also check:
   - root README rows that have no folder, and folders that have no row
   - IDEAS.md entries:
     - folder exists but the status is `idea` or `designed`: propose `built` plus a `spec` link
     - status `built` or `done` with no folder: flag it
     - items that have no entry: flag them
   - broken relative links in every `.md` file
   - untracked or modified files (from `git status`), as a reminder to commit
   - case-only mismatches between `git ls-files` and disk. Give the owner the `git rm --cached <old>` / `git add <new>` fix to run themselves.
   - version mismatches across duplication pairs
3. Output the table `# | Item | File | Finding | Proposed fix`.
4. Output the counts line: `items scanned: N | findings: N | IDEAS open: N`.
5. Output an "IDEAS reminder": every entry with status `idea`, `designed` or `needs-edit`, one line each, as `name — status — first 15 words of the description`.
6. Ask which numbers to apply: `all`, a list of numbers, or `none`. STOP.

### Step 2: Apply

- Apply status changes and README rows directly.
- A fix that edits another item's content, or needs an owner fact, goes through a PLAN step and STOPs.

### Step 3: Re-scan and report

1. Re-scan the fixed items.
2. Show the finding count before → after.
3. Give the final report.
