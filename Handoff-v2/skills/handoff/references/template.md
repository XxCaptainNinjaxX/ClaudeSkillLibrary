# Handoff file template

Fill every section that applies. Delete a section entirely if it would be empty. Don't leave "N/A" lines. Keep the section order: the top of the file is what the next Claude reads first and weights most.

```markdown
# Handoff — <Topic, in plain words>

> **To the next Claude:** This file continues a previous chat. Treat everything
> below as established context. Do not re-introduce yourself, re-explain covered
> material, or ask for info already listed here. Follow the "How to respond"
> rules exactly — they override your defaults. Start by doing the Resume point.

_Handoff created: <YYYY-MM-DD> · Topic type: <study | research/planning | technical | decision | creative | casual> · Source chat length: <rough turn count>_

## How to respond (rules set in the previous chat)
<!-- Formatting/behavior rules the user set or changed IN THAT CHAT. Write as
direct commands. Note when a rule overrides a Project or default behavior. -->
- <e.g. Do NOT add the end-of-response prompt note.>
- <e.g. Teach with 5 analogies per concept, plain explanation first.>

## Resume point
<!-- The single next action, specific enough to do immediately. -->
<e.g. Ask practice question 14 (accrual vs. cash basis). User has missed this concept twice.>

## Goal
<!-- 1–2 lines: what the user is ultimately trying to get done, and by when. -->

## Current state
<!-- Where things stand right now. Bullets, exact values. -->

## Decisions made
<!-- Decision — reason. Only things the USER confirmed. -->
- <Decision> — <why>

## Suggested but not confirmed
<!-- Claude's recommendations the user hasn't explicitly accepted. -->

## Rejected / ruled out
- <Option> — <why it was ruled out>

## Corrections to remember
<!-- Places where the user corrected Claude. State the correct version. -->
- <Wrong assumption> → <correct version>

## Key facts & data
<!-- Numbers, specs, names, dates, scores. Exact values. Mark (unverified) and
(as of YYYY-MM-DD) where relevant. -->

## <Topic-specific sections — see topic-modules.md>

## Open questions
**User needs to answer:**
- 
**Claude should look up / verify:**
- 

## Files to re-attach
<!-- Files uploaded or created in the old chat. They don't travel with this file. -->
- `<filename>` — <what it is, what it was used for>

## Reference archive
<!-- Past info the user may want to refer back to but that isn't active. Keep it
compact, and prefer outcome over transcript. -->

## Context gaps
<!-- What the handoff may be missing: early turns cut from context, anything
ambiguous. Omit the section if there are none. -->
```
