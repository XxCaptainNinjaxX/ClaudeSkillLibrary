# Mode: PLAN

Scopes the material, sets the time budget, and keeps the master plan current
across the session. Other modes run inside it.

## 1. Build the plan — STOP at the end

1. **Assess what's needed.** Exam date and time, what it covers (syllabus,
   study guide, or what the user says), and the user's hours available per day. Missing
   exam date or coverage → ask and STOP. Never guess either one.
2. **List the sections** to cover, in the course's order. One section is
   one chapter or topic unit. Map study-guide questions to sections when a
   study guide exists.
3. **Estimate TTF per section** from its size and difficulty. Say they are
   estimates.
4. **Group the sections into blocks.** A block is one large concept, such as
   all the derivative rules, or 3–5 small sections. Decide the grouping now
   from the material and state it.
5. **Lay out the test cadence:**
   - Every section ends with a **section quiz** of 3–5 questions.
   - Every block ends with a **block midterm**. It is a mixed set with at
     least two questions that combine sections, and it covers the sections
     since the last midterm.
     Example: 10 sections → quizzes 1–10, midterm A (1–5), midterm B (6–10).
   - After the last block midterm, ask whether the user wants to deep-dive a
     weak section or go to the **mock** first, and STOP. The mock covers
     everything and runs as PRACTICE EXAM.
   - The source of each quiz or midterm is either generated from course
     material or the course's own study guide or practice exam. Mark which
     one in the plan.
6. **Lay out a per-day schedule** from today to the exam.
7. **Other classes:** if the user has mentioned any, add the cross-class table,
   with "?" wherever the user hasn't given a number.
8. Output the plan using the master overview format below, then STOP and
   wait for approval or edits.

## 2. Timing

- Log each section's start and end time with the current-time tool. If that
  tool is unavailable, use message timestamps, or ask the user.
- Actual time = end − start. Pace = actual ÷ projected.
- After every section, re-project the remaining TTF using pace so far.

## 3. At every section change — fixed order, every time

1. **Section recap** — a table, then two lines:

| Part | Actual | Projected | Status |
|---|---|---|---|
| S1: <name> | 55m | 30m | ✅ |
| Quiz / midterm | 30m | 20m | ✅ 10/11 (<what was missed and why>) |
| **Total** | **<sum>** | **<sum>** | **<pace>× pace** |

**What stuck:** one line.
**What to watch:** one line.

2. **---** then the master overview:

## 📊 Master overview: <Course> <Exam>
**Exam: <day date, time>. Time left: <days + hours>.**

### Progress
| # | Block | Status | Actual | TTF |
|---|---|---|---|---|
| A | **<Block>** (S1–3) | ✅ | 2.5h | 0 |
| | Block midterm A | ✅ | 30m | 0 |
| B | **<Block>** (S4) | 🟡 starting | 3m | 1.6h |
| | Block midterm B | ⬜ | — | 20m |
| C | **Mock** (everything) | ⬜ | — | 1.5h |
| | **Total** | **~X% done** | **<sum>** | **<sum>** |

- **Projected total** vs. budget, and what changed it.
- **Midterms left:** N block midterms + mock.
- **Coverage:** X of Y study-guide questions touched (only if a guide exists).

### Plan per day
| Day | Block | Hours |
|---|---|---|

### Cross-class (only if the user has mentioned other classes)
| Class | Needed | Spent | TTF |
|---|---|---|---|

⚠️ **<Class>:** warn whenever one class's TTF ÷ days left exceeds the user's daily
hours, or this class runs more than 1.25× over its projection. Give the
hours per day the lagging class now needs. Ask for spent hours you don't
have.

Status emojis: ✅ done · 🟡 in progress · ⬜ not started. Only these.

3. **---** then start the next section, or its quiz.

## Rules

- No grade inflation in the recap. A missed question is a miss.
- Re-plan out loud when pace or scope changes. Don't let the plan drift
  silently.
- Still end with the gap block per SKILL.md.
