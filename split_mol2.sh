#/bin/bash

i=-1
start=1
chunk=1

while read line; do
  ((i++))
  if [ "$i" == $2 ]; then
    end=$(($line - 1))
    sed -n $start,${end}p $1 > ${1%.mol2}_chunk${chunk}.mol2
    start=$line
    i=0
    ((chunk++))
  fi
done < <(grep -Fn "@<TRIPOS>MOLECULE" $1 | cut -d: -f1)

# save last chunk
sed -n $start,'$p' $1 > ${1%.mol2}_chunk${chunk}.mol2
