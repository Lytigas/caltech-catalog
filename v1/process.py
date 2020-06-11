import sys
import json
import re

EXTRACT_SHORTNAME = re.compile(".*?([0-9]+).*?")

PREREQ_FINDER = re.compile("[a-zA-Z/]+ [0-9]+")

file = sys.argv[1]

rawdata = json.loads(open(file, "r").read())

classes = []

PR_CTR = 1

for c in rawdata:
    name = c["title"]
    shortname = "CS" + EXTRACT_SHORTNAME.match(name)[1]
    units = c["em0"]
    prereq_desc = c["em1"] if c["em1"] and c["em1"].startswith("Prerequisite") else None
    prereqs = PREREQ_FINDER.findall(prereq_desc) if prereq_desc else None

    def filter_prereq(pr):
        global PR_CTR
        if "CS" in pr:
            return "CS" + EXTRACT_SHORTNAME.match(pr)[1]
        elif "Ma" in pr:
            return "Ma" + EXTRACT_SHORTNAME.match(pr)[1]
        else:
            PR_CTR += 1
            return "non_cs_ma_" + str(PR_CTR)

    prereqs = [filter_prereq(x) for x in prereqs] if prereqs else None

    desc = c["desc"]
    classes.append(
        {
            "name": name,
            "number": shortname,
            "units": units,
            "prereq_desc": prereq_desc,
            "prereqs": prereqs,
            "desc": desc,
        }
    )


filtered = classes
# filter cross-listed courses
# filtered = [x for x in filtered if not x["desc"].startswith("For course desc")]
# filtered = [x for x in filtered if not "/" in x["name"]]
# filter courses w/ out prereqs
filtered = [x for x in filtered if x["prereqs"]]

# output DOT
print("digraph g {")
print("rankdir=LR;")
for c in filtered:
    # print(f'{c["number"]}', end="")
    print(f'{c["number"]} [label="{c["name"]}"]', end="")
for c in filtered:
    pr = c["prereqs"]
    if not pr:
        continue
    print(f'{c["number"]} -> {{ {" ".join(pr)} }}')


print("}")
