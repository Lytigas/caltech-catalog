jq -c '[ .[] | {code, c_prereq} ]' < ../09-all_courses_with_prereqs.json > public/data.json
