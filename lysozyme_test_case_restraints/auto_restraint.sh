#!/bin/bash

for X in "$@"
do
        echo =====  $X  =======================

        cd $X
	cp ../auto_restraint_files/* .
        python3 restraint_analysis.py 0.5 md-complex/BB.avg.dat md-complex/BB2.avg.dat setup/lig_tleap.mol2 complex-repres.pdb
        #float argument is the chosen cutoff fraction
        cd ..
done

