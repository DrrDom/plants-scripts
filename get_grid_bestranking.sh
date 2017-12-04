#!/bin/bash

# collect bestranking files from all subdirs
# print dir name + first two fields from bestranking file (mol_name, score)

# DIR=$HOME/IMTM/eEF2/u5/dock_plants/grid_dock_01

# find $DIR -name "bestranking.csv" | while read f; do
find . -name "bestranking.csv" | while read f; do
  LOCAL_DIR=`dirname $f`
  LOCAL_DIR=`basename $LOCAL_DIR`
#  echo $f
#  echo $LOCAL_DIR
#  awk -v var="$LOCAL_DIR" -F"," '{if (NR!=1) {print LOCAL_DIR, $1, $2}}' $f
  sed "1d" $f | cut -d',' -f1-2 | sed "s/^/${LOCAL_DIR},/"
done
