#!/bin/bash
#mywd=$(pwd)
date; echo
ls -1 "$@"
echo -n "  Total: "
ls -1 "$@"| wc -l
echo

mkdir out 

for X in "$@"
do
        echo =====  $X  =======================
	X_LIGNAME=$(basename -- "$X")
	#echo "${X_LIGNAME%.*}".txt
        
	./prep-lig-resp-g09.sh $X &> out/"${X_LIGNAME%.*}".txt
        echo
done

