#!/usr/bin/env python3
"""Tests for validate_config.py. Run: python3 scripts/test_validate_config.py"""
import json
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
VALIDATOR = os.path.join(HERE, "validate_config.py")
EXAMPLES = os.path.join(HERE, os.pardir, "references", "examples")
LENS = "A lens long enough to pass the forty character minimum for seats."


def run(text, flags=""):
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
        f.write(text)
    try:
        p = subprocess.run([sys.executable, VALIDATOR, f.name, "--flags", flags],
                           capture_output=True, text=True)
    finally:
        os.unlink(f.name)
    try:
        out = json.loads(p.stdout) if p.stdout.strip() else {}
    except ValueError:
        out = {}
    return p.returncode, out, p.stderr


def block(body):
    return "Some notes.\n\n```yaml\n# COUNCIL CONFIG v1\n" + textwrap.dedent(body) + "```\n"


class Valid(unittest.TestCase):
    def test_examples_are_valid(self):
        for name in ("extend", "tweak", "replace"):
            with open(os.path.join(EXAMPLES, name + ".md"), encoding="utf-8") as f:
                code, out, err = run(f.read())
            self.assertEqual(code, 0, f"{name}: {out} {err}")
            self.assertEqual(out["mode"], name)

    def test_flags_override_config(self):
        code, out, _ = run(block("version: 1\nmode: tweak\nrounds: 3\n"), flags="quick")
        self.assertEqual((code, out["rounds"]), (0, 1))
        code, out, _ = run(block("version: 1\nmode: tweak\nrounds: 1\n"), flags="rounds=2")
        self.assertEqual(out["rounds"], 2)

    def test_fable_needs_allow_fable(self):
        seat = f"  - id: deep\n    name: Deep\n    model: fable\n    lens: {LENS}\n"
        code, out, _ = run(block("version: 1\nmode: extend\nadd_seats:\n" + seat))
        self.assertEqual(code, 1)
        code, out, _ = run(block("version: 1\nmode: extend\nallow_fable: true\nadd_seats:\n" + seat))
        self.assertEqual((code, out["fable_seats"]), (0, ["deep"]))


class Invalid(unittest.TestCase):
    def assertError(self, text, fragment):
        code, out, err = run(text)
        self.assertEqual(code, 1, f"expected invalid: {out} {err}")
        joined = " ".join(out.get("errors", [])) + err
        self.assertIn(fragment, joined)

    def test_unknown_key(self):
        self.assertError(block("version: 1\nmode: tweak\nround: 3\n"), "unknown top-level key 'round'")

    def test_replace_needs_reason(self):
        seats = "".join(f"  - id: s{i}\n    name: S{i}\n    lens: {LENS}\n" for i in range(3))
        self.assertError(block("version: 1\nmode: replace\nseats:\n" + seats), "reason: required")

    def test_extend_cannot_swap(self):
        self.assertError(block("version: 1\nmode: extend\nremove_seats: [upside]\n"),
                         "not allowed in mode extend")

    def test_extend_needs_seats(self):
        self.assertError(block("version: 1\nmode: extend\nrounds: 3\n"), "add_seats: required")

    def test_empty_tweak(self):
        self.assertError(block("version: 1\nmode: tweak\n"), "tweak changes nothing")

    def test_quick_conflicts_with_rounds(self):
        self.assertError(block("version: 1\nmode: tweak\nquick: true\nrounds: 3\n"), "conflicts")

    def test_bad_target(self):
        self.assertError(block("version: 1\nmode: tweak\nseat_models:\n  skeptic: opus\n"),
                         "not a remaining default seat")

    def test_too_few_seats(self):
        self.assertError(block("version: 1\nmode: tweak\nremove_seats: [evidence, premortem, upside, reframer]\n"),
                         "the final roster needs 3 to 9")

    def test_duplicate_id(self):
        self.assertError(block(f"version: 1\nmode: extend\nadd_seats:\n  - id: evidence\n    name: Ev2\n    lens: {LENS}\n"),
                         "already names a default seat")

    def test_bad_model(self):
        self.assertError(block(f"version: 1\nmode: extend\nadd_seats:\n  - id: x\n    name: X\n    model: gpt-5\n    lens: {LENS}\n"),
                         "is not one of")

    def test_two_blocks(self):
        b = block("version: 1\nmode: tweak\nrounds: 3\n")
        code, _, err = run(b + b)
        self.assertEqual(code, 1)
        self.assertIn("keep exactly one", err)

    def test_wrong_version(self):
        self.assertError(block("version: 2\nmode: tweak\nrounds: 3\n"), "version: required and must be 1")


if __name__ == "__main__":
    unittest.main(verbosity=1)
