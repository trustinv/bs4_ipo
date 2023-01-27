#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

WORKDIR="/ipo_crawler"

echo '크롤링을 시작합니다'
python $WORKDIR/apps/ipo/main.py
/bin/bash
