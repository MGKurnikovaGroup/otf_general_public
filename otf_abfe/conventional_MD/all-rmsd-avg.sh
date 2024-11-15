#!/bin/bash
mypcl=$(realpath $(find ~/ -type d -name "otf_abfe"))
mywd=$(pwd)
for X in "$@"
do
        echo =====  $X  =======================
        cd $X/md-complex/
	cpptraj -i $mypcl/conventional_MD/cpp.rmsd-avg.in
        cd $mywd
	echo
done

