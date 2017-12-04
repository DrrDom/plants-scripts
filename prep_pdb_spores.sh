#!/usr/bin/env bash

# specify pdb file as command line arguments
# EXAMPLE:
# prep_pdb_spores.sh *_chain_*.pdb

INPUT_DIR=$(realpath $(dirname $1))

N=30
(
for f in "$@"; do
  ((i=i%N)); ((i++==0)) && wait
  FILE_NAME=$(basename ${f})
  NEW_DIR=$(basename ${f%.*})
  cd ${INPUT_DIR}
  mkdir ${NEW_DIR}
  cp ${f} ${NEW_DIR}/${FILE_NAME}
  cd ${NEW_DIR}
  SPORES_linux32bit --mode splitpdb ${FILE_NAME} &
done
)
