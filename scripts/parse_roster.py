#!/usr/bin/env python3
"""Parse an NIH eRA public roster page into structured JSON, and diff two rosters.

Works on three page types from public.era.nih.gov/pubroster/:
  - SEP meeting rosters        preSepIndex.era?CID=...&AGENDA=...
  - Chartered meeting rosters  preRosIndex.era?AGENDA=...&CID=...   ("*" marks temporary members)
  - Chartered membership lists roster.era?CID=...                   ("(27)" = term ends 6/30/2027)

The sandbox shell usually cannot reach nih.gov, so the normal flow is:
  1. Fetch the page with the web_fetch tool.
  2. Save the returned text (markdown or HTML, either works) to a file.
  3. python3 parse_roster.py page.txt --url <source url> -o roster.json
  4. python3 parse_roster.py new.json --diff old.json     (prints who joined/left)

If given an http(s) URL instead of a file, the script tries to download it and
tells you to fall back to web_fetch if that fails.
"""
import argparse
import datetime as dt
import html
import json
import re
import sys
import urllib.request

DEGREE_TOKENS = {
    "MD", "PHD", "DVM", "DDS", "DMD", "MPH", "MS", "MSC", "MA", "MBA", "MHS", "MSCE",
    "MBBS", "MDCM", "RN", "BSN", "MSN", "DNP", "PHARMD", "DO", "SCD", "DRPH", "MBCHB",
    "JD", "BS", "BA", "FRCP", "FRCPC", "FASN", "MMSC", "MSCI", "MSHP", "EDD", "PSYD",
}
SECTION_HEADS = {
    "CHAIRPERSON": "chair",
    "CO-CHAIRPERSON": "chair",
    "MEMBERS": "member",
    "MEMBER": "member",
    "ROSTER": "member",
    "SCIENTIFIC REVIEW OFFICER": "sro",
    "SCIENTIFIC REVIEW ADMINISTRATOR": "sro",
    "EXTRAMURAL SUPPORT ASSISTANT": "esa",
    "GRANTS TECHNICAL ASSISTANT": "esa",
}
NAME_RE = re.compile(r"^\*?\s*([A-Z][A-Z'\-\. ]+?),\s*(.+?)\s*(\(\d{2}\))?\s*(\*)?\s*$")


def load_text(src):
    if re.match(r"^https?://", src):
        try:
            req = urllib.request.Request(src, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                raw = r.read().decode("latin-1", errors="replace")
        except Exception as e:  # noqa: BLE001
            sys.exit(
                f"Could not download {src} ({e}).\n"
                "Fetch it with the web_fetch tool, save the text to a file, and pass the file path instead."
            )
    else:
        with open(src, encoding="utf-8", errors="replace") as f:
            raw = f.read()
    if "<html" in raw.lower() or "<br" in raw.lower():
        raw = re.sub(r"(?i)<br\s*/?>", "\n", raw)
        raw = re.sub(r"(?i)</(p|div|tr|li|h\d)>", "\n", raw)
        raw = re.sub(r"<[^>]+>", "", raw)
        raw = html.unescape(raw)
    return raw


def clean(line):
    line = line.replace("\\-", "-").replace(" ", " ")
    line = re.sub(r"[*_]{2,}", "", line)  # markdown bold
    line = re.sub(r"^#+\s*", "", line)
    return line.strip().rstrip("\\").strip()


def split_name(first_line):
    m = NAME_RE.match(first_line)
    if not m:
        return None
    last, rest, term, star = m.group(1).strip(), m.group(2), m.group(3), m.group(4)
    temporary = bool(star) or first_line.startswith("*")
    parts = [p.strip() for p in rest.split(",") if p.strip()]
    first_parts, degrees = [], []
    for p in parts:
        tok = p.replace(".", "").replace(" ", "").upper()
        if tok in DEGREE_TOKENS or (degrees and tok.isalpha() and len(tok) <= 6 and tok.isupper()):
            degrees.append(p.upper())
        else:
            first_parts.append(p)
    term_end = None
    if term:
        yy = int(term.strip("()"))
        term_end = f"20{yy:02d}-06-30"
    return {
        "last": last.title(),
        "first": " ".join(first_parts).title(),
        "degrees": degrees,
        "term_end": term_end,
        "temporary": temporary,
        "slug": re.sub(r"[^a-z0-9]+", "-", last.lower()).strip("-"),
    }


def parse(text, url=None):
    lines = [clean(l) for l in text.splitlines()]
    out = {
        "source_url": url,
        "parsed_on": dt.date.today().isoformat(),
        "page_type": None,
        "committee_code": None,
        "committee_title": None,
        "meeting_dates": None,
        "people": [],
    }
    joined = "\n".join(lines)
    if "Roster Committee Members" in joined or "Terms end 6/30" in joined:
        out["page_type"] = "chartered_membership"
    elif "SPECIAL EMPHASIS PANEL" in joined.upper() or "SEP" in joined and "Meeting Roster" in joined:
        out["page_type"] = "sep_meeting"
    elif "Meeting Roster" in joined:
        out["page_type"] = "chartered_meeting"

    m = re.search(r"(ZRG\d\s+[A-Z]+\s*-\s*[A-Z0-9]+\s*\(\d+\))", joined)
    if m:
        out["committee_code"] = re.sub(r"\s+", " ", m.group(1))
    m = re.search(r"(\d{2}/\d{2}/\d{2,4})\s*-\s*(\d{2}/\d{2}/\d{2,4})", joined)
    if m:
        out["meeting_dates"] = [m.group(1), m.group(2)]
    for i, l in enumerate(lines):
        if l.endswith("Study Section") or l.endswith("Review Committee"):
            out["committee_title"] = l
            break
        if out["committee_code"] and out["committee_code"].split("(")[0].replace(" ", "") in l.replace(" ", ""):
            for nxt in lines[i + 1 : i + 4]:
                if nxt and nxt.isupper() and not re.search(r"\d", nxt):
                    out["committee_title"] = nxt.title()
                    break
            if out["committee_title"]:
                break

    role = None
    block = []

    def flush():
        nonlocal block
        if block and role in ("chair", "member", "sro", "esa"):
            info = split_name(block[0])
            if info:
                info["role"] = role
                info["position_lines"] = block[1:]
                out["people"].append(info)
        block = []

    started = False
    for l in lines:
        head = l.rstrip(":").strip().upper()
        if head in SECTION_HEADS and not block:
            # a section heading only counts at the start of a block; inside a block
            # "SCIENTIFIC REVIEW OFFICER" is just the SRO's job title
            flush()
            role = SECTION_HEADS[head]
            started = True
            continue
        if not started:
            continue
        if re.fullmatch(r"-{3,}", l) or l.startswith("* * *"):
            continue
        if not l:
            flush()
            continue
        if l.startswith("[") or l.startswith("- [") or "eRA Logo" in l:
            flush()
            role = None
            continue
        if re.fullmatch(r"\*\s*(Temporary Member|Flexible)", l):
            continue
        # chartered rosters list members right after the chair with no MEMBERS header
        if role == "chair" and block == [] and any(p["role"] == "chair" for p in out["people"]):
            role = "member"
        block.append(l)
    flush()
    return out


def key(p):
    return (p["last"].upper(), p["first"].split(" ")[0].upper() if p["first"] else "")


def diff(new, old):
    def reviewers(r):
        return {key(p): p for p in r["people"] if p["role"] in ("chair", "member")}

    n, o = reviewers(new), reviewers(old)
    added = [n[k] for k in n if k not in o]
    removed = [o[k] for k in o if k not in n]
    changed = []
    for k in n.keys() & o.keys():
        a, b = n[k], o[k]
        if a["role"] != b["role"] or a["position_lines"] != b["position_lines"] or a["term_end"] != b["term_end"]:
            changed.append({"name": f'{a["last"]}, {a["first"]}', "old": b, "new": a})
    return {"added": added, "removed": removed, "changed": changed,
            "new_sro": [p for p in new["people"] if p["role"] == "sro"],
            "old_sro": [p for p in old["people"] if p["role"] == "sro"]}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", help="saved roster text/HTML file, a URL, or (with --diff) a parsed JSON")
    ap.add_argument("--url", help="original URL, recorded in the output")
    ap.add_argument("-o", "--out", help="write JSON here (default: stdout)")
    ap.add_argument("--diff", metavar="OLD_JSON", help="compare SOURCE (parsed JSON or raw page) to OLD_JSON")
    a = ap.parse_args()

    if a.source.endswith(".json"):
        with open(a.source) as f:
            data = json.load(f)
    else:
        data = parse(load_text(a.source), a.url or (a.source if a.source.startswith("http") else None))

    if a.diff:
        with open(a.diff) as f:
            old = json.load(f)
        result = diff(data, old)
        for label in ("added", "removed"):
            print(f"{label.upper()} ({len(result[label])}):")
            for p in result[label]:
                print(f'  {p["last"]}, {p["first"]} {", ".join(p["degrees"])} [{p["role"]}] {" / ".join(p["position_lines"][:1] + p["position_lines"][-2:-1])}')
        print(f'CHANGED ({len(result["changed"])}):')
        for c in result["changed"]:
            print(f'  {c["name"]}: role {c["old"]["role"]}->{c["new"]["role"]}; term {c["old"]["term_end"]}->{c["new"]["term_end"]}')
        so = {key(p) for p in result["old_sro"]}
        sn = {key(p) for p in result["new_sro"]}
        if so != sn:
            print("SRO CHANGED:", [f'{p["last"]}, {p["first"]}' for p in result["new_sro"]])
        return

    js = json.dumps(data, indent=2)
    if a.out:
        with open(a.out, "w") as f:
            f.write(js + "\n")
        n = sum(p["role"] in ("chair", "member") for p in data["people"])
        print(f'Wrote {a.out}: {data["page_type"]}, {data["committee_code"] or data["committee_title"]}, {n} reviewers')
    else:
        print(js)


if __name__ == "__main__":
    main()
