# Mode: POST-EXAM

Triggered when he pastes or describes a graded, returned exam. This is the
highest-signal data the whole system ever gets — a real instrument, scored by
the person who writes the questions. Everything else in this skill is a proxy
for it. Treat it accordingly.

## Procedure

1. **Take the exam apart before commenting on the score.** Per wrong answer:
   what the question actually tested, what he answered, and which of these it
   was:
   - **Content gap** — didn't know it.
   - **Boundary error** — knew both concepts, picked the wrong one. The most
     common failure and the one practice fixes fastest.
   - **Reading error** — knew it, misread the question or the qualifier.
   - **Execution error** — right method, arithmetic or transcription slip.
   - **Format surprise** — knew the material, wasn't ready for the question
     form.

   These four need completely different responses. Lumping them into "review
   this topic" wastes the exam.

2. **Check the prediction.** Compare the real exam against what
   `slide-breakdown` predicted under "Likely on the exam" and against
   `references/practice-exam.md`'s format mix. Say plainly where the
   prediction was wrong — question forms that showed up unpredicted, weighting
   that was off, topics that carried more than expected.

3. **Update the course's exam-structure notes.** Write out the corrected
   format description — question counts by type, weighting, time, what was
   given versus memorized — as a block he can paste into the Project's
   exam-structure file. Next exam's practice is only as good as this.

4. **Rewrite the gap log**, in one block:
   - `+` lines for confirmed gaps, tagged by chapter.
   - `-` lines for everything in the log this exam proved solid.
   - An `## Archive` move for everything belonging to the chapters this exam
     covered: resolved or not, it leaves the active list. It has been tested;
     carrying it forward buries the next unit's real gaps under old noise.
     Archived lines stay in the file, below the archive header, and every
     other mode ignores them.

5. **One paragraph on what to change for the next exam** — study method, not
   content. If the pattern is boundary errors, more reading won't help and
   more RECALL will. If it's format surprise, the fix is PRACTICE EXAM. Name
   the mode.

## Do not

- Do not open with reassurance about the grade. Open with the breakdown.
- Do not re-teach the missed material here. That's `slide-breakdown` on the
  specific topic, and say so in one line at the end.
