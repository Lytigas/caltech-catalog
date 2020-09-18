SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

webapp:
	(cd 19-20_classtrees; $(MAKE) webapp)
	jq -c '[ .[] | {code, c_prereq} ]' < 19-20_classtrees/09-all_courses_with_prereqs.json > app/public/trees/data.json
	(cd 20-21_catalog_search; $(MAKE) webapp)
	cp 20-21_catalog_search/08-final_catalog.json app/public/search/data.json
