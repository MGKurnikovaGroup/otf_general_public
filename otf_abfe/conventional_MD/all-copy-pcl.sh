#!/bin/bash
mywd=$(pwd)
mypcl=$(realpath $(find ~/ -type d -name "otf_abfe"))

for X in "$@"
do
        echo =====  $X  =======================
	cp $mypcl/conventional_MD/pcl-md-complex/* $X/md-complex/
	ls $X/md-complex/
done

