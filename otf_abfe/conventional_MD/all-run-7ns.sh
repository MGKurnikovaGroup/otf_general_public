#!/bin/bash
mywd=$(pwd)

for X in "$@"
do
        echo =====  $X  =======================
	cd $X/md-complex/
        chmod +x run-7ns.sh	
	./run-7ns.sh

	cd $mywd
done

