import json
import re
from collections import defaultdict

catalog = json.load(open("07-all_courses_merged.json"))

from common import CODE_FINDER_RE_NOCAP, parse_code, canonicalize as cancode

# create index by number
index = defaultdict(list)
codeset = set()
for course in catalog:
    _dept, num = parse_code(course["code"])
    index[num].append(course["code"])
    codeset.add(course["code"])

# This documents fucky things in the catalog as of writing
MANUAL_REWRITE_RULES = {
    "AM 125": None,  # as far as I can tell this course never existed
    "ME 35": None,  # this one no longer exists
    "FOR 140": None,  # comes from the phrase "For 140 a" referring to the a part of the same course
    "OR 146": None,  # literally "Prerequisites: or 146 or consent of the instructor" wtf
    "OR 156": None,  # "Prerequisites: CS 38 and CS 155 or 156a."
    "MATH 120": "MA 120",  # really guys, 3 of these
    "MATH 2": "MA 2",
    "MATH 1": "MA 2",
    "ACM 100": "ACM 95",  # this course has two names
    "PH/A 125": "PH 125",  # this stems from the phrase "Ch 125 a/Ph 125 a"
}

for course in catalog:
    pr = CODE_FINDER_RE_NOCAP.findall(course["prereq"])
    # occassionally pre-reqs arent listed in their proper
    # cross-listed format. We best-effort resolve these here
    def canonicalize(p):
        p = cancode(p)
        if p in MANUAL_REWRITE_RULES:
            p = MANUAL_REWRITE_RULES[p]
            if p is None:
                return None
        if p in codeset:
            return p
        dept, num = parse_code(p)
        if num in index:
            candidates = []
            questioning_segments = set(dept.split("/"))
            for candidate_code in index[num]:
                candidate_code_segments = set(parse_code(candidate_code)[0].split("/"))
                if len(questioning_segments.intersection(candidate_code_segments)) > 0:
                    candidates.append(candidate_code)
            if len(candidates) > 1:
                print(
                    f"Warning: found multiple candidates for {p} when canonicalizing: {candidates}. Selecting the first."
                )
            if len(candidates) <= 0:
                print(
                    f"Warning: found no candidates for code {p} when canonicalizing. Will return as-is"
                )
                return p
            return candidates[0]
        else:
            print(
                f"Warning: found no candidates for code {p} when canonicalizing. Will return as-is"
            )
            return p

    print(course["prereq"])
    print(pr)
    pr = [canonicalize(p) for p in pr]
    course["c_prereq"] = [p for p in pr if p is not None]

json.dump(catalog, open("09-all_courses_with_prereqs.json", "w"))
