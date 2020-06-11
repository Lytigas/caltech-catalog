import re

CODE_FINDER_RE = re.compile("(\w{1,4}(?:/\w{1,4})*) (\d+)")
CODE_FINDER_RE_NOCAP = re.compile("\w{1,4}(?:/\w{1,4})* \d+")


def parse_code(valid_code):
    matches = CODE_FINDER_RE.fullmatch(valid_code)
    return str(matches[1]), int(matches[2])


def canonicalize(valid_code):
    dept, num = parse_code(valid_code)
    dept = "/".join(sorted(dept.split("/")))
    return (dept + " " + str(num)).upper()
