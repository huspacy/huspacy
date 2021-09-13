#!/bin/bash

cat $1 | awk 'BEGIN{FS="\t"; OFS=FS} length($0) > 0 {if (substr($2, 1,1) == "I" && substr(prev, 1,1) == "O"){print $1, "B" substr($2, 2)} else {print}; prev=$2} length($0) == 0 {print}' > $2