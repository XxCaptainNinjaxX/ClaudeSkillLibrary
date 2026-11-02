# IS265

Instructions for a course Project that does two jobs. It handles study help by routing pasted course material to the slide-breakdown skill and review requests to the exam-review skill. It also drafts graded work through a `!homework` command: a briefing and questions first, then a draft in the user's own voice with checked APA citations, then revision rounds until the user says done.

| Category | Version | Works in |
|---|---|---|
| education | — | Claude chat (Project); Gemini Gem or custom GPT with fallbacks |

## What it does

| Job | Invocation | Output |
|---|---|---|
| Study help | Paste or screenshot course material; ask for a quiz, flashcards, a practice exam or a cheat sheet | A slide-breakdown or exam-review session. Without the skills, the same format done directly |
| Discussion forum | `!homework df` | A paste-ready Canvas post (≤7 sentences, starting "Initial Post - "), plus a word-count check line and, on request, 2 replies |
| Written homework | `!homework hw` or `!homework homework` | A formatted Google Doc draft, plus a rubric scorecard and checks in chat |

Both `!homework` types follow the same writing rules: first person, one connected argument, sentences of 30 words or fewer, no fluff, personal details only from what the user says in the chat, and outside sources only from a live web search that has been opened and checked.

## How it's triggered

- `!homework <type>` as the first thing in the message, where `<type>` is `df`, `hw` or `homework` (case-insensitive). Everything after it is input. During a run, no other skill triggers on that input.
- Pasted course material triggers slide-breakdown. "Quiz me", review, flashcard, practice-exam and cheat-sheet requests trigger exam-review.

## Inputs

- **DF:** the assignment text and the TED talk transcript. Classmate posts are optional and only calibrate tone and length.
- **HW:** the assignment text and the rubric (screenshot or paste).
- **Project knowledge:** the course textbook. It's searched for concepts, term meanings and the book citation, and never cited from memory.
- Whatever the user pastes in a run beats the defaults. Conflicts are named in one line.

## Output format

1. **Briefing and questions (stops).** DF gets a talk summary. HW gets the HW number. Both then get: terms, what the assignment wants, a rubric checklist (HW), constraints, and up to 5 questions.
2. **Angles and source (doesn't stop).** Up to 5 angles, all folded into the draft. One checked outside source, with its APA entry and 1–2 backups.
3. **Draft (stops).**
   - DF: one fenced block, then a check line (each sentence's word count, source cited, "set Arial 12 in the Canvas editor"), then "Want the 2 replies?"
   - HW: a Google Doc named `IS265 <HW number> – <short topic>` in the Drive folder `IS265`, set in Arial 12, double spaced, with 1-inch margins. In chat: the link, a rubric scorecard, checks, and a reminder to download it as .docx before submitting.
4. **Revision loop (stops after each round).** The user's pasted text becomes the current version, and only their notes are applied. Then come the re-run checks and at most 5 bullets on what changed. HW replaces the Doc's content; DF returns the full post.

## Dependencies

- **Course textbook**, uploaded as a Project knowledge file.
- **Skills:** [slide-breakdown](<../../skills/slide-breakdown/README.md>) and [exam-review](<../../skills/exam-review/README.md>) from this library. Without them, the Project does the task directly in the same format.
- **google-workspace skill** (a claude.ai built-in skill, not in this repo). It's read before the first Google Drive or Docs call.
- **Web search**, for outside sources. Without it, the Project says so and asks the user for a source.
- **Google Drive / Google Docs connector**, for HW drafts. Fallbacks: a Claude Docs doc (which exports to .docx), then the full draft in a fenced block.

## How to use

### Claude chat (Project)

1. Create a Project and paste the full text of [Instructions+Commands.md](<Instructions+Commands.md>) into its instructions.
2. Upload the course textbook to the Project's knowledge.
3. Install the [slide-breakdown](<../../skills/slide-breakdown/README.md>) and [exam-review](<../../skills/exam-review/README.md>) skills (see each README's **Claude chat** steps).
4. Connect Google Drive and turn on web search. For HW drafts, create a Drive folder named `IS265`; without it, the Doc goes to the Drive root.
5. In a chat inside the Project, type `!homework df` or `!homework hw`, followed by the assignment.

To use the instructions for another course, replace `IS265` in both files with that course's code.

### Other LLMs (Gemini Gem, custom GPT)

Paste [Instructions+Commands.md](<Instructions+Commands.md>) as the Gem or GPT instructions and attach the textbook as a knowledge file. Then type `!homework df` or `!homework hw` as plain text.

| Claude-only feature | What to do instead |
|---|---|
| slide-breakdown and exam-review skills | Built-in fallback: the model does the task directly in the same format. For the full formats, also paste each skill's SKILL.md body |
| google-workspace skill and Google Drive/Docs connector | Built-in fallback: the full draft comes back in a fenced block. Paste it into a Google Doc and set Arial 12, double spacing and 1-inch margins yourself |
| Claude Docs fallback | Skip it; use the fenced-block draft |
| Project knowledge search | Attach the textbook to the Gem or GPT. If the model can't search it, paste the relevant pages |
| Live web search with page checks | Use a model with browsing turned on, or supply the source yourself when it asks |
