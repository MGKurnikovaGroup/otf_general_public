#!/bin/bash
mywd=$(pwd)
for X in "$@"
do
        echo =====  $X  =======================
        cd $X/md-complex/
	../../cpp.get-repres-pdb.sh
	mv complex-repres.* ../
        cd $mywd
	echo
done

