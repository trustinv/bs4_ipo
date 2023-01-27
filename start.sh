#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

WORKDIR="/ipo_crawler"

# python $WORKDIR/apps/ipo/main.py
python apps/ipo/main.py
