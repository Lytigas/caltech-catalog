import json
import re
from collections import defaultdict

with open("04-pdf_catalog_dump.txt") as f:
    pdf_txt = f.read()

txt_blocks = [block.strip(" ") for block in pdf_txt.split("\n\n")]
# [print("==>\n", repr(block), "\n<==") for block in txt_blocks]
FIRST_BLOCK_PREFIX = "AEROSPACE\n"
first_block_idx = next(
    i for i, v in enumerate(txt_blocks) if v.startswith(FIRST_BLOCK_PREFIX)
)
txt_blocks = txt_blocks[first_block_idx:]

txt_blocks = filter(bool, txt_blocks)  # remove empty strings

# Strip lines that are all caps
def remove_first_line_if_form_feed_prefix(s):
    if s[0] == "\x0c":
        return "".join(s.splitlines(True)[2:])  # \f is its own line
    return s


def strip_course_prefix(s):
    if s.startswith("Courses\f"):
        return s[len("Courses\f") :]
    return s


txt_blocks = map(remove_first_line_if_form_feed_prefix, txt_blocks)
txt_blocks = map(strip_course_prefix, txt_blocks)

PREREQ_FINDER_RE = re.compile("Prerequisites?:.+?\.")


def extract_prereqs_txt(txt_block):
    txt = " ".join(txt_block.splitlines(False))
    matches = PREREQ_FINDER_RE.search(txt)
    if matches:
        return matches[0]
    return None


prereqs_list = []
LABEL_FINDER_RE = re.compile(
    "(\w{1,4}(?:/\w{1,4})*) (\d+(?:/\d+)*)(?: (a|b|c|d|x){0,4})?\."
)

for block in txt_blocks:
    label_matches = LABEL_FINDER_RE.match(block)
    preq = extract_prereqs_txt(block)
    if label_matches and preq:
        prereqs_list.append(
            {
                "number": label_matches[2],
                "depts": label_matches[1],
                "label": label_matches[0],
                "desc_len": len(block),
                "prereqs": extract_prereqs_txt(block),
            }
        )
# merge courses by code, prefering the longer descriptions
preqs_index = defaultdict(list)
for course in prereqs_list:
    preqs_index[course["label"]].append(course)
# verify code slashes matches length
for label, courses in preqs_index.items():
    ct = label.count("/") + 1
    cs = len(courses)
    if ct < cs:
        print(f"Warning: course {label} has {cs} entries for {ct} cross-listings")
# do actual merging
new_preqs_list = []
for courses in preqs_index.values():
    new_entry = max(courses, key=lambda c: c["desc_len"])
    new_preqs_list.append(new_entry)
prereqs_list = new_preqs_list

catalog = json.load(open("02-all_courses_scraped.json"))
# index courses by number
indexed_catalog = defaultdict(list)
for course in catalog:
    label_matches = LABEL_FINDER_RE.match(course["label"])
    if not label_matches:
        print(course)
    number = label_matches[2]
    course["_depts"] = label_matches[1]
    course["_matched"] = False
    course["prerequisites"] = None
    indexed_catalog[number].append(course)


def add_preq_string(course, prereq):
    if course["prerequisites"] is not None:
        print(f"Warning: double match for {course['label']}")
        course["prerequisites"] += prereq
    course["prerequisites"] = prereq


def attempt_exact_match(preq_info, candidate_list):
    # Check for exact matches
    exact_match_ct = 0
    for candidate_course in candidate_list:
        if candidate_course["label"] == preq_info["label"]:
            exact_match_ct += 1
            print(f"matched {preq_info['label']} to {candidate_course['label']}")
            add_preq_string(candidate_course, preq_info["prereqs"])
    if exact_match_ct > 1:
        print(f"Warning: found multiple exact matches for {preq_info['label']}")
    if exact_match_ct >= 1:
        return True
    else:
        return False


def attempt_fuzzy_match(preq_info, candidate_list):
    preq_depts = set(preq_info["depts"].split("/"))
    matching_candidates = []
    for candidate_course in candidates:
        candidate_depts = set(candidate_course["_depts"].split("/"))
        match_len = len(candidate_depts.intersection(preq_depts))
        if match_len > 0:
            matching_candidates.append((candidate_course, match_len))
    matching_candidates.sort(key=lambda tup: tup[1], reverse=True)
    if len(matching_candidates) > 1:
        print(
            f"Warning: found multiple candidates for {preq_info['label']} when matching: {[c[0]['label'] for c in matching_candidates]} Selecting the first."
        )
    if len(matching_candidates) >= 1:
        print(f"matched {preq_info['label']} to {matching_candidates[0][0]['label']}")
        add_preq_string(matching_candidates[0][0], preq_info["prereqs"])
        return True
    else:
        return False


# find the best match in the catalog
for preq_info in prereqs_list:
    candidates = indexed_catalog[preq_info["number"]]
    if attempt_exact_match(preq_info, candidates):
        continue
    print(f"Info: falling back to fuzzy matches for {preq_info['label']}")
    if attempt_fuzzy_match(preq_info, candidates):
        continue
    print(
        f"Warning: found no catalog course to attach found prereqs for {preq_info['label']}"
    )


# delete temporary fields
for course in catalog:
    del course["_depts"]
    del course["_matched"]

json.dump(catalog, open("06-all_courses_prereqs.json", "w"))
