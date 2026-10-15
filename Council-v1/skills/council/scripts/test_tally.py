#!/usr/bin/env python3
"""Tests for tally.py. Run: python3 scripts/test_tally.py"""
import json
import os
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
TALLY = os.path.join(HERE, "tally.py")

ANSWERS = """=== MAP
A = evidence | Evidence
B = premortem | Pre-mortem
C = upside | Upside
D = operator | Operator
=== ANSWER A
POSITION: Build the portfolio project.
CLAIMS:
1. [fact] Most intern screens look at shipped work first - recruiter surveys say so.
2. [inference] LeetCode matters less for TPM roles
   than for SWE roles - interview loops differ.
RISK: The project stalls.
ASSUMPTIONS: none
FLIP: Target companies run coding screens for TPM interns.
CONFIDENCE: high - several sources agree
SOURCES: none
=== ANSWER B
POSITION: Do LeetCode first.
CLAIMS:
1. [judgment] Unfinished projects signal nothing - half-done repos read as abandoned.
2. [fact] Break is four weeks long - per the case file.
3. [inference] Coding screens filter before portfolios are read - order of the funnel.
RISK: Burnout.
ASSUMPTIONS: none
FLIP: A finished project already exists.
CONFIDENCE: medium - depends on targets
SOURCES: none
=== ANSWER C
POSITION: Build something public.
CLAIMS:
1. [judgment] A project can turn into a startup - upside is uncapped.
2. [inference] Public work compounds - people find it later.
RISK: Distraction.
ASSUMPTIONS: none
FLIP: No time.
CONFIDENCE: low - speculative
SOURCES: none
=== ANSWER D
POSITION: Split the weeks.
CLAIMS:
1. [judgment] Two weeks each is feasible - the schedule fits.
2. [inference] Splitting halves the payoff of each - context switching costs.
RISK: Neither gets done.
ASSUMPTIONS: none
FLIP: Hard deadline appears.
CONFIDENCE: high - simple plan
SOURCES: none
"""

REVIEWS = """=== REVIEW evidence
RANKING: A > B > D > C
VOTES:
A1: agree - mine
A2: agree - mine
B1: dispute - weak
B2: agree - stated
B3: unsure - unclear
C1: dispute - fantasy
C2: agree - plausible
D1: agree - fine
D2: dispute - wrong
STRONGEST: A - shipped work
WEAKEST: C - fantasy
MISSED: nobody asked about the deadline
=== REVIEW premortem
RANKING: B > A > C > D
VOTES:
A1: agree - ok
A2: dispute - not shown
B1: agree - mine
B2: agree - mine
B3: agree - mine
C1: dispute - no
C2: unsure - maybe
D1: agree - ok
D2: dispute - no
STRONGEST: B - funnel
WEAKEST: D - vague
MISSED: nothing material
=== REVIEW Upside
RANKING: C > D > A > B
VOTES:
A1: agree - ok
A2: dispute - no data
B1: dispute - no
B2: agree - ok
B3: agree - ok
C1: agree - mine
C2: agree - mine
D1: agree - ok
STRONGEST: C - upside
WEAKEST: B - narrow
MISSED: none
=== REVIEW operator
RANKING: D > A > B > C
VOTES:
- **A1**: agree — fine
A2: unsure - hmm
B1: disagree - no
B2: agree - yes
B3: dispute - funnel varies
C1: dispute - no
C2: agree - yes
D1: agree - mine
D2: agree - mine
STRONGEST: D - feasible
WEAKEST: C - vague
MISSED: cost of tools
"""

REBUTTALS = """=== REBUTTAL premortem
B1: WITHDRAW - fair, a half-done repo with a clear README still signals
B3: DEFEND - most large companies screen first
FINAL POSITION: Do LeetCode first, keep a small project going.
CHANGED: no - nothing named a flaw in the funnel argument
=== REBUTTAL evidence
A2: AMEND - LeetCode matters less for TPM interns at non-FAANG companies
FINAL POSITION: Build the project.
CHANGED: yes - the base rate I used was for SWE roles
"""


def run(text, *args):
    p = subprocess.run([sys.executable, TALLY, "-", *args], input=text, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def run_json(text):
    code, out, err = run(text, "--json")
    return code, (json.loads(out) if code == 0 else None), err


class Tally(unittest.TestCase):
    def setUp(self):
        code, self.r, err = run_json(ANSWERS + REVIEWS)
        self.assertEqual(code, 0, err)
        self.claims = {c["id"]: c for c in self.r["claims"]}

    def test_statuses_and_votes_exclude_self(self):
        expect = {"A1": ("Confirmed", 3, 0, 0), "A2": ("Disputed", 0, 2, 1),
                  "B1": ("Disputed", 0, 3, 0), "B2": ("Confirmed", 3, 0, 0),
                  "B3": ("Contested", 1, 1, 1), "C1": ("Disputed", 0, 3, 0),
                  "C2": ("Confirmed", 2, 0, 1), "D1": ("Confirmed", 3, 0, 0),
                  "D2": ("Disputed", 0, 2, 0)}
        for cid, (status, a, d, u) in expect.items():
            c = self.claims[cid]
            self.assertEqual((c["status"], c["a"], c["d"], c["u"]), (status, a, d, u), cid)

    def test_multiline_claim_and_support_split(self):
        self.assertEqual(self.claims["A2"]["claim"], "LeetCode matters less for TPM roles than for SWE roles")
        self.assertEqual(self.claims["A2"]["support"], "interview loops differ.")

    def test_peer_ranks_exclude_self(self):
        ranks = {r["letter"]: r["avg_peer_rank"] for r in self.r["peer_ranks"]}
        self.assertEqual(ranks, {"A": 2.33, "B": 3.0, "C": 3.67, "D": 3.0})
        self.assertEqual(self.r["peer_ranks"][0]["letter"], "A")

    def test_confidence_and_warnings(self):
        self.assertEqual(self.r["seat_confidence"], {"high": 2, "medium": 1, "low": 1, "missing": 0})
        self.assertTrue(any("no vote on D2" in w for w in self.r["warnings"]))

    def test_review_header_by_name(self):
        self.assertEqual(self.claims["C1"]["d"], 3)

    def test_round3_candidates(self):
        self.assertEqual(self.r["round3_candidates"],
                         {"evidence": ["A2"], "premortem": ["B1", "B3"], "upside": ["C1"], "operator": ["D2"]})

    def test_rebuttals_applied(self):
        code, r, err = run_json(ANSWERS + REVIEWS + REBUTTALS)
        self.assertEqual(code, 0, err)
        c = {x["id"]: x for x in r["claims"]}
        self.assertEqual(c["B1"]["status"], "Withdrawn")
        self.assertEqual(c["B3"]["status"], "Contested (defended)")
        self.assertEqual(c["A2"]["status"], "Disputed (amended, not re-voted)")
        self.assertEqual(r["rebuttals"]["evidence"]["changed"], "yes")
        self.assertEqual(r["round3_candidates"], {})
        self.assertTrue(any("unanswered: C1, D2" in w for w in r["warnings"]))

    def test_markdown_render(self):
        code, out, err = run(ANSWERS + REVIEWS)
        self.assertEqual(code, 0, err)
        self.assertIn("| A2 | LeetCode matters less for TPM roles than for SWE roles | Evidence | 0/2/1 | Disputed | must show |", out)
        self.assertIn("--- Pre-mortem (premortem)", out)

    def test_quick_run_has_no_statuses(self):
        code, r, err = run_json(ANSWERS)
        self.assertEqual(code, 0, err)
        self.assertFalse(r["peer_review"])
        self.assertTrue(all(c["status"] == "No peer review" for c in r["claims"]))

    def test_unusable_files(self):
        self.assertEqual(run("just some text")[0], 1)
        self.assertEqual(run("=== MAP\nA = evidence\n=== ANSWER B\nPOSITION: x\n")[0], 1)


if __name__ == "__main__":
    unittest.main(verbosity=1)
