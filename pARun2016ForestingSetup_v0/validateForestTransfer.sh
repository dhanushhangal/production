#!/bin/bash
if [ $# -lt 1 ]
then
  echo "Usage: ./validateForestTransfer.sh <version>"
  exit 1
fi

for i in `cat expressrunstoprocess` 
do
	num_lines=$(cat lists/ExpressPhysics.$i.${1}.list | wc -l)
	out_files=$(echo "$i" | eval `awk -F "284" '{print "eos ls /store/group/phys_heavyions/kjung/ExpressForests/v1/000/284/"$2}'` | wc -l)
	if [ "$num_lines" != "$out_files" ]; then
		echo "$i is not finished!"
	else
		echo "run $i is fully transferred"
	fi 
	
done

