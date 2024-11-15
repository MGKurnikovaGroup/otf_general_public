#!/bin/bash

mywd=$(pwd)
for X in "$@"
do
        echo =====  $X  =======================
        cd $X/md-complex/
	cpptraj -i ../../cpp.rmsd-avg.in
        cd $mywd
	echo
done

