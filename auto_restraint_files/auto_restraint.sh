#!/bin/bash

for X in "$@"
do
        echo =====  $X  =======================

        cd $X
	cp ../auto_restraint_files/* .
	./cpptraj.restraint.sh
        python3 restraint_analysis.py 0.5
        #argument is the chosen cutoff fraction
        cd ..
done

