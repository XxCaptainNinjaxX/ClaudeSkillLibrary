#!/usr/bin/env python3
"""Check that the chat and code editions of the council skill have not drifted apart.

Usage: python3 scripts/check_editions.py PATH_TO_OTHER_EDITION_FOLDER

Compares the sections of SKILL.md marked "<!-- shared: ... -->" and the files both
editions share. Exit 0 when they match, 1 when anything differs.
"""
import filecmp
import os
import sys

SHARED_FILES = ["LICENSE", "CREDITS.md", "scripts/tally.py", "scripts/validate_config.py",
                "scripts/test_tally.py", "scripts/test_validate_config.py",
                "scripts/check_editions.py"]
MARKERS = [
    ("<!-- shared: section 1", "## 2. Load configuration"),
    ("<!-- shared: from here to the end of section 3", "## 4. Write the case file"),
    ("<!-- shared: from here to the end of the file", None),
]


def shared_sections(path):
    text = open(os.path.join(path, "SKILL.md"), encoding="utf-8").read()
    parts = []
    for start, end in MARKERS:
        i = text.find(start)
        if i < 0:
            parts.append(None)
            continue
        j = text.find(end, i) if end else len(text)
        parts.append(text[i:j if j >= 0 else len(text)])
    return parts


def main():
    if len(sys.argv) != 2:
        print(__doc__.strip(), file=sys.stderr)
        sys.exit(2)
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    other = os.path.abspath(sys.argv[1])
    problems = []
    for n, (a, b) in enumerate(zip(shared_sections(here), shared_sections(other)), 1):
        if a is None or b is None:
            problems.append(f"shared block {n}: marker missing in {'this' if a is None else 'the other'} edition")
        elif a != b:
            problems.append(f"shared block {n} of SKILL.md differs")
    for f in SHARED_FILES:
        pa, pb = os.path.join(here, f), os.path.join(other, f)
        if not (os.path.exists(pa) and os.path.exists(pb)) or not filecmp.cmp(pa, pb, shallow=False):
            problems.append(f"{f} differs or is missing")
    if problems:
        print("Editions have drifted:\n- " + "\n- ".join(problems))
        sys.exit(1)
    print("Editions match: shared SKILL.md sections and shared files are identical.")


if __name__ == "__main__":
    main()
