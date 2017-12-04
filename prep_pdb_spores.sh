#!/usr/bin/env bash

for f in "$@"; do
  FILE_NAME=$(basename ${f})
  INPUT_DIR=$(dirname ${f})
  NEW_DIR=$(basename ${f%.*})
  mkdir ${INPUT_DIR}/${NEW_DIR}
  cp ${f} ${INPUT_DIR}/${NEW_DIR}/${FILE_NAME}
  SPORES --mode splitpdb ${INPUT_DIR}/${NEW_DIR}/${FILE_NAME}
done
