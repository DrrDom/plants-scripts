#!/usr/bin/env bash

# collect bestranking files from all subdirs
# print dir name + first two fields from bestranking file (mol_name, score)

# DIR=$HOME/IMTM/eEF2/u5/dock_plants/grid_dock_01

# find $DIR -name "bestranking.csv" | while read f; do
find $1 -name "bestranking.csv" | while read f; do
  LOCAL_DIR=`dirname $f`
#  LOCAL_DIR=`basename $LOCAL_DIR`
  LOCAL_DIR=$(echo ${LOCAL_DIR} | tr / ,)
  sed "1d" $f | cut -d',' -f1-2 | awk -v prefix="$LOCAL_DIR" -F"," '{print prefix","$0}'
#  sed "1d" $f | cut -d',' -f1-2 | sed "s/^/${LOCAL_DIR},/"
done
