#/bin/bash

# $1 - mol2 file
# $2 - number of molecules per split
# $3 - plantsconfig file for input mol2 file

DIR_SCRIPT=$(dirname $0)

${DIR_SCRIPT}/split_mol2.sh $1 $2

v=$1
chunk=1
for f in ${v%.mol2}_chunk*.mol2; do
  CONFIG_NEW=$3.chunk${chunk}
  v=$(grep "^output_dir" $3)
  sed "s/${v}/${v}\/${chunk}/" $3 > ${CONFIG_NEW}
  sed -i "s/$(basename $1)/$(basename $f)/" ${CONFIG_NEW}
  ((chunk++))
done

