#!/bin/bash
mywd=$(pwd)
for X in "$@"
do	
	cp analysis.py convergence_test.py $X
	cd $X
        python3 analysis.py
	cd ..
done

python3 gp_summary.py "$@"
ls
