#!/bin/bash
mywd=$(pwd)
mypcl=~/protocols/alk2_absolute_g

for X in "$@"
do
	cd $X
	cp $mypcl/*.py .
	# python3 dcrg_main.py $mypcl --initial_time 0.5 --additional_time 0.25
	# python3 rtr_main.py $mypcl --initial_time 0.5 --additional_time 0.25
	# python3 water_main.py $mypcl --initial_time 0.5 --additional_time 0.25
	python3 abfe_main.py $mypcl dcrg --initial_time 0.5 --additional_time 0.25
	python3 abfe_main.py $mypcl rtr --initial_time 0.5 --additional_time 0.25
	python3 abfe_main.py $mypcl water --initial_time 0.5 --additional_time 0.25
	cd ..
	mv $X ~/trajectories2/ALK2/fifth
done
