#!/bin/bash
mywd=$(pwd)
mypcl=~/protocols/lys_abfe_10/

for X in "$@"
do
	cd $X
	cp $mypcl/*.py .
	python3 dcrg_main.py $mypcl
	python3 rtr_main.py $mypcl
	python3 water_main.py $mypcl
	cd ..
	mv $X ~/trajectories2/abfe_updated_protocol/10ns/ntr_change
done
