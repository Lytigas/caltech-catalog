#!/usr/bin/env bash

set -euxo pipefail

pip install -r 20-21_catalog_search/requirements.txt
make webapp
