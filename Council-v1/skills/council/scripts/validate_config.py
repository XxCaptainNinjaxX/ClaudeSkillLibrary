#!/usr/bin/env python3
"""Validate a COUNCIL CONFIG v1 block and print the resolved council as JSON.

Usage:
  python3 validate_config.py CONFIG_FILE [--flags "quick rounds=3 default"] [--skill-md PATH]
  python3 validate_config.py - [--flags ...]        (read the text from stdin)
  python3 validate_config.py --print-default [--skill-md PATH]

CONFIG_FILE may be any text file (a CLAUDE.md, a SKILL.md, a Project-instructions dump)
that contains one fenced code block whose first line is exactly "# COUNCIL CONFIG v1",
or a file that is just the YAML itself starting with that line.

Exit codes: 0 valid, 1 invalid config, 2 usage or file error, 3 no YAML parser available.
The default roster is read from the "# COUNCIL DEFAULT ROSTER v1" block in SKILL.md,
so editing that block is the only change a fork needs to alter the default panel.
"""
import argparse
import json
import os
import re
import sys

CONFIG_SENTINEL = "# COUNCIL CONFIG v1"
ROSTER_SENTINEL = "# COUNCIL DEFAULT ROSTER v1"
MODELS = ("opus", "sonnet", "haiku", "fable")
MIN_SEATS, MAX_SEATS = 3, 9
ID_RE = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")

TOP_KEYS = {
    "version", "mode", "reason", "rounds", "quick", "allow_fable", "shared_context",
    "add_seats", "swap_seats", "remove_seats", "seat_models", "seats",
}
MODE_KEYS = {
    "extend": {"add_seats"},
    "tweak": {"add_seats", "swap_seats", "remove_seats", "seat_models"},
    "replace": {"seats"},
}
SETTING_KEYS = {"rounds", "quick", "allow_fable", "shared_context"}
SEAT_KEYS = {"id", "name", "lens", "asks", "model", "web_search"}


def load_yaml(text):
    try:
        import yaml  # PyYAML
    except ImportError:
        yaml = None
    if yaml is not None:
        return yaml.safe_load(text)
    try:
        body = "\n".join(l for l in text.splitlines() if not l.lstrip().startswith("#"))
        return json.loads(body)
    except ValueError:
        print("No YAML parser available (pip install pyyaml), and the block is not JSON. "
              "Validate by hand against SKILL.md section 2.", file=sys.stderr)
        sys.exit(3)


def extract_blocks(text, sentinel):
    """Return the bodies of fenced blocks whose first line is the sentinel."""
    blocks = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        m = re.match(r"^\s*(`{3,}|~{3,})", lines[i])
        if m:
            fence = m.group(1)
            j = i + 1
            body = []
            while j < len(lines) and not lines[j].strip().startswith(fence):
                body.append(lines[j])
                j += 1
            first = next((l.strip() for l in body if l.strip()), "")
            if first == sentinel:
                blocks.append("\n".join(body))
            i = j + 1
            continue
        i += 1
    if not blocks:
        stripped = text.strip()
        if stripped.splitlines() and stripped.splitlines()[0].strip() == sentinel:
            blocks.append(stripped)
    return blocks


def is_str(v):
    return isinstance(v, str)


def check_len(errors, where, v, lo, hi):
    if not is_str(v):
        errors.append(f"{where}: must be a string")
        return
    n = len(v.strip())
    if n < lo or n > hi:
        errors.append(f"{where}: length {n}, must be {lo} to {hi} characters")


def validate_seat(seat, where, errors, default_model="opus"):
    if not isinstance(seat, dict):
        errors.append(f"{where}: a seat must be a mapping")
        return None
    for k in seat:
        if k not in SEAT_KEYS:
            errors.append(f"{where}: unknown seat key '{k}'")
    for req in ("id", "name", "lens"):
        if req not in seat:
            errors.append(f"{where}: missing required key '{req}'")
    sid = seat.get("id")
    if sid is not None:
        if not is_str(sid) or len(sid) > 24 or not ID_RE.match(sid):
            errors.append(f"{where}: id '{sid}' must be lowercase hyphen-separated words, "
                          "starting with a letter, at most 24 characters")
    name = seat.get("name")
    if name is not None:
        if not is_str(name) or "\n" in name.strip():
            errors.append(f"{where}: name must be a single-line string")
        else:
            check_len(errors, f"{where}.name", name, 1, 40)
    if "lens" in seat:
        check_len(errors, f"{where}.lens", seat["lens"], 40, 700)
    asks = seat.get("asks")
    if asks is not None:
        if not isinstance(asks, list) or not 1 <= len(asks) <= 4:
            errors.append(f"{where}.asks: must be a list of 1 to 4 questions")
        else:
            for n, q in enumerate(asks):
                check_len(errors, f"{where}.asks[{n}]", q, 5, 160)
    model = seat.get("model", default_model)
    if model not in MODELS:
        errors.append(f"{where}.model: '{model}' is not one of {', '.join(MODELS)}")
    ws = seat.get("web_search", False)
    if not isinstance(ws, bool):
        errors.append(f"{where}.web_search: must be true or false")
    return {
        "id": sid,
        "name": name.strip() if is_str(name) else name,
        "lens": " ".join(seat.get("lens", "").split()) if is_str(seat.get("lens")) else None,
        "asks": [q.strip() for q in asks] if isinstance(asks, list) else [],
        "model": model,
        "web_search": ws if isinstance(ws, bool) else False,
    }


def load_default_roster(skill_md):
    try:
        text = open(skill_md, encoding="utf-8").read()
    except OSError as e:
        print(f"Cannot read SKILL.md at {skill_md}: {e}", file=sys.stderr)
        sys.exit(2)
    blocks = extract_blocks(text, ROSTER_SENTINEL)
    if len(blocks) != 1:
        print(f"SKILL.md must contain exactly one '{ROSTER_SENTINEL}' block; found {len(blocks)}",
              file=sys.stderr)
        sys.exit(2)
    data = load_yaml(blocks[0]) or {}
    errors = []
    if not isinstance(data, dict) or not isinstance(data.get("seats"), list):
        errors.append("default roster: needs a 'seats' list")
        data = {"seats": []}
    rounds = data.get("rounds", 2)
    if rounds not in (1, 2, 3):
        errors.append("default roster: rounds must be 1, 2 or 3")
    seats = [validate_seat(s, f"default.seats[{i}]", errors) for i, s in enumerate(data["seats"])]
    for s in seats:
        if s and s["model"] == "fable":
            errors.append(f"default roster: seat '{s['id']}' must not default to fable")
    check_roster(seats, "default roster", errors)
    if errors:
        print("Default roster in SKILL.md is invalid:\n- " + "\n- ".join(errors), file=sys.stderr)
        sys.exit(2)
    return seats, rounds


def check_roster(seats, where, errors):
    seats = [s for s in seats if s]
    if not MIN_SEATS <= len(seats) <= MAX_SEATS:
        errors.append(f"{where}: {len(seats)} seats; the final roster needs {MIN_SEATS} to {MAX_SEATS}")
    ids = [s["id"] for s in seats]
    names = [str(s["name"]).lower() for s in seats]
    for dup in sorted({i for i in ids if ids.count(i) > 1 and i is not None}):
        errors.append(f"{where}: seat id '{dup}' is used more than once")
    for dup in sorted({n for n in names if names.count(n) > 1}):
        errors.append(f"{where}: seat name '{dup}' is used more than once")


def parse_flags(flag_text):
    flags = {"quick": False, "rounds": None, "default": False}
    if not flag_text:
        return flags
    text = flag_text.lower()
    flags["quick"] = bool(re.search(r"\bquick\b", text))
    flags["default"] = bool(re.search(r"(?<![\w-])-{0,2}default\b", text))
    m = re.search(r"\brounds\s*[=:]?\s*(\d+)", text)
    if m:
        flags["rounds"] = int(m.group(1))
        if flags["rounds"] not in (1, 2, 3):
            print("rounds flag must be 1, 2 or 3", file=sys.stderr)
            sys.exit(2)
    return flags


def resolve(cfg, default_seats, default_rounds):
    errors, warnings = [], []
    if not isinstance(cfg, dict):
        return None, ["the config block must be a YAML mapping"], warnings
    for k in cfg:
        if k not in TOP_KEYS:
            errors.append(f"unknown top-level key '{k}'")
    if cfg.get("version") != 1:
        errors.append("version: required and must be 1")
    mode = cfg.get("mode")
    if mode not in MODE_KEYS:
        errors.append("mode: required; must be extend, tweak or replace")
        return None, errors, warnings
    for k in cfg:
        if k in TOP_KEYS - SETTING_KEYS - {"version", "mode", "reason"} and k not in MODE_KEYS[mode]:
            errors.append(f"'{k}' is not allowed in mode {mode}")

    reason = cfg.get("reason")
    if mode == "replace" and reason is None:
        errors.append("reason: required in replace mode (say why extend or tweak can't do it)")
    if reason is not None:
        check_len(errors, "reason", reason, 20, 400)

    rounds = cfg.get("rounds", default_rounds)
    if "rounds" in cfg and (isinstance(cfg["rounds"], bool) or cfg["rounds"] not in (1, 2, 3)):
        errors.append("rounds: must be 1, 2 or 3")
    quick = cfg.get("quick", False)
    if not isinstance(quick, bool):
        errors.append("quick: must be true or false")
    elif quick:
        if "rounds" in cfg and cfg["rounds"] in (2, 3):
            errors.append("quick: true conflicts with rounds 2 or 3; keep one")
        rounds = 1
    allow_fable = cfg.get("allow_fable", False)
    if not isinstance(allow_fable, bool):
        errors.append("allow_fable: must be true or false")
        allow_fable = False
    shared = cfg.get("shared_context")
    if shared is not None:
        check_len(errors, "shared_context", shared, 1, 1500)

    default_ids = [s["id"] for s in default_seats]
    roster = []
    if mode == "replace":
        seats = cfg.get("seats")
        if not isinstance(seats, list) or not seats:
            errors.append("seats: required in replace mode, as a list of seats")
        else:
            roster = [validate_seat(s, f"seats[{i}]", errors) for i, s in enumerate(seats)]
    else:
        roster = [dict(s) for s in default_seats]
        if mode == "tweak":
            removed = cfg.get("remove_seats", [])
            if not isinstance(removed, list):
                errors.append("remove_seats: must be a list of default seat ids")
                removed = []
            for rid in removed:
                if rid not in default_ids:
                    errors.append(f"remove_seats: '{rid}' is not a default seat id")
            roster = [s for s in roster if s["id"] not in removed]

            swaps = cfg.get("swap_seats", [])
            if not isinstance(swaps, list):
                errors.append("swap_seats: must be a list of {replace, with} entries")
                swaps = []
            swapped = set()
            for i, sw in enumerate(swaps):
                where = f"swap_seats[{i}]"
                if not isinstance(sw, dict) or set(sw) != {"replace", "with"}:
                    errors.append(f"{where}: needs exactly the keys 'replace' and 'with'")
                    continue
                target = sw["replace"]
                if target not in default_ids:
                    errors.append(f"{where}.replace: '{target}' is not a default seat id")
                    continue
                if target in removed:
                    errors.append(f"{where}.replace: '{target}' is also in remove_seats")
                    continue
                if target in swapped:
                    errors.append(f"{where}.replace: '{target}' is swapped twice")
                    continue
                new = validate_seat(sw["with"], f"{where}.with", errors)
                swapped.add(target)
                roster = [new if s["id"] == target else s for s in roster]

            models = cfg.get("seat_models", {})
            if not isinstance(models, dict):
                errors.append("seat_models: must map default seat ids to models")
                models = {}
            for sid, model in models.items():
                if sid not in default_ids or sid in removed or sid in swapped:
                    errors.append(f"seat_models: '{sid}' is not a remaining default seat "
                                  "(set a swapped-in or added seat's model on the seat itself)")
                    continue
                if model not in MODELS:
                    errors.append(f"seat_models.{sid}: '{model}' is not one of {', '.join(MODELS)}")
                    continue
                for s in roster:
                    if s["id"] == sid:
                        s["model"] = model

        adds = cfg.get("add_seats")
        if mode == "extend" and (not isinstance(adds, list) or not adds):
            errors.append("add_seats: required in extend mode, as a list of at least one seat")
        if adds is not None and not isinstance(adds, list):
            errors.append("add_seats: must be a list of seats")
            adds = []
        for i, s in enumerate(adds or []):
            new = validate_seat(s, f"add_seats[{i}]", errors)
            if new and new["id"] in default_ids:
                errors.append(f"add_seats[{i}]: id '{new['id']}' already names a default seat; "
                              "use swap_seats (tweak) to redefine a default seat")
            roster.append(new)

        if mode == "tweak":
            changes = [k for k in ("add_seats", "swap_seats", "remove_seats", "seat_models",
                                   "rounds", "shared_context") if cfg.get(k) not in (None, [], {})]
            if cfg.get("quick") is True:
                changes.append("quick")
            if not changes:
                errors.append("tweak changes nothing; add at least one change")

    check_roster(roster, "final roster", errors)
    for s in roster:
        if s and s.get("model") == "fable" and not allow_fable:
            errors.append(f"seat '{s['id']}' uses fable but allow_fable is not true")
    return {
        "mode": mode,
        "rounds": rounds,
        "allow_fable": allow_fable,
        "shared_context": " ".join(shared.split()) if is_str(shared) else None,
        "reason": " ".join(reason.split()) if is_str(reason) else None,
        "seats": [s for s in roster if s],
    }, errors, warnings


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description="Validate a COUNCIL CONFIG v1 block.")
    ap.add_argument("config_file", nargs="?")
    ap.add_argument("--flags", default="", help='run flags, e.g. "quick" or "rounds=3" or "default"')
    ap.add_argument("--skill-md", default=os.path.join(here, os.pardir, "SKILL.md"))
    ap.add_argument("--print-default", action="store_true")
    args = ap.parse_args()

    default_seats, default_rounds = load_default_roster(args.skill_md)
    flags = parse_flags(args.flags)

    if args.print_default or flags["default"] or not args.config_file:
        if not args.print_default and not flags["default"]:
            ap.print_usage(sys.stderr)
            sys.exit(2)
        result = {"config_source": "none (default roster)", "mode": "default",
                  "rounds": default_rounds, "allow_fable": False, "shared_context": None,
                  "reason": None, "seats": default_seats}
        warnings = ["default flag: project config ignored"] if flags["default"] else []
    else:
        try:
            text = (sys.stdin.read() if args.config_file == "-"
                    else open(args.config_file, encoding="utf-8").read())
        except OSError as e:
            print(f"Cannot read {args.config_file}: {e}", file=sys.stderr)
            sys.exit(2)
        blocks = extract_blocks(text, CONFIG_SENTINEL)
        if not blocks:
            print(f"No block starting with '{CONFIG_SENTINEL}' in {args.config_file}", file=sys.stderr)
            sys.exit(1)
        if len(blocks) > 1:
            print(f"{len(blocks)} COUNCIL CONFIG blocks in one file; keep exactly one", file=sys.stderr)
            sys.exit(1)
        cfg = load_yaml(blocks[0])
        result, errors, warnings = resolve(cfg, default_seats, default_rounds)
        if errors:
            print(json.dumps({"valid": False, "errors": errors}, indent=2))
            sys.exit(1)
        result = {"config_source": "stdin" if args.config_file == "-" else args.config_file, **result}

    if flags["quick"]:
        if flags["rounds"] not in (None, 1):
            warnings.append("both quick and rounds flags given; quick wins")
        result["rounds"] = 1
    elif flags["rounds"]:
        result["rounds"] = flags["rounds"]
    result["valid"] = True
    result["warnings"] = warnings
    result["fable_seats"] = [s["id"] for s in result["seats"] if s["model"] == "fable"]
    print(json.dumps(result, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
