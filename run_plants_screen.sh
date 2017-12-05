#!/usr/bin/env bash

# $1 - path to dir from which all plantsconfig* files found in all subdirs recursively will be run
# unsafe for path with spaces

N=30

i=0

for f in $(find $1 -name "plantsconfig*" -type f); do
    i=$((i+1))
    j=$((i%N))
    if [ $j -eq 0 ]
    then
      wait
    fi
    PLANTS1.2 --mode screen ${f} > /dev/null 2>&1 &
done
