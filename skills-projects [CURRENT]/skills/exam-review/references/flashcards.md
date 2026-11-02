# Mode: FLASHCARDS

This is the user's locked flashcard spec. When he says anything like "make a
flashcard set," "min 80 slide flashcard set for quizlet," or "do the same for
chapter N," build exactly this — same structure every time, no re-asking.

## Output — one Quizlet file per chapter

- **One `.txt` file per chapter**, saved to `/mnt/user-data/outputs/` and
  presented with `present_files`. Multiple chapters = multiple files, never one
  combined file. Name: `ch<NN>_<course>_quizlet.txt` (e.g.
  `ch01_is265_quizlet.txt`).
- Format: **term, TAB, definition, one card per line.** No header row.
- **No newlines and no tabs inside a card.** Quizlet splits on them, so a
  multiline question silently fractures into broken cards. Multiple-choice
  options go inline on one line.
- After presenting, give the import settings in one line:
  **Between term and definition: Tab. Between rows: New line.**
- Do not paste the full set into chat — at 80+ cards it buries the response.
  The file is the deliverable.
- Anki `.csv` only if he asks for Anki. Then: `#separator:comma` first line,
  no header, RFC 4180 quoting.

## Size

- **Minimum 80 cards per chapter** unless he names a different number. 80 is
  a floor, not a target — go over if the chapter supports it.
- Reach the floor with more MC / T/F / scenario cards **on real chapter
  content**, never invented content. If the source genuinely can't support 80
  without fabricating, say so, state the count you can honestly build, and
  build that.
- State the final count per file in the response.

## Card mix (per chapter, approximate)

| Type | Share | Why it's in the set |
| --- | --- | --- |
| Definitions | ~35% | The exam expects near-verbatim recall of course terms |
| Multiple choice | ~25% | Mirrors the exam format; trains picking the right term out of close distractors |
| True/False | ~20% | Catches the half-understood version — the statement that's almost right |
| Scenario / "which one failed?" | ~10% | Tests applying a term to a situation, which is where he loses points |
| List-the-set + compare cards | ~10% | Exams ask for the whole category, and for the difference between neighbors |

Order the file **by topic**, not by type — all of a topic's cards together,
definitions first, then MC, T/F, scenario. Studying one concept at a time
beats shuffling types before he knows the terms (Quizlet can shuffle later).

## Card formats — exact

- **Definition:** `Accuracy` → `Intrinsic dimension: information is correct and free of errors. Ex: a thermometer reading 72°F when it's actually 91°F fails accuracy.`
  Course wording first, then a one-line example.
- **Multiple choice:** `MC: Which dimension is intrinsic? A) Timeliness B) Accuracy C) Relevance D) Completeness` → `B) Accuracy — judged on the info itself, no task needed. The other three depend on the task (contextual).`
  4 options, one correct, distractors pulled from the same chapter so they're
  genuinely close. Answer names the letter, the term, and **why the best
  distractor is wrong**.
- **True/False:** `T/F: Timeliness is an intrinsic dimension of information quality.` → `False — timeliness is contextual; how fresh is fresh enough depends on the task.`
  Roughly half true, half false. Every answer gets a one-line reason.
- **Scenario:** `Scenario: A report is accurate but three weeks old for a daily decision. Which dimension fails?` → `Timeliness (contextual) — the info is correct, just wrong for this task's time window.`
- **List-the-set:** `List the intrinsic dimensions (course version).` → full list in one card. Per the card rule below, a set he must recite is one card, not one per item.
- **Compare:** `Intrinsic vs. contextual — how do you tell them apart?` → `Intrinsic: judged on the info alone. Contextual: depends on the task. Test: would it be bad for everyone, or only for this job?`

## Required breakdowns — when he names a taxonomy, decompose it fully

If his request names a category structure (e.g. "info quality dimensions =
intrinsic + contextual, intrinsic = accurate, believable, objective, …"), that
structure is **mandatory coverage**, and each level gets its own cards:

1. **Parent** — definition + list-the-set card (e.g. "Info quality dimensions").
2. **Each branch** — definition, list-the-set card, compare card against the
   sibling branch.
3. **Each leaf** — definition in course wording, one concrete example, at
   least one MC or T/F that tests which branch it belongs to, and one
   scenario card where it's the thing that failed.

**His named structure beats general knowledge.** If he or the course puts a
term in a different branch than the textbook-standard model (e.g. Wang &
Strong), use his/the course's placement — that's what's graded — and flag the
difference once in the response, not in the cards.

## Card-writing rules

- Definitions in the **course's wording** wherever the exam expects
  near-verbatim recall.
- **One idea per card** — except a set he must list, which is one card asking
  for the whole set, because the exam asks for the set.
- Quantitative material gets **two-directional formula cards**: formula → what
  it computes, and what it computes → formula.
- Every answer fits in ~2 lines. If it doesn't, it's an explanation, not a
  card — split it or cut it.
- No duplicate cards. Variants that test the same fact from a different angle
  (MC vs. T/F vs. scenario) are fine; the same question twice is padding.

## Before generating

Only ask if the chapter source is missing. Otherwise build immediately —
this spec answers the format questions.
