#!/bin/bash
mywd=$(pwd)
for X in "$@"
do	
	cp analysis.py $X
	cd $X
        python3 analysis.py
	cd ..
done

python3 rel_summary_seed.py "$@"

