# Example: replace (full custom council; discouraged, needs a reason)

Use case: a claude.ai Project that checks statistical analyses for coursework. A decision
panel is the wrong tool here, so the config replaces it and says why.

```yaml
# COUNCIL CONFIG v1
version: 1
mode: replace
reason: >
  This Project checks statistical analyses, not decisions. Upside, Operator and
  Stakeholder have nothing to judge here, and a tweak would still leave a decision panel
  ruling on a methods question.
rounds: 2
seats:
  - id: methodologist
    name: Methodologist
    model: opus
    lens: >
      Is the study design right for the question? Check the unit of analysis, sampling,
      confounders, and whether the stated conclusion can follow from this design at all.
  - id: assumptions
    name: Assumptions Checker
    model: opus
    lens: >
      List the assumptions each test or model needs (independence, normality, equal
      variance, linearity, sample size), say which ones the data shown could violate, and
      what each violation would do to the result.
  - id: reviewer-two
    name: Reviewer Two
    model: sonnet
    lens: >
      Act as the harshest fair peer reviewer. Find the single weakest step in the
      analysis, the alternative explanation nobody ruled out, and the claim that
      overreaches.
  - id: explainer
    name: Explainer
    model: sonnet
    lens: >
      Check that the conclusion is stated correctly for a non-expert reader: p-values,
      confidence intervals and effect sizes interpreted correctly, and no causal language
      the design cannot support.
```

Resolved council: Methodologist (opus), Assumptions Checker (opus), Reviewer Two
(sonnet), Explainer (sonnet); 2 rounds. The run record says the default panel was
replaced.
