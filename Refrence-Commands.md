# /command reference

`/command` is this repo's library-management command. It lives in `.claude/commands/command.md`. This file lists what each action does. If this file and the command file disagree, the command file wins, and both should be fixed together (they're a duplication pair in `.claude/CLAUDE.md`).

## Usage

| Action          | Syntax                                                      | What it does                                                                                  | Stops for you                                 |
| --------------- | ----------------------------------------------------------- | --------------------------------------------------------------------------------------------- | --------------------------------------------- |
| add             | `/command add <idea> [eval]`                                | Builds a new skill from its IDEAS.md entry, using skill-creator. Skills only.                 | Gap questions, build plan, safety-check fixes |
| fix (problem)   | `/command fix <name> "<problem>"`                           | Diagnoses and repairs a skill's, project's or prompt's behavior.                              | Fix plan, safety-check fixes                  |
| fix (wiring)    | `/command fix <name> wiring`                                | Checks and repairs the item's README row, IDEAS entry, versions, folder and links.            | Fix plan (only if something fails)            |
| dump            | `/command dump`                                             | Imports every skill zip in `dump/`: adds new skills and replaces existing ones in place.      | Name questions, import plan, zip delete offer |
| safety          | `/command safety all` or `/command safety <name> [<name>]`  | Checks for personal info, leaked keys, machine paths and unsafe scripts. `all` includes dump zips. | Findings list (you pick numbers)              |
| remove / delete | `/command remove <name>` or `/command delete <name>`        | Deletes the item and every reference to it.                                                   | Caution line, removal list, typed `delete`    |
| retire          | `/command retire <name>` or `/command remove <name> retire` | Moves the item to `skills-projects [RETIRED]/` and updates the README, IDEAS and links.       | Retire plan                                   |
| cleanup         | `/command cleanup`                                          | Runs a repo-wide surface check: wiring, links, folder READMEs, IDEAS status, untracked files. | Findings list (you pick numbers)              |

Actions and parameters are case-insensitive. Running `/command` with no action prints this table.

## Parameters

- `<idea>`: the kebab name of an IDEAS.md entry with `type: skill`.
- `<name>`: the name of a skill folder, a project folder or a PROMPTS.md entry. Skill and prompt names are kebab-case; project folder names can be anything.
- `eval`: runs skill-creator's test and eval loop during `add`. It's off by default.
- `"<problem>"`: what's wrong, in your words. Put it in quotes.
- `wiring`: checks connections only and leaves content alone.
- `all` (after safety): checks every skill, project and prompt, current or retired, plus the root docs and every zip in `dump/` and `dump/done/`.
- `retire` (after remove/delete): retires the item instead of deleting it.

## What every action does

- **Plans:** steps that change more than a status line open a Claude Code plan, and nothing changes until you approve it. If plan mode isn't available, the plan is posted in chat and the run stops.
- **Other items:** edits inside another skill's content, such as removing a link to a retired skill, always go through a plan.
- **Files:** moves use plain `mv`; deletes use `rm` on named files and `rmdir` on emptied folders, never `rm -rf`.
- **Git:** only read-only git. Nothing is ever staged or committed.
- **Report:** each run ends with skipped or unverified items at the top, then every file created, changed, moved or deleted.

## Importing with dump

Put skill zips in `dump/`, then run `/command dump`. `dump/` is tracked, so a committed zip is public, and safety fixes change only the imported skill, not the zip. Each skill is identified by the `name` in its SKILL.md, not by the zip's filename.

| Result    | When                                                         | What happens                                       |
| --------- | ------------------------------------------------------------ | -------------------------------------------------- |
| NEW       | No skill has that name.                                      | Added, with a README, CHANGELOG, README row and IDEAS entry. |
| REPLACE   | The skill exists and the zip differs.                        | Files replaced; README.md and CHANGELOG.md are kept and updated. |
| NO CHANGE | The skill exists and the files match, ignoring line endings. | Nothing changes.                                   |
| BLOCKED   | The skill's folder has uncommitted changes.                  | Nothing changes. Commit, then run it again.        |
| OLDER     | The zip's version is lower than the repo's.                  | Skipped unless you override it in the plan reply.  |

A zip is rejected if it has unsafe paths or symlinks. The SAFETY CHECK runs on the zip's contents before anything is written, and the plan shows its table so you can pick the fixes when you approve.

A replaced skill isn't moved to `skills-projects [RETIRED]/`, because it's still maintained and git already keeps the old version. Its CHANGELOG names the commit that holds it, which you can read with `git show <hash>:"skills-projects [CURRENT]/skills/<name>/SKILL.md"`. To discontinue a skill, use `retire`.

Processed zips move to `dump/done/`. Skipped, blocked and older zips stay in `dump/` for the next run. If a processed zip had a safety finding, the run offers to delete it, and deletes only the zips you name. The final report warns about any flagged or unscanned zip that's left, because committing it publishes its contents.

## Status flow in IDEAS.md

`idea` → (`add` asks the gap questions) → `designed` → (`add` builds it) → `built` → (`fix` from `needs-edit`) → `built` → (`retire`) → `retired`

`done` is set only by you.

## Not commands

- **Adding a prompt or a project:** ask Claude Code directly. It follows the Formats in `.claude/CLAUDE.md` and then runs the SAFETY CHECK.

## Examples

```text
/command add webapp-design
/command fix exam-review "description says five modes, README has six"
/command fix patch wiring
/command dump
/command safety all
/command safety handoff patch
/command retire council
/command delete old-skill
/command cleanup
```
