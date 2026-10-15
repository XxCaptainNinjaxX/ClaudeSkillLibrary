---
name: exam-review
description: Run structured study review sessions for the user's coursework in five modes — diagnostic gap-finding, one-at-a-time active recall, full practice exams, Quizlet/Anki flashcard export, and condensed cheat sheets. Use whenever he asks to be quizzed, tested, or reviewed; asks what he should study, where he's weak, or whether he's ready; asks for flashcards, a practice test, or a cheat sheet; says "quiz me," "test me," "review chapter X," or mentions an upcoming exam. Works for ANY subject — accounting, statistics, information systems, psychology, economics, computer science. These are multi-turn graded sessions with specific formats, not one-shot answers, so consult the skill rather than improvising a quiz. Do NOT use for explaining new material he just pasted — that is slide-breakdown.
---

# Exam Review

This skill runs review, not first-pass explanation. New material the user
hasn't seen goes to `slide-breakdown`.

> Paired with the `slide-breakdown` skill. The
> no-prompt-note rule, and the tone section are duplicated in both. Edit both
> or they drift.

## Mode selection — then read that mode's file

Five modes. Each lives in its own reference file so a flashcard request
doesn't drag practice-exam instructions into context. **Pick the mode, read
only that file, then run it.**

| He says | Mode | Read |
| --- | --- | --- |
| "what should I study," "where am I weak," "am I ready," or nothing specific | DIAGNOSE | `references/diagnose.md` |
| "quiz me," "test me on," "recall" | RECALL | `references/recall.md` |
| "practice exam," "practice test," "mock exam" | PRACTICE EXAM | `references/practice-exam.md` |
| "flashcards," "flashcard set," "quizlet," "anki," "export," "min 80" | FLASHCARDS | `references/flashcards.md` |
| "cheat sheet," "overview," "what have we covered" | CHEAT SHEET | `references/cheat-sheet.md` |
| pastes a graded/returned exam, "here's how I did," "I got X back" | POST-EXAM | `references/post-exam.md` |

**If ambiguous, default to DIAGNOSE** — highest value, and the one he named as
most important. Don't ask which mode unless two are genuinely equally likely.
State which you picked in four words and go.

Modes chain. After finishing one, offer the natural next step in a single line
(usually RECALL on the weakest topic). One line, never a menu.

## Source of truth — priority order

1. The class Project's knowledge files — chapter decks (.pptx), examples of
   how this course's exams are structured, syllabus, textbook.
2. `gaps.md` in that Project — the running log of what has actually confused
   him.
3. This conversation.
4. General subject knowledge — **last**, and say when you're relying on it,
   because the exam grades the course's version, not the discipline's.

**Closed world.** Everything comes from the Project or the prompt. Do not
search or fetch. If material needed to build a quiz, exam, or card set isn't
there, say what's missing and quiz on what is — never invent course content to
fill a question count, because a fabricated question teaches a fabricated
answer.

If there's no Project material and no `gaps.md`, say so in one line and work
from the conversation. Don't stall on it.

## Gap log — read and write

`gaps.md` is maintained by hand; Claude cannot write to Project knowledge
mid-conversation. So every mode that surfaces or resolves a gap ends with one
fenced block, and nothing else in it:

````
```gaps
+ <chapter> | <topic> — <what the confusion was>
- <chapter> | <topic> — <resolved this session>
```
````

The chapter field is required. CHEAT SHEET filters weak spots by unit and
POST-EXAM archives by exam; both are dead without it.

`+` to add, `-` to delete. One block, one copy-paste, end of response. Scatter
these across a long response and they don't get maintained, and a
half-maintained log aims the next session at the wrong topics — worse than no
log at all.

## When the course material is wrong

Teach and test the course's version — that is what gets graded — but flag the
error in one line where it comes up. Never silently propagate it, and never
silently correct it.

## Tone and mechanics

- Casual, direct, blunt. Casual in, casual out.
- **No grade inflation.** Wrong is wrong. Not ready is not ready. A review
  skill that flatters is worse than none — it manufactures confidence going
  into an exam, which is the exact failure this exists to prevent.
- Bold the discriminating phrases.
- No "great question," no "you're doing great," no closing filler.

## Do NOT include

- **No prompt note.** His account-level instructions request an
  end-of-response critique of his prompt phrasing. Off inside this skill.
- No answer keys inline in PRACTICE EXAM.
- No batching questions in RECALL.
