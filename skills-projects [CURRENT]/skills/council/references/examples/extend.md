# Example: extend (add a seat, keep the default six)

Use case: a claude.ai Project for career decisions. Paste the block into the Project's
instructions (or into a knowledge file). The six default seats stay as they are and a
seventh seat joins them.

```yaml
# COUNCIL CONFIG v1
version: 1
mode: extend
shared_context: >
  The asker is a student weighing internships and early-career moves toward technical
  product management. Weigh learning value and career signal, not only short-term pay.
add_seats:
  - id: hiring-manager
    name: Hiring Manager
    model: opus
    lens: >
      Judge each option the way a hiring manager screening early-career product and
      program candidates would: the signal it sends on a resume and in interviews, what
      it proves about execution, and what a stronger candidate would have done instead.
    asks:
      - How would this choice read as one resume line?
      - Which interview question does it help answer, and how well?
```

Resolved council: Evidence (opus), Pre-mortem (opus), Upside (sonnet), Reframer (opus),
Operator (sonnet), Stakeholder (sonnet), Hiring Manager (opus); 2 rounds.
