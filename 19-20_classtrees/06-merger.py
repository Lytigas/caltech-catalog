import json
from collections import defaultdict

catalog = json.load(open("05-all_courses_with_codes.json"))

# TODO: envisage a better way to keep track of a/b/c etc
# Some course are listed separately, some together
# Eg Ma 1 abc vs Ge 114 a Ge 114 b

# merge courses by code, prefering the longer descriptions
index = defaultdict(list)
for course in catalog:
    index[course["code"]].append(course)
# verify code slashes matches length
for code, courses in index.items():
    ct = code.count("/") + 1
    cs = len(courses)
    if ct != cs:
        print(f"Warning: course {code} has {cs} entries for {ct} cross-listings")
# do actual merging
new_catalog = []
for courses in index.values():
    new_entry = max(courses, key=lambda c: len(c["desc"]))
    # merge prereqs
    new_entry["prereq"] = "|".join([str(c["prereq"]) for c in courses])
    new_catalog.append(new_entry)


json.dump(new_catalog, open("07-all_courses_merged.json", "w"))
