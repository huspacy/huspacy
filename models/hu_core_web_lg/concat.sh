#!/bin/bash

find . -wholename "$1" -print \
  | xargs cat \
  | grep -v "^#" \
  | awk -F $'\t' 'BEGIN {id=0; OFS=FS} NF==0 {id=0; print} NF>0 {id=id+1; print id, $1,$2,$3,$4,$5,"_","_","_",$6}' \
  > "$2"