# Example: tweak (swap a seat, re-model a seat, change rounds)

Use case: a claude.ai Project for product decisions on a side project. Paste the block
into the Project's instructions.

```yaml
# COUNCIL CONFIG v1
version: 1
mode: tweak
rounds: 3
swap_seats:
  - replace: stakeholder
    with:
      id: user-advocate
      name: User Advocate
      model: sonnet
      lens: >
        Speak for the people who would use this product. What problem do they actually
        have, what would make them switch, and which option makes their week better? Point
        to the evidence in the case, and say when there isn't any.
seat_models:
  operator: opus
shared_context: >
  Solo builder with about ten hours a week. Prefer options that can ship in two weeks
  and be undone cheaply.
```

Resolved council: Evidence (opus), Pre-mortem (opus), Upside (sonnet), Reframer (opus),
Operator (opus), User Advocate (sonnet); 3 rounds (answers, peer review, rebuttal).
