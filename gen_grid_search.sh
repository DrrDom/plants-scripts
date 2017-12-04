#!/usr/bin/env bash

# gen_grid_search.sh ligand.mol2 .
# $1 - path to ligand.mol2
# #2 - path to dir with chain subdirs with protein.mol2

LIGAND_FILE=$1

find $2 -name "*_chain_*" -type d | while read d; do
  echo $d
  gen_plantsconfig_grid_search.py -p ${d}/protein.mol2 -l ${LIGAND_FILE} -d ${d}/grid_search
done
