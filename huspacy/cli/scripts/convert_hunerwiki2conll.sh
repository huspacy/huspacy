#!/bin/bash

zcat $1 \
  | awk -F $'\t' 'BEGIN {id=0; OFS=FS} NF==0 {id=0; print} NF>0 {id=id+1; print $1,$6}' \
  > "$2"