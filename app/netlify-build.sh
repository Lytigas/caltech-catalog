#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd "$DIR"

cd ..
python3.7 04-canonicalizer.py
python3.7 06-merger.py
python3.7 08-add_prereqs.py

cd "$DIR"
sh strip-data.sh
