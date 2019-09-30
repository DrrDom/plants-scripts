#/bin/bash

# $1 - mol2 file
# $2 - number of molecules per split
# $3 - plantsconfig file for input mol2 file

# the script splits mol2 on chunks and created new plantsconfig files and run them all

DIR_SCRIPT=$(dirname $0)

${DIR_SCRIPT}/split_plants_task.sh $1 $2 $3

for f in ${3}.chunk*; do
  PLANTS --mode screen $f &
done

