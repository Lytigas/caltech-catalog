SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

webapp: 09-all_courses_with_prereqs.json
.PHONY: webapp

05-all_courses_with_codes.json: 03-all_courses_hand_fixed.json 04-canonicalizer.py
	python3 04-canonicalizer.py

07-all_courses_merged.json: 05-all_courses_with_codes.json 06-merger.py
	python3 06-merger.py

09-all_courses_with_prereqs.json: 07-all_courses_merged.json 08-add_prereqs.py
	python3 08-add_prereqs.py
