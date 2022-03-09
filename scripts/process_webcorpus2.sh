#!/bin/bash

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
PREPROCESS_SCRIPT=$SCRIPT_DIR/../tools/cli/preprocess_webcorpus.py
OUT_DIR=$2

wget -q -O - https://nessie.ilab.sztaki.hu/~ndavid/Webcorpus2_clean/$1 \
    | zcat \
    | grep "# text =" \
    | cut -c 10- \
    | $PREPROCESS_SCRIPT \
    > $OUT_DIR/${1::-7}.txt
echo "$1 ✔️"
