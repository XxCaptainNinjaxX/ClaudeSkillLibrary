#!/usr/bin/env python3
"""Tally a council run: peers-only votes, claim statuses, peer ranks, round-3 briefs.

Usage:
  python3 tally.py RUN_FILE [--json]
  python3 tally.py - [--json] < RUN_FILE        (read the run file from stdin)

The run file is the seats' raw outputs pasted verbatim under section headers:

  === MAP
  A = evidence | Evidence
  B = upside | Upside
  === ANSWER A
  <round-1 output of the seat mapped to A, verbatim>
  === REVIEW evidence
  <round-2 output of the evidence seat, verbatim>
  === REBUTTAL upside
  <round-3 output of the upside seat, verbatim>

MAP lines are "<letter> = <seat id> | <seat name>" (the name is optional). REVIEW and
REBUTTAL headers name the seat id. Each reviewer's votes on its own answer's claims, and
its ranking of its own answer, are dropped. Exit codes: 0 ok, 1 unusable run file, 2 usage.
"""
import argparse
import json
import re
import sys
from collections import OrderedDict

STATUS_ORDER = ["Disputed", "Contested", "Confirmed", "Confirmed (thin)", "Unreviewed",
                "Withdrawn", "No peer review"]
FIELDS = ["FINAL POSITION", "POSITION", "CLAIMS", "RISK", "ASSUMPTIONS", "FLIP", "CONFIDENCE",
          "SOURCES", "RANKING", "VOTES", "STRONGEST", "WEAKEST", "MISSED", "CHANGED"]
SECTION_RE = re.compile(r"^\s*={3,}\s*(MAP|ANSWER|REVIEW|REBUTTAL)\b\s*(.*?)\s*=*\s*$", re.I)
MAP_RE = re.compile(r"^\s*([A-Z])\s*[=:]\s*([A-Za-z][A-Za-z0-9-]*)\s*(?:\|\s*(.+?))?\s*$")
FIELD_RE = re.compile(r"^\s*[*_`#>\- ]*\s*(" + "|".join(FIELDS) + r")\s*[*_`]*\s*:\s*(.*)$", re.I)
CLAIM_RE = re.compile(r"^\s*(?:[-*]\s*)?(?:[A-Z])?(\d+)\s*[.)]\s*(?:\[(fact|inference|judg(?:e)?ment)\]\s*)?(.*)$", re.I)
ID_PREFIX = r"^\s*[-*]?\s*[*_`]*\s*([A-Z])\s*-?\s*(\d+)\s*[*_`]*\s*[:.)\-–—]\s*[*_`]*\s*"
VOTE_RE = re.compile(ID_PREFIX + r"(agree|agrees|dispute|disputes|disputed|disagree|unsure)\b[*_`]*\s*(?:[-–—:]\s*)?(.*)$", re.I)
REBUT_RE = re.compile(ID_PREFIX + r"(defend|amend|withdraw)\b[*_`]*\s*(?:[-–—:]\s*)?(.*)$", re.I)
SPLIT_RE = re.compile(r"\s+[-–—]\s+")
VOTE_WORDS = {"agree": "agree", "agrees": "agree", "dispute": "dispute", "disputes": "dispute",
              "disputed": "dispute", "disagree": "dispute", "unsure": "unsure"}


def split_sections(text):
    sections, current = [], None
    for line in text.splitlines():
        m = SECTION_RE.match(line)
        if m:
            current = {"kind": m.group(1).upper(), "arg": m.group(2).strip(), "lines": []}
            sections.append(current)
        elif current is not None:
            current["lines"].append(line)
    return sections


def split_fields(lines):
    """Map FIELD -> list of lines (first line holds the text after the colon)."""
    fields, current = OrderedDict(), None
    for line in lines:
        m = FIELD_RE.match(line)
        if m:
            current = m.group(1).upper()
            fields.setdefault(current, [])
            if m.group(2).strip():
                fields[current].append(m.group(2).strip())
        elif current is not None:
            fields[current].append(line)
    return fields


def one_line(lines):
    return " ".join(l.strip() for l in lines if l.strip())


def parse_claims(lines, letter, warnings):
    claims, current = [], None
    for line in lines:
        m = CLAIM_RE.match(line)
        if m and m.group(3).strip():
            current = {"num": int(m.group(1)), "tag": (m.group(2) or "").lower(),
                       "raw": m.group(3).strip()}
            claims.append(current)
        elif current is not None and line.strip():
            current["raw"] += " " + line.strip()
    out, seen = [], set()
    for c in claims:
        cid = f"{letter}{c['num']}"
        if cid in seen:
            warnings.append(f"answer {letter}: claim number {c['num']} appears twice; kept the first")
            continue
        seen.add(cid)
        parts = SPLIT_RE.split(c["raw"], maxsplit=1)
        out.append({"id": cid, "letter": letter, "tag": c["tag"].replace("judgement", "judgment"),
                    "claim": parts[0].strip(), "support": parts[1].strip() if len(parts) > 1 else ""})
    return out


def short(text, words=20):
    w = text.split()
    return " ".join(w[:words]) + ("…" if len(w) > words else "")


def status_for(a, d):
    if d >= 2 and d > a:
        return "Disputed"
    if a >= 2 and a > d:
        return "Confirmed"
    if a == 1 and d == 0:
        return "Confirmed (thin)"
    if d >= 1:
        return "Contested"
    return "Unreviewed"


def tally(text):
    warnings, errors = [], []
    sections = split_sections(text)
    if not sections:
        return None, ["no '=== MAP' / '=== ANSWER' sections found"], warnings

    letter_to_seat, seat_names = OrderedDict(), {}
    for s in sections:
        if s["kind"] != "MAP":
            continue
        for line in s["lines"]:
            if not line.strip():
                continue
            m = MAP_RE.match(line)
            if not m:
                warnings.append(f"MAP: could not read line '{line.strip()}'")
                continue
            letter, seat, name = m.group(1), m.group(2).lower(), (m.group(3) or m.group(2)).strip()
            if letter in letter_to_seat:
                errors.append(f"MAP: letter {letter} is assigned twice")
            if seat in letter_to_seat.values():
                errors.append(f"MAP: seat '{seat}' has two letters")
            letter_to_seat[letter] = seat
            seat_names[seat] = name
    if not letter_to_seat:
        errors.append("MAP section missing or empty")
    seat_to_letter = {v: k for k, v in letter_to_seat.items()}
    by_name = {n.lower(): s for s, n in seat_names.items()}

    def resolve_seat(arg):
        key = arg.strip().lower()
        return key if key in seat_names else by_name.get(key, key)

    answers, claims = OrderedDict(), OrderedDict()
    for s in sections:
        if s["kind"] != "ANSWER":
            continue
        letter = s["arg"].strip().upper()[:1]
        if letter not in letter_to_seat:
            errors.append(f"ANSWER {s['arg']}: letter is not in the MAP")
            continue
        if letter in answers:
            errors.append(f"ANSWER {letter} appears twice")
            continue
        f = split_fields(s["lines"])
        conf = one_line(f.get("CONFIDENCE", [])).lower()
        level = next((w for w in ("high", "medium", "low") if conf.startswith(w)), None)
        if level is None:
            warnings.append(f"answer {letter}: no high/medium/low CONFIDENCE line")
        cl = parse_claims(f.get("CLAIMS", []), letter, warnings)
        if not cl:
            warnings.append(f"answer {letter}: no numbered CLAIMS found")
        elif not 2 <= len(cl) <= 4:
            warnings.append(f"answer {letter}: {len(cl)} claims (the brief asks for 2 to 4)")
        answers[letter] = {"seat": letter_to_seat[letter], "position": one_line(f.get("POSITION", [])),
                           "confidence": level, "claims": [c["id"] for c in cl]}
        for c in cl:
            c.update({"seat": letter_to_seat[letter], "votes": [], "a": 0, "d": 0, "u": 0})
            claims[c["id"]] = c
    if not answers:
        errors.append("no ANSWER sections parsed")
    if errors:
        return None, errors, warnings

    reviews, rank_positions = OrderedDict(), {l: [] for l in answers}
    missed = []
    for s in sections:
        if s["kind"] != "REVIEW":
            continue
        reviewer = resolve_seat(s["arg"])
        if reviewer in reviews:
            warnings.append(f"REVIEW {reviewer} appears twice; kept the first")
            continue
        own = seat_to_letter.get(reviewer)
        if reviewer not in seat_names:
            warnings.append(f"REVIEW {reviewer}: seat not in MAP; all its votes count as peer votes")
        f = split_fields(s["lines"])
        voted, dropped, unknown = set(), 0, []
        for line in f.get("VOTES", []):
            m = VOTE_RE.match(line)
            if not m:
                if line.strip() and not line.strip().startswith("("):
                    warnings.append(f"review by {reviewer}: could not read vote line '{short(line.strip(), 12)}'")
                continue
            cid = f"{m.group(1).upper()}{int(m.group(2))}"
            vote = VOTE_WORDS[m.group(3).lower()]
            if cid not in claims:
                unknown.append(cid)
                continue
            if cid in voted:
                continue
            voted.add(cid)
            if claims[cid]["letter"] == own:
                dropped += 1
                continue
            claims[cid]["votes"].append({"by": reviewer, "vote": vote, "reason": m.group(4).strip()})
            claims[cid][{"agree": "a", "dispute": "d", "unsure": "u"}[vote]] += 1
        expected = {cid for cid, c in claims.items() if c["letter"] != own}
        missing = sorted(expected - voted, key=lambda x: (x[0], int(x[1:])))
        if missing:
            warnings.append(f"review by {reviewer}: no vote on {', '.join(missing)}")
        if unknown:
            warnings.append(f"review by {reviewer}: votes on unknown claims {', '.join(sorted(set(unknown)))}")
        ranking_text = one_line(f.get("RANKING", []))
        order = []
        for tok in re.findall(r"\b([A-Z])\b", ranking_text):
            if tok in answers and tok not in order:
                order.append(tok)
        if not order:
            warnings.append(f"review by {reviewer}: no usable RANKING line")
        elif set(order) != set(answers):
            warnings.append(f"review by {reviewer}: ranking leaves out {', '.join(sorted(set(answers) - set(order)))}")
        for pos, letter in enumerate(order, 1):
            if letter != own:
                rank_positions[letter].append(pos)
        m_text = one_line(f.get("MISSED", []))
        if m_text and m_text.lower().strip(' ."') not in ("nothing material", "none", "nothing"):
            missed.append({"by": reviewer, "text": m_text})
        reviews[reviewer] = {"own_letter": own, "votes_dropped_as_self": dropped,
                             "strongest": one_line(f.get("STRONGEST", [])),
                             "weakest": one_line(f.get("WEAKEST", []))}

    peer_review = bool(reviews)
    for c in claims.values():
        c["status"] = status_for(c["a"], c["d"]) if peer_review else "No peer review"
        c["engaged"] = c["a"] + c["d"]

    rebuttals = OrderedDict()
    for s in sections:
        if s["kind"] != "REBUTTAL":
            continue
        seat = resolve_seat(s["arg"])
        own = seat_to_letter.get(seat)
        if own is None:
            warnings.append(f"REBUTTAL {seat}: seat not in MAP; ignored")
            continue
        f = split_fields(s["lines"])
        actions = []
        for line in s["lines"]:
            m = REBUT_RE.match(line)
            if not m:
                continue
            cid = f"{m.group(1).upper()}{int(m.group(2))}"
            act = m.group(3).upper()
            if cid not in claims or claims[cid]["letter"] != own:
                warnings.append(f"rebuttal by {seat}: {cid} is not one of its claims; ignored")
                continue
            c = claims[cid]
            if c["status"] not in ("Contested", "Disputed"):
                warnings.append(f"rebuttal by {seat}: {cid} was {c['status']}, not challenged; ignored")
                continue
            c["rebuttal"] = {"action": act, "text": m.group(4).strip()}
            if act == "WITHDRAW":
                c["status_before_rebuttal"], c["status"] = c["status"], "Withdrawn"
            elif act == "AMEND":
                c["status"] += " (amended, not re-voted)"
            else:
                c["status"] += " (defended)"
            actions.append(cid)
        changed = one_line(f.get("CHANGED", [])).lower()
        rebuttals[seat] = {"actions": actions, "final_position": one_line(f.get("FINAL POSITION", [])),
                           "changed": "yes" if changed.startswith("yes") else ("no" if changed.startswith("no") else None),
                           "changed_because": one_line(f.get("CHANGED", []))}

    ranks = []
    for letter, positions in rank_positions.items():
        ranks.append({"letter": letter, "seat": answers[letter]["seat"],
                      "avg_peer_rank": round(sum(positions) / len(positions), 2) if positions else None,
                      "rankings": len(positions)})
    ranks.sort(key=lambda r: (r["avg_peer_rank"] is None, r["avg_peer_rank"] or 0))

    conf = {"high": 0, "medium": 0, "low": 0, "missing": 0}
    for a in answers.values():
        conf[a["confidence"] or "missing"] += 1

    round3 = OrderedDict()
    if peer_review:
        for c in claims.values():
            base = c["status"].split(" (")[0]
            if base in ("Contested", "Disputed") and "rebuttal" not in c:
                round3.setdefault(c["seat"], []).append(c["id"])
    if rebuttals and round3:
        left = [cid for ids in round3.values() for cid in ids]
        warnings.append(f"round 3 left these challenged claims unanswered: {', '.join(left)}")
        round3 = OrderedDict()

    return {
        "peer_review": peer_review,
        "seats_answered": len(answers),
        "reviews_parsed": len(reviews),
        "seat_confidence": conf,
        "claims": list(claims.values()),
        "peer_ranks": ranks,
        "missed": missed,
        "round3_candidates": round3,
        "rebuttals": rebuttals,
        "seat_names": seat_names,
        "answers": answers,
    }, [], warnings


def sort_key(c):
    base = c["status"].split(" (")[0]
    return (STATUS_ORDER.index(base) if base in STATUS_ORDER else 99, c["letter"], int(c["id"][1:]))


def render(result, warnings):
    names = result["seat_names"]
    out = []
    c = result["seat_confidence"]
    out.append(f"Seats answered: {result['seats_answered']} · reviews parsed: {result['reviews_parsed']}"
               f" · seat confidence: {c['high']} high, {c['medium']} medium, {c['low']} low"
               + (f", {c['missing']} missing" if c["missing"] else ""))
    out.append("")
    if not result["peer_review"]:
        out.append("No REVIEW sections: this is a quick run. Statuses (Shared / Lone / Opposed) are "
                   "the chairman's judgment; this list only collects the claims.")
        out.append("")
    out.append("| ID | Claim | Seat | Votes (agree/dispute/unsure) | Status | Notes |")
    out.append("|---|---|---|---|---|---|")
    for cl in sorted(result["claims"], key=sort_key):
        base = cl["status"].split(" (")[0]
        notes = []
        if base in ("Disputed", "Contested"):
            notes.append("must show")
        if result["peer_review"] and cl["engaged"] <= 1 and base != "Withdrawn":
            notes.append("thin: chairman may override with a reason")
        votes = f"{cl['a']}/{cl['d']}/{cl['u']}" if result["peer_review"] else "n/a"
        out.append(f"| {cl['id']} | {short(cl['claim'])} | {names.get(cl['seat'], cl['seat'])} | "
                   f"{votes} | {cl['status']} | {'; '.join(notes)} |")
    if result["peer_ranks"] and result["peer_review"]:
        out.append("")
        out.append("Peer ranks (lower is better; own-answer rankings excluded):")
        for r in result["peer_ranks"]:
            avg = "n/a" if r["avg_peer_rank"] is None else f"{r['avg_peer_rank']:.2f}"
            out.append(f"- {r['letter']} {names.get(r['seat'], r['seat'])}: {avg} over {r['rankings']} rankings")
    if result["missed"]:
        out.append("")
        out.append("Reviewers' 'missed by every answer':")
        for m in result["missed"]:
            out.append(f"- {names.get(m['by'], m['by'])}: {m['text']}")
    if result["round3_candidates"]:
        out.append("")
        out.append("Round 3 challenged claims (paste each seat's block into its rebuttal brief):")
        by_id = {cl["id"]: cl for cl in result["claims"]}
        for seat, ids in result["round3_candidates"].items():
            out.append("")
            out.append(f"--- {names.get(seat, seat)} ({seat})")
            for cid in ids:
                cl = by_id[cid]
                out.append(f"{cid}: {cl['claim']} - status {cl['status'].split(' (')[0]}")
                for v in cl["votes"]:
                    if v["vote"] in ("dispute", "agree") and v["reason"]:
                        out.append(f"  {v['vote']}: {v['reason']}")
    if result["rebuttals"]:
        out.append("")
        out.append("Round 3 results:")
        for seat, r in result["rebuttals"].items():
            changed = r["changed"] or "unclear"
            out.append(f"- {names.get(seat, seat)}: changed position: {changed}. Final: {r['final_position']}")
        for cl in result["claims"]:
            if cl.get("rebuttal") and cl["rebuttal"]["action"] == "AMEND":
                out.append(f"  - {cl['id']} amended: {cl['rebuttal']['text']}")
    if warnings:
        out.append("")
        out.append("Warnings (fix or re-request the seat before trusting the affected rows):")
        out.extend(f"- {w}" for w in warnings)
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="Tally a council run file.")
    ap.add_argument("run_file", help="path to the run file, or - for stdin")
    ap.add_argument("--json", action="store_true", help="print the full result as JSON")
    args = ap.parse_args()
    try:
        text = sys.stdin.read() if args.run_file == "-" else open(args.run_file, encoding="utf-8").read()
    except OSError as e:
        print(f"Cannot read {args.run_file}: {e}", file=sys.stderr)
        sys.exit(2)
    result, errors, warnings = tally(text)
    if errors:
        print("Run file unusable:\n- " + "\n- ".join(errors), file=sys.stderr)
        sys.exit(1)
    if args.json:
        print(json.dumps({**result, "warnings": warnings}, indent=2, ensure_ascii=False))
    else:
        print(render(result, warnings))
    sys.exit(0)


if __name__ == "__main__":
    main()
