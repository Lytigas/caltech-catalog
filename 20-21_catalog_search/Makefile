SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

webapp: 08-final_catalog.json
.PHONY: webapp

06-all_courses_prereqs.json: 04-pdf_catalog_dump.txt 02-all_courses_scraped.json 05-add-prereqs.py
	python3 05-add-prereqs.py

08-final_catalog.json: 06-all_courses_prereqs.json 07-post-processing.py
	python3 07-post-processing.py
