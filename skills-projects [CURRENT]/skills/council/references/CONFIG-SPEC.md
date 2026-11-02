# COUNCIL CONFIG v1 — specification (claude.ai chat edition)

This file is the long-form spec. `SKILL.md` section 2 holds the normative core, and
`scripts/validate_config.py` implements it; if this file and SKILL.md ever disagree,
SKILL.md wins. Everything here is written so that a separate session can generate a valid
config from this file alone.

## 1. Precedence

From highest to lowest, for one run:

1. **Run level**: flags typed right after the trigger (`quick`, `rounds=N`, `default`), and
   a COUNCIL CONFIG v1 block pasted into the triggering message itself. Both apply to that
   run only. Flags are applied on top of a pasted block.
2. **Project config**: one COUNCIL CONFIG v1 block found in the current Project.
3. **Built-in default**: the `# COUNCIL DEFAULT ROSTER v1` block in SKILL.md.

`default` skips step 2. There is no account-level config layer: your profile preferences
never count. To change the default panel everywhere, edit the default roster block in
SKILL.md and upload the skill again.

## 2. Where a config can live

Checked in this order:

1. The current Project's instructions.
2. The current Project's knowledge files. When the Project uses search over its
   knowledge, the skill searches for `COUNCIL CONFIG v1`.

A chat outside any Project has no project config. Prefer the instructions: they are always
in context, while a large knowledge base is searched, and a search can miss the block.

**Ties and conflicts**

- The first block found in the order above wins. The run record lists any lower-ranked
  block that was ignored.
- Two knowledge files that each hold a block are a tie. The skill stops and asks which
  one to use.
- A file may contain at most one block.
- Text inside the council skill's own folder (this spec, the examples) never counts.

## 3. Block format

- A fenced code block (three or more backticks or tildes; an info string such as `yaml`
  is fine) whose **first non-empty line is exactly** `# COUNCIL CONFIG v1`.
- The body is YAML. Plain mappings, lists and scalars only; no anchors, aliases or tags.
  Long text can use folded scalars (`>`). Any line beginning with `#` is a comment.
- Booleans are `true` or `false`. Integers are bare digits. Strings may be quoted or
  unquoted.

## 4. Top-level keys

Any key not listed is an error.

| Key | Type | Default | Allowed in | Constraint |
|---|---|---|---|---|
| `version` | integer | none | all, **required** | must be `1` |
| `mode` | string | none | all, **required** | `extend`, `tweak` or `replace` |
| `reason` | string | none | **required** in `replace`; optional elsewhere | 20 to 400 characters |
| `rounds` | integer | from the default roster (2) | all | `1`, `2` or `3` |
| `quick` | boolean | `false` | all | `true` forces rounds = 1; `true` with `rounds: 2` or `3` is an error |
| `allow_fable` | boolean | `false` | all | must be `true` if any seat has `model: fable` |
| `shared_context` | string | none | all | 1 to 1500 characters; appended verbatim to every case file |
| `add_seats` | list of seat | none | `extend` (**required**, at least 1), `tweak` | each id must be new |
| `swap_seats` | list of swap | none | `tweak` | see below |
| `remove_seats` | list of seat id | none | `tweak` | default seat ids only |
| `seat_models` | map of seat id to model | none | `tweak` | remaining default seats only |
| `seats` | list of seat | none | `replace`, **required** | the full roster |

A **swap** is a mapping with exactly two keys: `replace` (a default seat id) and `with`
(a seat).

## 5. Seat object

Any key not listed is an error.

| Key | Type | Default | Constraint |
|---|---|---|---|
| `id` | string | none, **required** | lowercase letters and digits in hyphen-separated words, starting with a letter, at most 24 characters (regex `^[a-z][a-z0-9]*(-[a-z0-9]+)*$`); unique in the final roster |
| `name` | string | none, **required** | 1 to 40 characters, one line; unique in the final roster, ignoring case |
| `lens` | string | none, **required** | 40 to 700 characters: what this seat looks for and argues; written as instructions to the seat |
| `asks` | list of string | none | 1 to 4 items, each 5 to 160 characters: questions the seat must address |
| `model` | string | `opus` | `opus`, `sonnet`, `haiku` or `fable` |
| `web_search` | boolean | `false` | `true` lets the seat search the web in round 1 |

Write the lens as a job, not a personality: what the seat checks, what it argues, what
it ignores because another seat covers it. Never write a lens that tells a seat to agree,
to reach a set answer, or to defer to another seat.

## 6. Modes

| | extend | tweak | replace |
|---|---|---|---|
| Starts from | default roster | default roster | nothing |
| `add_seats` | required | allowed | not allowed |
| `swap_seats`, `remove_seats`, `seat_models` | not allowed | allowed | not allowed |
| `seats` | not allowed | not allowed | required |
| `reason` | optional | optional | required |
| Settings (`rounds`, `quick`, `allow_fable`, `shared_context`) | allowed | allowed | allowed |

- **extend** is additive. Every default seat runs exactly as defined in SKILL.md.
- **tweak** changes the defaults. It must change something: a seat change, `rounds`,
  `quick: true` or `shared_context`. An empty tweak is an error.
- **replace** is discouraged. Prefer extend or tweak whenever any default seat still
  applies. The `reason` must say why neither works, and the run record says the default
  panel was replaced.

## 7. How a config is resolved

1. Start from the default roster (`extend`, `tweak`) or from `seats` (`replace`).
2. `tweak` only, in this order: drop `remove_seats`; replace each `swap_seats.replace`
   with its `with` seat at the same position; apply `seat_models`.
3. Append `add_seats` at the end, in order.
4. Settings: `rounds` (or 1 if `quick: true`), `allow_fable`, `shared_context`.
5. Run flags: `quick` sets rounds to 1; `rounds=N` sets rounds to N; `quick` wins if both
   are given.
6. Final checks: 3 to 9 seats, unique ids and names, the Fable rule.

## 8. Validation errors (complete list)

A config with any of these is invalid. The council does not convene; it lists every error.

- Unknown top-level key, or unknown seat key
- `version` missing or not `1`; `mode` missing or not one of the three
- A seat-structure key used in a mode that does not allow it (table in section 6)
- `reason` missing in replace mode, or outside 20 to 400 characters
- `rounds` not 1, 2 or 3; `quick` not a boolean; `quick: true` together with `rounds: 2` or `3`
- `allow_fable` not a boolean; any `fable` seat without `allow_fable: true`
- `shared_context` empty or over 1500 characters
- `add_seats` missing or empty in extend mode; an added id that matches a default seat id
  (redefine a default seat with `swap_seats` instead)
- `remove_seats` or `swap_seats.replace` naming a seat that is not a default seat; the same
  id both removed and swapped, or swapped twice; a swap without exactly `replace` and `with`
- `seat_models` naming a seat that is not a remaining default seat (set the model of a
  swapped-in or added seat on the seat itself); an unknown model
- A seat missing `id`, `name` or `lens`; any field outside its constraint
- Final roster below 3 or above 9 seats; duplicate ids; duplicate names
- More than one block in one file; a tie between two locations at the same step

## 9. Run flags

Typed right after the trigger, for one run only, for example `/council quick: should I…`
or `ask the council (rounds=3): …`.

| Flag | Effect |
|---|---|
| `quick` | rounds = 1: independent answers and synthesis, no peer review |
| `rounds=N` | N = 1, 2 or 3 (`rounds 3` also works) |
| `default` | ignore any project config and run the default roster |

## 10. Models

- Seats run on the model named in their config: `opus`, `sonnet`, `haiku` or `fable`. The
  chairman is always the main session, on whatever model it runs.
- No seat ever defaults to `fable`. Using it takes `model: fable` on the seat and
  `allow_fable: true` in the same config, and the convening line names every Fable seat.
- If the subagent tool rejects a model, that seat runs on the tool's default model and the
  run record says so.

## 11. Examples

One per mode, each validated by `scripts/validate_config.py`:

- `examples/extend.md`: career-decisions Project; adds a Hiring Manager seat
- `examples/tweak.md`: product-decisions Project; swaps Stakeholder for User Advocate,
  moves Operator to opus, runs 3 rounds
- `examples/replace.md`: statistics-methods Project; four custom seats, with a reason

## 12. Invalid configs and their errors

```yaml
# COUNCIL CONFIG v1
version: 1
mode: extend
remove_seats: [upside]
```
Error: `'remove_seats' is not allowed in mode extend` and `add_seats: required in extend
mode`. Use `mode: tweak` to remove seats.

```yaml
# COUNCIL CONFIG v1
version: 1
mode: tweak
round: 3
```
Errors: `unknown top-level key 'round'` and `tweak changes nothing`. The key is `rounds`.

```yaml
# COUNCIL CONFIG v1
version: 1
mode: tweak
seat_models:
  stakeholder: fable
```
Error: `seat 'stakeholder' uses fable but allow_fable is not true`.

```yaml
# COUNCIL CONFIG v1
version: 1
mode: replace
seats:
  - id: a
    name: A
    lens: Too short.
```
Errors: `reason: required in replace mode`, `seats[0].lens: length 10, must be 40 to 700
characters` and `final roster: 1 seats; the final roster needs 3 to 9`.

## 13. Checklist for a session that writes configs

1. Start the block with a fence, then the exact line `# COUNCIL CONFIG v1`.
2. Include `version: 1` and `mode`.
3. Pick the weakest mode that does the job: extend, then tweak, and replace only with a
   real `reason`.
4. Use only the keys in sections 4 and 5, in the modes section 6 allows.
5. Refer to default seats only by these ids: `evidence`, `premortem`, `upside`, `reframer`,
   `operator`, `stakeholder` (unless the fork's SKILL.md changed them).
6. Give new seats unique kebab-case ids, a `name` and a 40 to 700 character `lens`.
7. Never set `fable` without `allow_fable: true`, and only when asked to.
8. Check the final seat count is between 3 and 9.
9. If Python is available, write the block to a file and run
   `python3 scripts/validate_config.py <that-file>`, then fix every error.
