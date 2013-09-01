#!/bin/bash

searchdir=$1

if [ "$#" -ne 1 ]; then
echo -e "1 arg required\nexample: numlines.sh \"src/*\""
exit
fi

tmp="tmp_numlines"
echo "" > $tmp
for file in $searchdir; do wc -l $file | cut -f1 -d" " >> $tmp; done
awk '{s+=$1} END {print s}' $tmp
rm -f $tmp
