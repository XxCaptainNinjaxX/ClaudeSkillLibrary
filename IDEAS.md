# Ideas and inventory

The to-do list and inventory for every skill, project and prompt in this library, and the record of their status. Status moves `idea` → `designed` → `built`; `needs-edit` marks something to rework, and `done` marks it finished.

## education

### exam-review
- type: skill
- status: built
- description: Run structured study review sessions for a course in seven modes: build a master study plan with time estimates, diagnose gaps, one-question-at-a-time recall, practice exams, Quizlet/Anki flashcards, cheat sheets, and post-exam analysis of a graded exam.
- spec: [exam-review/SKILL.md](<skills-projects [CURRENT]/skills/exam-review/SKILL.md>) (built before this workflow existed)
- notes: Open findings from the 2026-10-26 migration safety check, not yet applied: a reference to the owner's account-level instructions; a past-chat reference in mode selection; post-exam.md says "four" error types but lists five; flashcard saving has no fallback outside Claude chat. Open from the 2026-11-05 dump safety check: mode selection's "and go" contradicts the session plan's STOP; `TTF` is undefined in references/plan.md (the owner says it means "time to finish", not yet written in).

### IS265
- type: project
- status: built
- description: Course Project that routes pasted material to slide-breakdown and review requests to exam-review, and drafts graded work through a !homework command.
- spec: [IS265/Instructions+Commands.md](<skills-projects [CURRENT]/projects/IS265/Instructions+Commands.md>)
- notes:

### slide-breakdown
- type: skill
- status: built
- description: Turn pasted or screenshotted course material from any subject into a fixed-format study breakdown: plain explanation, three analogies and two worked examples per topic, comparison table, exam predictions, and traps.
- spec: [slide-breakdown/SKILL.md](<skills-projects [CURRENT]/skills/slide-breakdown/SKILL.md>) (built before this workflow existed)
- notes: Open findings from the 2026-10-26 migration safety check, not yet applied: a line naming the owner's field of study; a reference to the owner's account-level instructions; a field-specific analogy domain; only an implied fallback when there's no claude.ai Project. Open from the 2026-11-05 dump safety check: "usage constrained" in Step 0 describes the owner's plan limits; the "connectedness" example may come from a specific course (⚠️ VERIFY).

## career-planning

No items yet.

## programming

### safety
- type: skill
- status: idea
- description: safety-checks skills and code before publishing
- spec:
- notes: ⚠️ VERIFY: placeholder, to expand

### webapp-design
- type: skill
- status: idea
- description: web app design guidance
- spec:
- notes: ⚠️ VERIFY: placeholder, to expand

## other

### council
- type: skill
- status: built
- description: Convene a council of independent Claude subagents on a hard decision: blind answers, anonymous peer review with a vote on every claim, a scripted tally, and a chairman's verdict that keeps dissent visible.
- spec: [council/SKILL.md](<skills-projects [CURRENT]/skills/council/SKILL.md>) (built before this workflow existed)
- notes: claude.ai chat edition. SKILL.md refers to a separate Claude Code edition that isn't in this library, and scripts/check_editions.py needs it. validate_config.py needs PyYAML.

### handoff
- type: skill
- status: built
- description: Compress the current chat into a handoff a new chat (Claude, Gemini, or ChatGPT) can continue from: state, decisions, rules, next step. Also produces an AI-ready overview and prints a portable overview prompt.
- spec: [handoff/SKILL.md](<skills-projects [CURRENT]/skills/handoff/SKILL.md>) (built before this workflow existed)
- notes: Open findings from the 2026-10-26 migration safety check, not yet applied: references/template.md and references/topic-modules.md are unused older copies (proposed for deletion); the example filename in SKILL.md looks like a real exam.

### new-games
- type: project
- status: built
- description: Picks what to play from the user's backlog, judges whether a deal is worth buying now or waiting for, finds new releases that fit, and keeps the game library file accurate.
- spec: [new-games/instructions.md](<skills-projects [CURRENT]/projects/new-games/instructions.md>)
- notes:

### patch
- type: skill
- status: built
- description: Package a claude.ai failure (a Project instruction, ! command, skill, preference or memory line that produced the wrong behavior) into one self-contained patch report for a separate chat to fix.
- spec: [patch/SKILL.md](<skills-projects [CURRENT]/skills/patch/SKILL.md>) (built before this workflow existed)
- notes:

### prompt,project,skill-creator
- type: project
- status: built
- description: Turns a rough, wordy request into a tightened prompt, a full Project instruction set, a ! command for a specific Project, or a fix built from a patch report.
- spec: [prompt,project,skill-creator/instructions.md](<skills-projects [CURRENT]/projects/prompt,project,skill-creator/instructions.md>)
- notes:

### research-items
- type: project
- status: built
- description: Researches an item to buy from any store: a ranked, cross-referenced shortlist first, then availability, where to buy and direct links once the user is ready.
- spec: [research-items/instructions.md](<skills-projects [CURRENT]/projects/research-items/instructions.md>)
- notes:
