# Claude Skill Library

A public, [MIT-licensed](LICENSE) library of AI skills, Project instructions and saved prompts. It's built and maintained in Claude Code, but everything here is written to be used anywhere: Claude chat, Claude Code, Gemini, ChatGPT, or pasted as a plain prompt. Each skill's README covers installing it on every surface and lists any Claude-only features.

## Layout

```text
skills-projects [CURRENT]/   maintained
  skills/                    one folder per skill
  projects/                  instructions for claude.ai Projects, Gems and custom GPTs
skills-projects [RETIRED]/   no longer maintained, kept for reference
  skills/
  projects/
PROMPTS.md                   saved prompts, by category
IDEAS.md                     to-do list and status of everything above
```

## Skills

### education

| Skill | What it does | Works in | Version |
|---|---|---|---|
| [exam-review](<skills-projects [CURRENT]/skills/exam-review/README.md>) | Six study-review modes: diagnosis, recall, practice exams, flashcards, cheat sheets, post-exam analysis. | Claude chat, Claude Code, Gemini, any | 2.0 |
| [slide-breakdown](<skills-projects [CURRENT]/skills/slide-breakdown/README.md>) | Turns pasted course material into a fixed-format breakdown with examples and exam traps. | Claude chat, Claude Code, Gemini, any | 1.0 |

### career-planning

No skills yet.

### programming

No skills yet.

### other

| Skill | What it does | Works in | Version |
|---|---|---|---|
| [council](<skills-projects [CURRENT]/skills/council/README.md>) | Independent Claude subagents debate a hard decision, peer-review each other, and deliver a verdict. | Claude chat (Claude Code ⚠️) | 1.1 |
| [handoff](<skills-projects [CURRENT]/skills/handoff/README.md>) | Compresses a chat into a handoff any new chat or model can continue from. | Claude chat, Claude Code, Gemini, any | 2.0 |
| [patch](<skills-projects [CURRENT]/skills/patch/README.md>) | Packages a misfiring claude.ai instruction into one report another chat can fix. | Claude chat | 1.0 |

## Projects

Instructions to paste into a claude.ai Project, a Gem, or a custom GPT. No projects yet; they'll go in [skills-projects [CURRENT]/projects/](<skills-projects [CURRENT]/projects/README.md>).

## Prompts

All saved prompts are in [PROMPTS.md](PROMPTS.md): [education](PROMPTS.md#education) · [career-planning](PROMPTS.md#career-planning) · [programming](PROMPTS.md#programming) · [other](PROMPTS.md#other).

## Retired

Nothing retired yet. Retired [skills](<skills-projects [RETIRED]/skills/README.md>) and [projects](<skills-projects [RETIRED]/projects/README.md>) are kept for reference but no longer maintained.

## Install

- **Claude Code:** symlink the skill folder into `~/.claude/skills/`; see the skill's README.
- **Claude chat:** zip the skill folder and upload it as a custom skill; see the skill's README.
- **Other LLMs:** paste the skill's SKILL.md body as custom instructions, a Gem, or a system prompt; see the skill's README for what doesn't carry over.
