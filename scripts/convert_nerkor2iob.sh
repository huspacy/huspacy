#!/bin/bash

pattern=$1
dir=${pattern%%/*}
find $dir -wholename "$pattern" -print | xargs cat -s \
  | awk -F $'\t' 'BEGIN {id=0; OFS=FS} NF==0 {id=0; print} NF>0 && substr($1, 1, 1) != "#" {id=id+1; print $1,$NF}' \
  > "$2"