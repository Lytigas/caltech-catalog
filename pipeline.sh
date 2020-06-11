#!/usr/bin/env sh

set -e

python3.8 04-canonicalizer.py
python3.8 06-merger.py
python3.8 08-add_prereqs.py
sh 11-gen-graph.sh
