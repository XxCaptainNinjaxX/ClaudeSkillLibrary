# CLAUDE.md: claude-skill-Library

A public, MIT-licensed library of AI skills and saved prompts. It's maintained in Claude Code; the skills and prompts are used in Claude chat, Claude Code, Gemini, and as pasted plain prompts. **Everything committed here is public.**

## Baseline rules

> ⚠️ VERIFY: reconstructed because the master template (`.claude/CLAUDE-master-.MD`) was empty on 2026-10-26. These are only the rules stated in the migration task; compare them with your template and add anything missing.

- **No commits, no staging, no `git mv`.** The owner handles git. Rename with plain `mv`.
- **No new dependencies** (packages, tools, services) without asking first.
- **Audit before deleting.** Read the target and say why it should go before removing it. Delete named files with `rm` and emptied folders with `rmdir`; never `rm -rf`.
- **Mark uncertain points with `⚠️ VERIFY`** instead of guessing.
- **Never let a partial task read as complete.** Put anything skipped, failed or unverified at the top of the report.
- **No build gate.** Nothing builds here. The SAFETY CHECK below is the gate before the owner pushes.

## Stack

- Markdown: skills (`skills-projects [CURRENT]/skills/<name>/SKILL.md` plus reference files), Project instructions (`skills-projects [CURRENT]/projects/`), `PROMPTS.md`, `IDEAS.md`, and READMEs.
- Python 3 scripts in `skills-projects [CURRENT]/skills/council/scripts/`. They use only the standard library, except `validate_config.py` and its test, which need PyYAML.

## Deployment

Public GitHub repo, branch `main`. No CI, and nothing builds. The only gate before the owner pushes is the SAFETY CHECK: run it on everything that changed, report the findings, and let the owner pick which fixes to apply.

## Commands

Run these from the repo root (the folder names contain spaces and brackets, so keep the quotes). They're the only real commands:

- `python3 "skills-projects [CURRENT]/skills/council/scripts/test_tally.py"`: council tally tests, standard library only (10 tests passing on 2026-10-26).
- `python3 "skills-projects [CURRENT]/skills/council/scripts/test_validate_config.py"`: config validator tests. Needs PyYAML, which isn't installed on the owner's machine; ask before installing it.
- `python3 "skills-projects [CURRENT]/skills/council/scripts/validate_config.py" --print-default`: prints council's default panel. Needs PyYAML.
- A mechanical sweep for SAFETY CHECK items 1–3. It covers the working tree including untracked files, honors `.gitignore`, and skips this file, which quotes the patterns. Exit code 1 means no matches:

  ```bash
  git grep -nIiE --untracked '(^|[^a-z0-9])sk-[a-z0-9_-]{16,}|ghp_|github_pat_|AKIA[0-9a-z]{12,}|Bearer [a-z0-9._-]{8,}|api[_-]?key|password|secret|/Users/|[a-z]:.Users|/home/|[a-z0-9._%+-]+@[a-z0-9-]+\.[a-z]{2,}' -- . ':(exclude).claude/CLAUDE.md'
  ```

  It doesn't catch names, schools, courses or context leaks; read the changed files for those.

## Do not touch

- `LICENSE`
- `.claude/CLAUDE-master-.MD`
- `.env`

## Hidden folder (private output)

`hidden/` at the repo root is gitignored (`/hidden` in `.gitignore`), so nothing in it is ever pushed. Put any file I produce for the owner that isn't part of the library there: reports, repo maps, discovery or audit output, scratch notes, and anything that may carry personal info. Use `.txt` (or `.md`) names like `repo-map-report.txt`. Never put library content (skills, prompts, READMEs) in it. Nothing here counts toward the SAFETY CHECK, but still don't write secrets into it.

## Source of truth

`IDEAS.md` is the inventory and status record for every skill and prompt. Its notes hold open items, including the 2026-10-26 migration safety findings that haven't been applied yet. When a status changes, update IDEAS.md first, then sync the duplication pairs below.

## Known duplication pairs (change both sides together)

- `IDEAS.md` ↔ root `README.md` (skill list)
- `PROMPTS.md` ↔ root `README.md` (prompt categories)
- SKILL.md `metadata.version` ↔ `CHANGELOG.md` ↔ root `README.md` (Version column)
- `skills-projects [CURRENT]/skills/exam-review/SKILL.md` ↔ `skills-projects [CURRENT]/skills/slide-breakdown/SKILL.md` (the no-prompt-note rule and the tone section are copied in both)
- `skills-projects [CURRENT]/skills/<name>/SKILL.md` ↔ `skills-projects [CURRENT]/skills/<name>/README.md` (triggers, inputs, output format, dependencies)
- `.claude/commands/command.md` ↔ `Refrence-command.md` (actions, parameters, stops, examples)

## Library conventions

- **Layout:**
  - Skills: `skills-projects [CURRENT]/skills/<kebab-name>/`, flat: no category subfolders and no version in the name. Each holds `SKILL.md`, `README.md` and `CHANGELOG.md`, plus `references/`, `scripts/` and so on as needed.
  - Project instructions (for claude.ai Projects, Gems, custom GPTs): `skills-projects [CURRENT]/projects/<kebab-name>/`.
  - Retired skills and projects move, with plain `mv`, to `skills-projects [RETIRED]/skills/` or `skills-projects [RETIRED]/projects/`. They're kept for reference and not maintained.
  - Each of these folders keeps a short README.md, so it shows on GitHub even when empty.
- **Frontmatter:**
  - `name` matches the folder name.
  - `description` is trigger-rich: what the skill does, when to use it, and the phrases that should fire it.
  - The version goes in `metadata.version` as a quoted `"x.y"` string (quoted so `1.10` isn't read as `1.1`). Don't add a top-level `version:`: skill-creator's validator, and likely the claude.ai upload, accept only `name`, `description`, `license`, `allowed-tools`, `metadata` and `compatibility` at the top level.
- **Body:** under about 500 lines, with supporting files referenced by relative path.
- **Versioning:** minor bump for wording (`1.1` → `1.2`), major bump for behavior (`1.2` → `2.0`).
- **Categories** (metadata only, never folders): `education`, `career-planning`, `programming`, `other`. IDEAS.md, PROMPTS.md and the root README use them as headings.
- **Personal-info rule:** every committed file is fully generic. That means no name, school, employer, city, age or course codes, and no references to the owner's memory, Projects or past chats. Course or subject specifics go in a `## Configuration` block at the top of the SKILL.md body, with generic placeholders. Git history isn't rewritten.
- **Case-only renames:** git here runs with `core.ignorecase=true`, so a case-only rename done with `mv` is invisible to git. Tell the owner to record it with `git rm --cached <old>` and then `git add <new>`.

### Formats

IDEAS.md entry, under its category heading:

```markdown
### <kebab-name>

- type: skill | prompt
- status: idea | designed | built | needs-edit | done | retired
- description: <what it should do, in the owner's words>
- spec: <empty until designed>
- notes:
```

PROMPTS.md entry, under its category heading (the first entry replaces "No prompts yet."):

````markdown
### <kebab-name>

- version: x.y | works-in: claude-chat, claude-code, gemini, any
- use when: <one line>

```text
<the prompt, ready to paste>
```
````

CHANGELOG.md, newest entry first:

```markdown
# Changelog

## <x.y> — <YYYY-MM-DD>

- <what changed>
```

Skill README.md (copy the layout of `skills-projects [CURRENT]/skills/handoff/README.md`): a title and one-paragraph intro, a `Category | Version | Works in` table, then What it does, How it's triggered, Inputs, Output format and Dependencies. Last comes **How to use**, with three subsections:

- **Claude Code:** `mkdir -p ~/.claude/skills`, then `ln -s "$PWD/skills-projects [CURRENT]/skills/<name>" ~/.claude/skills/<name>`, plus the Windows junction alternative (`cmd /c mklink /J`, because PowerShell's `New-Item` misreads the `[ ]` in the path).
- **Claude chat:** zip the folder so the zip contains `<name>/SKILL.md` (leave out README.md and CHANGELOG.md), then upload it as a custom skill.
- **Other LLMs (Gemini, ChatGPT, plain prompt):** paste the SKILL.md body as custom instructions, a Gem, or a system prompt. List every Claude-only feature and what to do instead.

Root README.md Skills section: one table per category, with columns `Skill | What it does (≤15 words) | Works in | Version`. The skill name links to `<skills-projects [CURRENT]/skills/<name>/README.md>` (angle brackets, because the path has spaces), and an empty category reads "No skills yet."

## LIBRARY COMMANDS

- All library management runs through `/command` (`.claude/commands/command.md`). Its usage is in `Refrence-command.md`. The actions are `add`, `fix`, `remove`/`delete`, `retire` and `cleanup`.
- Outside a `/command` run, change IDEAS.md, `skills-projects [CURRENT]/`, `skills-projects [RETIRED]/` or PROMPTS.md only when the owner asks for that change directly. State a plan first and wait for approval.
- Adding a prompt or a project isn't a command. Do it when asked, using the Formats above, then run the SAFETY CHECK.
- `skill-creator` (user-level) defaults to `~/.claude/skills/`. Always point it at `skills-projects [CURRENT]/skills/<name>/` instead.

### SAFETY CHECK

Run it when the owner says "safety check <all | names>" (`all` means every `built` or `done` item), and as a step of `/command add` and `/command fix`. Never auto-fix.

The repo is public. Check the working tree only (not git history), and flag these in skills, prompts, scripts and docs:

1. **Personal identity:** the owner's name or nicknames, school, employer, city or age; email addresses, phone numbers, usernames.
2. **Secrets:** API keys, tokens, passwords, private URLs. Search for patterns such as `sk-`, `ghp_`, `AKIA`, `Bearer `, `api_key`, `password`, `secret`.
3. **Machine leaks:** absolute paths that contain usernames (`/Users/`, `C:\Users\`, `/home/`).
4. **Context leaks:** references to the owner's memory, Projects or past chats, or to courses and assignments by name.
5. **Unsafe behavior:**
   - scripts that make network calls, run shell commands built from model input, or delete files
   - instructions that tell the model to ignore other instructions or skip confirmation
6. **Portability:** a Claude-only tool, skill or feature with no plain-prompt fallback.
7. **Quality:**
   - dependencies missing from the README
   - a trigger description too vague to fire
   - redundant or contradictory instructions

Output a table with these columns, then ask which numbers to apply:

`# | Item | File:line | Check (1–7) | Severity (high/med/low) | Finding | Proposed fix`
