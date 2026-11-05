# slide-breakdown

Turns course material (pasted text or a screenshot) into a full study breakdown with the same structure every time, whatever the subject: frame the set, plain explanation, five worked items per topic, a comparison table, exam predictions and traps.

| Category | Version | Works in |
|---|---|---|
| education | 1.1 | Claude chat, Claude Code, Gemini, any |

## What it does

1. **Scope check.** 1 to 4 topics get full treatment. With 5 or more, it frames the whole set, gives every term a one-line orientation, and takes the 3 or 4 that matter most (by exam weight and how easily they're confused).
2. **Image restatement.** For screenshots, it first restates what it read (terms, table, formula, numbers) so a misread gets caught early.
3. **Frame the set**, flagging where the course's definitions differ from the standard academic version, because the exam grades the course's version.
4. **Plain explanation** of each topic, before any analogy.
5. **Five items per topic:** three analogies from different domains, then two worked examples (numeric for quantitative material, applied scenarios for conceptual material).
6. **Compare-and-contrast table** covering every term in the input, with a diagnostic column.
7. **Master diagnostic question** that separates the whole set.
8. **Likely on the exam:** question forms, quizzable phrases, and which formulas are given versus memorized.
9. **Traps and how to dodge them**, worst confusion first.
10. **Gap-log block**, only when an exchange revealed a real miss.

It works closed-world: everything comes from the course material or the message. It says when it falls back to general knowledge, and it flags (but still teaches) course material that's wrong.

## How it's triggered

Pasting or screenshotting class content (slides, textbook tables, definitions, formulas, lecture notes), even with no instruction or just "explain this", "next", "break this down" or "what is this". Also "what's the difference between X and Y" when X and Y are course terms being learned.

Not for quizzing or review; that's [exam-review](../exam-review/README.md).

## Inputs

- Course material: pasted text or images.
- Optional: a per-class claude.ai Project with chapter decks, examples of the course's exams, and `gaps.md`. The skill reads these before using general knowledge.

## Output format

Fixed sections, in this order: frame the set → for each topic, a plain explanation and five numbered items → comparison table with a diagnostic column → master diagnostic question → "Likely on the exam" → "Traps", led by "The one your exam will try to trip you on: X vs. Y." Key phrases are in bold. When an exchange revealed a miss, it ends with one block to copy into `gaps.md`:

````text
```gaps
<chapter> | <topic> — <what the confusion was>
```
````

SKILL.md includes a short example of the output shape (primary key vs. foreign key).

## Dependencies

- None required. Optional: a claude.ai Project per class with the course files and `gaps.md`.
- Paired skill: [exam-review](../exam-review/README.md). Quizzing and review go there, exam-review's POST-EXAM mode checks this skill's "Likely on the exam" predictions, and the two skills share the tone and no-prompt-note rules (edit both together).

## How to use

### Claude Code

From the repo root:

```bash
mkdir -p ~/.claude/skills
ln -s "$PWD/skills-projects [CURRENT]/skills/slide-breakdown" ~/.claude/skills/slide-breakdown
```

On Windows, Git Bash's `ln -s` copies the folder instead of linking it (unless native symlinks are turned on), so later edits won't reach Claude Code. Use a junction from PowerShell instead, also from the repo root (`mklink` is used because PowerShell's `New-Item` misreads the `[ ]` in the path):

```powershell
New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
cmd /c mklink /J "$HOME\.claude\skills\slide-breakdown" "$PWD\skills-projects [CURRENT]\skills\slide-breakdown"
```

For screenshots, give Claude Code the image's file path.

### Claude chat

Zip the folder so the zip contains `slide-breakdown/SKILL.md`. README.md and CHANGELOG.md are for people, so leave them out. From the repo's `skills-projects [CURRENT]/skills/` folder:

```bash
# macOS / Linux
zip -r slide-breakdown.zip slide-breakdown -x "slide-breakdown/README.md" "slide-breakdown/CHANGELOG.md"
```

```powershell
# Windows
tar -a -cf slide-breakdown.zip --exclude=README.md --exclude=CHANGELOG.md slide-breakdown
```

Upload the zip as a custom skill in Claude's settings (skills need code execution and file creation turned on). It works best inside a per-class Project holding the course decks and `gaps.md`.

### Other LLMs (Gemini, ChatGPT, plain prompt)

Paste the SKILL.md body (everything after the closing `---` of the frontmatter) as custom instructions, a Gem, or a system prompt, then paste course material. Screenshots work in models that accept images; otherwise paste the text.

| Claude-only feature | What to do instead |
|---|---|
| Per-class Project knowledge (decks, exam examples) | Add them as Gem or GPT knowledge files, or paste the material with your message |
| `gaps.md` in the Project | Keep it as a knowledge file, and add new gap blocks to it yourself |
| Routing to the `exam-review` skill | Use exam-review in a separate chat, or put both SKILL.md bodies in one Gem |
