#!/usr/bin/env bash

for f in *_chain*.pdb; do
  DIR=$(basename ${f%.*})
  mkdir ${DIR}
  cp ${f} ${DIR}/${f}
  SPORES --mode splitpdb ${DIR}/${f}
done
