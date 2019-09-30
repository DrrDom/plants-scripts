#/bin/bash

i=0
start=1
chunk=1
grep -Fn "@<TRIPOS>MOLECULE" $1 | cut -d: -f1 | while read line; do
  ((i++))
  if [ "$i" == $2 ]; then
    end=$(($line - 1))
    sed -n $start,${end}p $1 > ${1%.mol2}_chunk${chunk}.mol2
    start=$line
    i=1
    ((chunk++))
  fi
done
