#!/bin/bash
mypcl=$(realpath $(find ~/ -type d -name "otf_rbfe"))


for X in "$@"
do
	cp $mypcl/*.py $X
	cp $mypcl/site/*.sh $X/site
	cp $mypcl/water/*.sh $X/water
	cp $mypcl/water/cpp* $X/water
	cd $X
	python3 write_scmask.py
	cd ..
done
