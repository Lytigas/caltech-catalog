import json
import re

catalog = json.load(open("03-all_courses_hand_fixed.json"))

# Canonical format is
# AA/BB/Cc/Dd 10
# note lack of abc, period, or leading zeroes
# note alphabetical code

from common import CODE_FINDER_RE, canonicalize

# canonicalize course names
for course in catalog:
    name = course["title"].strip()
    code = CODE_FINDER_RE.match(name)[0]
    course["code"] = canonicalize(code)

json.dump(catalog, open("05-all_courses_with_codes.json", "w"))
