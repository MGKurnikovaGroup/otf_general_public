#!/bin/bash
_d="$(pwd)"
echo "$_d"
mypcl=$(realpath $(find ../ -type d -name "otf_rbfe"))

for X in "$@"
do
	cd $X
	python3 site_water_equal_1.py ~/protocols/ALK2_otf "$_d"/$X/scmask.txt --initial_time 2.5
	cd ..
	mv $X ~/trajectories2/ALK2/cluster8
done
