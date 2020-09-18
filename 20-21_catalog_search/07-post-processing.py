import json

catalog = json.load(open("06-all_courses_prereqs.json"))


def remove_prefix_if(s, prefix):
    if s.startswith(prefix):
        return s[len(prefix) :]
    return s


def attempt_remove_prefixes(course, key, prefixes):
    if not course[key]:
        return
    for p in prefixes:
        course[key] = remove_prefix_if(course[key], p)


for course in catalog:
    attempt_remove_prefixes(
        course,
        "instructors",
        ["Instructors: ", "Instructors:", "Instructor: ", "Instructor:"],
    )
    attempt_remove_prefixes(
        course,
        "prerequisites",
        ["Prerequisites: ", "Prerequisites:", "Prerequisite: ", "Prerequisite:"],
    )


json.dump(catalog, open("08-final_catalog.json", "w"))
