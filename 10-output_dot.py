import json
from common import canonicalize

USE_LABELS = False
HIGHLIGHT_COURSES = []
HIGHLIGHT_COURSES = ["AY 219", "CDS 243"]
HIGHLIGHT_COLORS = ["red", "blue"]
DRAW_NON_HIGHLIGHTED = False


catalog = json.load(open("09-all_courses_with_prereqs.json"))

# convert all codes to dot-compatible ids
dot = lambda x: x.replace(" ", "_").replace("/", "_")
for course in catalog:
    course["code"] = dot(course["code"])
    course["c_prereq"] = [dot(p) for p in course["c_prereq"]]
HIGHLIGHT_COURSES = [dot(canonicalize(c)) for c in HIGHLIGHT_COURSES]


# build index
index = {}
for course in catalog:
    index[course["code"]] = course


# dfs on index to add path
def dfs(course_code, index, color, dot_lines, seen):
    # print(f"finding course code {course_code}")
    seen.add(course_code)
    dot_lines.append(f"{course_code} [color={color}]")
    for pr_code in index[course_code]["c_prereq"]:
        # note that we DO add the edge, then we check if visited
        # even if we've visited the node, we want to draw the new edge to it
        dot_lines.append(f"{course_code} -> {pr_code} [color={color}]")
        if pr_code in seen:
            continue
        dfs(pr_code, index, color, dot_lines, seen)


dot_lines = []
for course, color in zip(HIGHLIGHT_COURSES, HIGHLIGHT_COLORS):
    dfs(course, index, color if color else "red", dot_lines, set())

# These are filters for courses that arent explicitly traced
filtered = catalog
# filter courses w/ out prereqs
filtered = [x for x in filtered if x["c_prereq"]]
# only show courses from a set of departments
# filtered = [x for x in filtered if any(d in x["code"] for d in ["CS", "MA"])]

# output DOT
print("strict digraph g {")
print("rankdir=LR;")
if DRAW_NON_HIGHLIGHTED:
    for c in filtered:
        if USE_LABELS:
            print(f'{c["code"]} [label="{c["title"].strip()}"]', end="")
        else:
            print(f'{c["code"]}', end="")
        # print("[repulsiveforce=2]", end="")
        print()
    for c in filtered:
        pr = c["c_prereq"]
        if not pr:
            continue
        print(f'{c["code"]} -> {{ {" ".join(pr)} }}')

for line in dot_lines:
    print(line)

print("}")
