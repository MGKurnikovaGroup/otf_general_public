#!/bin/bash

#mywd=$(pwd)

for X in "$@"
do
        echo =====  $X  =======================
        X_LIGNAME=$(basename -- "$X")
        #echo "${X_LIGNAME%.*}".txt

        ./prep-lig-resp-g16.sh $X &> out."${X_LIGNAME%.*}".txt
        
		echo
done
