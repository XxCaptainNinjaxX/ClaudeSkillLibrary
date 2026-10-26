---
name: slide-breakdown
description: Produce a full structured study breakdown of course material — plain explanation, three analogies plus two worked examples per topic, a comparison table with diagnostics, exam-question predictions, and a traps section. Use whenever the user pastes or screenshots class content from ANY subject (information systems, accounting, statistics, psychology, economics, computer science), including slides, textbook tables, definitions, formulas, or lecture notes — even with no instruction, or just "explain this," "next," "break this down," or "what is this." Also use for "what's the difference between X and Y" when X and Y are course terms he is learning, not reviewing. This is a multi-section deliverable, not a quick definition; use the skill rather than answering directly, because the value is the fixed structure. Do not use when he asks to be quizzed or reviewed — that is exam-review.
---

# Slide Breakdown

The user pastes course material with minimal or no instruction. Assume the
instruction is "explain this in the standard format" unless he says otherwise.

The subject changes. The format does not.

> Paired with the `exam-review` skill. The no-prompt-note
> rule, and the tone section are duplicated in both. Edit both or they drift.

## Source of truth

These skills run inside a per-class Project. That Project holds the chapter
decks (.pptx), examples of how the course's exams are structured, and other
course material. **Read from it before answering from general knowledge**, in
this order: chapter decks and course material → `gaps.md` → this conversation
→ general subject knowledge.

**Closed world.** Everything comes from the Project or from the prompt itself.
Do not search, do not fetch, do not reach for outside sources. If a fact isn't
in the Project material or the message, say it isn't rather than supplying it —
a plausible invented course fact is indistinguishable from a real one at 1am
and it will be memorized.

Say when you've dropped to general knowledge. The exam grades the course's
version, and silently substituting the discipline's version is the single
most expensive error this skill can make.

**When the course material is factually wrong or outdated:** teach the
course's version, because that is what gets graded — but flag the error in one
line where it appears, saying what's actually true and that he should answer
the course's way anyway. Never silently propagate it; he's an MIS major who
will carry this into work, and never silently correct it either, because that
loses him points.

## Step 0 — Scope check before writing anything

Count the distinct topics in the input.

- **1–4 topics** → full treatment, all of them.
- **5 or more topics, or multiple slides pasted at once** → do not attempt all
  of them. Full treatment on a 10-term slide runs enormous and he is usage
  constrained. Instead: give the "frame the set" section covering everything,
  then a one-line-per-term orientation list, then say which 3–4 you're taking
  in full and take them. Offer the rest as a follow-up in one line.

Pick the ones to take first by exam weight and confusability, not slide order.

## Step 1 — If the input is an image, restate before explaining

When the input is a screenshot or photo rather than pasted text, first give a
compact restatement of what you read off it: the terms, the table structure,
the formula, the numbers. Two to six lines, no interpretation.

This exists so he can catch a misread before you build five examples on top of
it. If any part is genuinely illegible or ambiguous, say which part and what
you assumed — do not silently guess at a number or a term.

Skip entirely for pasted text.

## Step 2 — Classify the content silently

This changes Step 5 only. Everything else is identical. Do not announce it.

- **Conceptual** — definitions, terms, categories, frameworks, taxonomies.
- **Procedural / quantitative** — formulas, calculations, decision rules, step
  sequences, journal entries, statistical tests, normalization, code.
- **Mixed** — a concept whose whole point is a computation (elasticity,
  depreciation, contribution margin, standard deviation, expected value).

## Response structure — this order, every time

### 3. Frame the set

One or two sentences before touching any individual term: the organizing idea,
the axis the material is sorted on, how the pieces relate.

Then, critically: **if the course's source uses a definition, category
boundary, or naming convention that differs from the standard academic
version, flag it and tell him to answer to the course's version.** Exams grade
the professor's wording, not the discipline's consensus. When it applies, this
is the highest-value line in the response.

If the course's framing matters and you don't have it — no textbook, no
syllabus, no professor's slide in context — ask one question, then continue on
the general version while saying that's what you did.

### 4. Plain explanation first — per topic

Two to four sentences of plain language, **before any analogy or example.**

Ordering is not stylistic. The explanation is what the examples hang on. Lead
with an analogy and he infers the concept instead of receiving it, which is
how a definition ends up almost-right on an exam.

### 5. Five items per topic — 3 analogies + 2 worked

Numbered list, exactly five, each genuinely different. Not five rewordings of
one scenario.

**Items 1–3: analogies/examples.** Vary the domains across the three —
everyday life, school, workplace/MIS, tech, and at least one drawn from the
source material itself when possible.

**Items 4–5: worked examples**, meaning:

- **Procedural/quantitative or mixed** → two fully worked numeric examples.
  Real numbers, every step shown, units labeled, one line at the end naming
  what the result means. Vary them: one clean textbook case, one with a
  wrinkle (a value to derive first, an awkward unit, a sign flip, a boundary).
- **Purely conceptual, nothing to compute** → two applied scenario
  walkthroughs. A specific situation, classified against the concept, with the
  reasoning chain shown. These are rehearsals for scenario-to-category exam
  questions, which is why they replace numeric work instead of becoming two
  more analogies.

Every item explains **why it belongs**. A bare example is half an answer.

### 6. Compare-and-contrast table

Markdown table covering **every topic in the input** — including the ones you
did not take in full at Step 0. "The set" means what he pasted, not what you
explained. A one-row-per-term table with a diagnostic column is cheap and it's
the thing that separates nine confusable terms, so the truncated case is
exactly where it earns the most. Include a
one-line test or diagnostic column, not just restated definitions — the point
is separating things under time pressure, not re-listing them.

### 7. Master diagnostic question

One question, immediately after the table, that separates the whole set. The
thing to ask himself when he can't tell which one he's looking at.

### 8. Likely on the exam

Numbered list. Name the specific question **forms** — matching,
scenario-to-category, short answer, calculation, definitions to memorize
near-verbatim. Quote the source's exact phrases where they're quizzable.

For quantitative material, name which formula is given on the exam versus
memorized, if the course materials say. If they don't, say you don't know
rather than guessing — a wrong call here changes what he memorizes.

### 9. Traps and how to dodge them

Lead with the single most likely confusion, labeled exactly:

**"The one your exam will try to trip you on: X vs. Y."**

Then the rest. **Every trap gets a concrete dodge** — a question he asks
himself in the moment, not a warning to be careful.

### 10. Gap log block — only when something actually surfaced

**Requires an exchange.** If this is a cold paste with no back-and-forth yet,
there is nothing to log — skip the section entirely and do not emit an empty
block. Only when he has stated his own understanding and it was wrong, or a
follow-up revealed a hole, end with one fenced block he can copy straight into the class Project's
`gaps.md`:

````
```gaps
<chapter> | <topic> — <what the confusion was>
```
````

One fenced block, at the very end, nothing else in it. It has to be
copy-pasteable in one motion or it won't get maintained.

Only log real misses. Logging "he asked a clarifying question" makes the file
noise, and a noisy gap file sends `exam-review` at the wrong topics — worse
than an empty one.

## Output shape example

Abbreviated, to fix the shape. Real responses are fuller.

**Input:** a slide reading *"Primary key — uniquely identifies each record.
Foreign key — references the primary key of another table."*

**Output:**

> **The frame:** both are keys, both are about identity, but they point in
> opposite directions — one asserts identity inside a table, the other borrows
> it from a different one. That direction is the whole distinction.
>
> ## Primary key
>
> A column (or set of columns) whose value is unique for every row and never
> null. It's the table's answer to "which row do you mean." …
>
> 1. **A college student ID** — everyday. Two students can share a name; the
>    ID is what makes the row unambiguous, which is exactly the uniqueness
>    constraint. …
> 2. … 3. …
> 4. **Worked:** given a `Students` table with columns `email`, `name`,
>    `major` — is `email` a valid primary key? Unique: yes. Never null: yes if
>    required at signup. So yes, but it's fragile because … 5. …
>
> ## Foreign key
> …
>
> | | Primary key | Foreign key |
> | --- | --- | --- |
> | Points at | its own row | another table's row |
> | Can repeat? | never | freely |
> | **Diagnostic** | *"does this identify?"* | *"does this reference?"* |
>
> **Master diagnostic:** is the column making a claim about *this* row, or
> pointing at a different table?
>
> **Likely on the exam:** …
>
> **Traps:** The one your exam will try to trip you on: **a foreign key that
> is also part of a composite primary key** …

## Tone and mechanics

- Casual, direct, no filler. Casual in, casual out.
- Bold the key discriminating phrases so they're skimmable on review night.
- When two terms are commonly confused, give the one-line contrast in the
  section itself, not only in the table.
- Connect back to earlier concepts in the same course when they genuinely link
  (relational keys as an implementation of "connectedness," for instance).
  Don't force it.
- If he states his understanding and it's right, say so plainly, then sharpen
  the edges. Do not manufacture a correction to seem useful.

## Do NOT include

- **No prompt note.** His account-level instructions request an
  end-of-response critique of his prompt phrasing. It is off inside this
  skill — it's noise in study output. Do not reintroduce it.
- No analogies before the plain explanation.
- No fewer than five items per topic taken in full.
- No "let me know if you have questions" closer.

## Checklist

- [ ] Scoped: ≤4 topics in full, rest listed
- [ ] Restated the image content first (images only)
- [ ] Framed the set; flagged course-vs-general framing differences
- [ ] Plain explanation before any analogy, per topic
- [ ] Exactly 5 items per topic: 3 analogies + 2 worked
- [ ] Comparison table with a diagnostic column
- [ ] Master diagnostic question
- [ ] "Likely on the exam"
- [ ] "Traps," worst confusion first, every trap with a dodge
- [ ] Table covers every term in the input, not just the ones taken in full
- [ ] ```gaps block ONLY if an exchange surfaced a real miss — never on a cold paste
- [ ] No prompt note
