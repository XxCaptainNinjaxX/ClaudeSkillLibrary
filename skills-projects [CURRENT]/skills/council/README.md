# council

A decision tool. It convenes a panel of independent Claude subagents ("seats") on a hard decision. Each seat answers blind, the seats peer-review each other anonymously and vote on every claim, a script tallies the votes, and the main session, as chairman, writes a verdict that keeps dissent visible.

| Category | Version | Works in |
|---|---|---|
| other | 1.1 | Claude chat (Claude Code ⚠️) |

This is the **claude.ai chat edition**, forked from [amgadelgamal/claude-council](https://github.com/amgadelgamal/claude-council) (MIT). It keeps its own [LICENSE](LICENSE) and [CREDITS.md](CREDITS.md).

## What it does

- Writes one neutral case file and sends it, unchanged, to every seat as a separate subagent.
- Default panel: six seats (Evidence, Pre-mortem, Upside, Reframer, Operator, Stakeholder), split across Opus and Sonnet so every core tension spans two models.
- **Round 1:** independent answers. **Round 2:** anonymous peer review and a vote on every claim. **Round 3** (optional): challenged seats defend, amend or withdraw their claims.
- `scripts/tally.py` gives each claim a status (Confirmed, Contested, Disputed, ...) and averages peer ranks. The chairman then makes the call.
- Never simulates seats in one context. If no subagent tool exists, it stops.

## How it's triggered

Only by an explicit request: `/council`, "council this", "ask the council" or "convene the council".

Optional flags right after the trigger, for that run only: `quick` (1 round, no peer review), `rounds=N` (N = 1 to 3), `default` (ignore any project config).

## Inputs

- The question. Best with the decision, the options and the constraints. If it's too thin to brief agents that start cold, the skill asks one clarifying question.
- Optional: a `COUNCIL CONFIG v1` block that extends, tweaks or replaces the panel, placed in a claude.ai Project's instructions or knowledge files, or pasted into the triggering message. Spec: [references/CONFIG-SPEC.md](references/CONFIG-SPEC.md). Examples: [references/examples/](references/examples/).

## Output format

```text
## Council verdict: <short title>
**Verdict:** <one to three sentences>
**Confidence:** <High|Medium|Low> - <reason> (seats: <n> high, <n> medium, <n> low)
| ID | Claim | Seat | Votes (agree/dispute/unsure) | Status |
**Strongest dissent worth weighing (<seat>):** <steelman>. Not adopted because <...>.
**Would flip the verdict:** <one or two signals>
**Next step:** <one concrete action>
Run record: config, seats and models, rounds, tally method, empty seats, peer favorite, chairman's prior
```

Quick runs replace the vote column with "Seats in agreement" and use the statuses Shared, Lone and Opposed.

## Dependencies

- **A subagent tool** (Agent) that can set the model per call. Seats default to `opus` and `sonnet`; `fable` only when a config sets `allow_fable: true`.
- **Code execution with Python 3** for `scripts/tally.py` (standard library only) and `scripts/validate_config.py`, which also needs **PyYAML** and exits with code 3 without it. Without Python, the skill tallies by hand.
- Optional: web search (used by the Evidence seat) and a claude.ai Project (to hold a saved config).
- Cost: one subagent call per seat per round. By default that's 6 seats × 2 rounds, and runs go up to 3 rounds.
- Developer scripts: `scripts/test_tally.py`, `scripts/test_validate_config.py` (needs PyYAML) and `scripts/check_editions.py`. The last one compares this edition with a Claude Code edition, which isn't in this library.

## How to use

### Claude Code

From the repo root:

```bash
mkdir -p ~/.claude/skills
ln -s "$PWD/skills-projects [CURRENT]/skills/council" ~/.claude/skills/council
```

On Windows, Git Bash's `ln -s` copies the folder instead of linking it (unless native symlinks are turned on), so later edits won't reach Claude Code. Use a junction from PowerShell instead, also from the repo root (`mklink` is used because PowerShell's `New-Item` misreads the `[ ]` in the path):

```powershell
New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
cmd /c mklink /J "$HOME\.claude\skills\council" "$PWD\skills-projects [CURRENT]\skills\council"
```

⚠️ VERIFY before relying on it in Claude Code. This is the chat edition. Its guard tells Claude Code to use a local skill named `council` instead, which in this setup is the same skill. It also finds its scripts with `find /`, which scans the whole disk on a local machine. SKILL.md refers to a separate Claude Code edition, which isn't in this library.

### Claude chat

Zip the folder so the zip contains `council/SKILL.md`. README.md and CHANGELOG.md are for people, so leave them out. From the repo's `skills-projects [CURRENT]/skills/` folder:

```bash
# macOS / Linux
zip -r council.zip council -x "council/README.md" "council/CHANGELOG.md"
```

```powershell
# Windows
tar -a -cf council.zip --exclude=README.md --exclude=CHANGELOG.md council
```

Upload the zip as a custom skill in Claude's settings. Council needs code execution and file creation turned on, and the Agent (subagent) tool available. To keep a saved `COUNCIL CONFIG v1`, put it in a Project's instructions.

### Other LLMs (Gemini, ChatGPT, plain prompt)

**Not supported.** Pasting the SKILL.md body won't give you a council. Without a subagent tool the skill stops at its guard ("Council not convened") by design, because independent seats can't be faked in one context. These Claude-only features have no substitute:

- Subagents with a model per seat (the core of the skill).
- Code execution for `tally.py` and `validate_config.py`. Section 6 of SKILL.md has by-hand tally rules, but they only matter once seats can run.
- claude.ai Project config lookup. A config block pasted into the message works the same way.

What you can do instead: ask for a plainly labelled single-perspective analysis. The guard allows that as long as it isn't called a council.
