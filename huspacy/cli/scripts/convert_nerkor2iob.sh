#!/bin/bash

#echo $i

#cat -s "$1" \
#  | awk -F $'\t' 'BEGIN {id=0; OFS=FS} NF==0 {id=0; print} NF>0 && substr($1, 1, 1) != "#" {id=id+1; print $1,$6}' \
#  > "$2"
  
find . -wholename "$1" -print \
  | xargs cat -s \
  | awk -F $'\t' 'BEGIN {id=0; OFS=FS} NF==0 {id=0; print} NF>0 && substr($1, 1, 1) != "#" {id=id+1; print $1,$6}' \
  > "$2"