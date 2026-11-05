# exam-review

Runs structured study review sessions for a course. It picks one of six modes from what you ask, reads only that mode's reference file, and runs it as a multi-turn graded session with a fixed format.

| Category | Version | Works in |
|---|---|---|
| education | 2.2 | Claude chat, Claude Code, Gemini, any |

## What it does

| Mode | Use it for | Reference |
|---|---|---|
| DIAGNOSE (default) | Find what you don't know: probing questions in small batches, gaps ranked by exam cost, a specific study prescription and an honest readiness read | [references/diagnose.md](references/diagnose.md) |
| RECALL | Active recall: one question per message, graded, with the full answer every time; misses come back later in new wording | [references/recall.md](references/recall.md) |
| PRACTICE EXAM | A full practice exam (default 20 questions) matched to the course's real exam format; no answer key until you submit; per-topic scores | [references/practice-exam.md](references/practice-exam.md) |
| FLASHCARDS | One Quizlet import file per chapter (minimum 80 cards, fixed mix of card types); Anki CSV on request | [references/flashcards.md](references/flashcards.md) |
| CHEAT SHEET | A dense last-pass overview: map, term bank by section, formulas, distinctions table, logged weak spots | [references/cheat-sheet.md](references/cheat-sheet.md) |
| POST-EXAM | Takes a graded exam apart by error type, checks earlier predictions, and rewrites the gap log | [references/post-exam.md](references/post-exam.md) |

It teaches and tests the course's version of the material (flagging errors in it rather than silently fixing them), never invents course content to fill a question count, and doesn't inflate grades.

**Known issue:** SKILL.md's description and intro say "five modes" but define six. The description doesn't mention POST-EXAM, so that mode may need an explicit request, such as "here's how I did on the exam".

## How it's triggered

Requests to be quizzed, tested or reviewed: "quiz me", "test me", "review chapter X", "what should I study", "where am I weak", "am I ready", asking for flashcards, a practice test or a cheat sheet, or mentioning an upcoming exam. Pasting a graded exam ("here's how I did", "I got X back") selects POST-EXAM. An ambiguous request defaults to DIAGNOSE.

Not for explaining new material; that goes to [slide-breakdown](../slide-breakdown/README.md).

## Inputs

- Your request: the mode, the chapter or topic, and optionally a question count.
- Course material, in priority order: the class Project's knowledge files (chapter decks, examples of the course's exams, syllabus, textbook), then `gaps.md`, then the conversation. General subject knowledge comes last, and the skill says when it uses it.
- Optional `gaps.md`: a running log of confusions, kept by hand.
- For POST-EXAM: the graded exam, pasted or described.

## Output format

- Every mode that surfaces or resolves a gap ends with one copy-paste block for `gaps.md`:

  ````text
  ```gaps
  + <chapter> | <topic> — <what the confusion was>
  - <chapter> | <topic> — <resolved this session>
  ```
  ````

- FLASHCARDS: one `.txt` file per chapter, named `ch<NN>_<course>_quizlet.txt`, one card per line as `term<TAB>definition`, no header row. The reply states the card count and the Quizlet import settings (Tab between term and definition, new line between rows).
- PRACTICE EXAM: questions first; answers, explanations and per-topic scores only after you submit.
- POST-EXAM: an error type for each wrong answer (content gap, boundary, reading, execution, format surprise), a corrected exam-structure block to paste into the Project, and a gap-log rewrite with an `## Archive` section.
- Tone: casual and blunt, key phrases in bold, no filler.

## Dependencies

- None required.
- Optional: a claude.ai Project per class holding the course files and `gaps.md`. Without one, it works from the conversation.
- FLASHCARDS saves to `/mnt/user-data/outputs/` and presents the file with `present_files`, which only exist in Claude chat.
- Paired skill: [slide-breakdown](../slide-breakdown/README.md). New material is routed there, POST-EXAM checks slide-breakdown's "Likely on the exam" predictions, and the two skills share the tone and no-prompt-note rules (edit both together).

## How to use

### Claude Code

From the repo root:

```bash
mkdir -p ~/.claude/skills
ln -s "$PWD/skills-projects [CURRENT]/skills/exam-review" ~/.claude/skills/exam-review
```

On Windows, Git Bash's `ln -s` copies the folder instead of linking it (unless native symlinks are turned on), so later edits won't reach Claude Code. Use a junction from PowerShell instead, also from the repo root (`mklink` is used because PowerShell's `New-Item` misreads the `[ ]` in the path):

```powershell
New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
cmd /c mklink /J "$HOME\.claude\skills\exam-review" "$PWD\skills-projects [CURRENT]\skills\exam-review"
```

Claude Code has no Project and no `/mnt/user-data/outputs/`. Keep the course files and `gaps.md` in your working folder and point the skill at them, and ask for flashcard files in the working directory.

### Claude chat

Zip the folder so the zip contains `exam-review/SKILL.md`. README.md and CHANGELOG.md are for people, so leave them out. From the repo's `skills-projects [CURRENT]/skills/` folder:

```bash
# macOS / Linux
zip -r exam-review.zip exam-review -x "exam-review/README.md" "exam-review/CHANGELOG.md"
```

```powershell
# Windows
tar -a -cf exam-review.zip --exclude=README.md --exclude=CHANGELOG.md exam-review
```

Upload the zip as a custom skill in Claude's settings (skills need code execution and file creation turned on). It works best inside a per-class Project with the course files and `gaps.md` as knowledge.

### Other LLMs (Gemini, ChatGPT, plain prompt)

Paste the SKILL.md body (everything after the closing `---` of the frontmatter) as custom instructions, a Gem, or a system prompt. **Also** add the six `references/*.md` files as knowledge files (Gem or custom GPT), or paste them after the body: SKILL.md tells the model to read the mode's file before running it.

| Claude-only feature | What to do instead |
|---|---|
| Project knowledge files | Add the course files as Gem or GPT knowledge, or paste the material into the chat |
| `gaps.md` in the Project | Keep it as a knowledge file, or paste it at the start of a session |
| Saving flashcards to `/mnt/user-data/outputs/` with `present_files` | Ask for each chapter's cards in a code block and save them as a `.txt` file yourself |
| Routing to the `slide-breakdown` skill | Put slide-breakdown's SKILL.md body in the same Gem, or use it in a separate chat |
