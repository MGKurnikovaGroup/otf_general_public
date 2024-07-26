#!/bin/bash
for X in "$@"
do
	cp ~/protocols/ALK2_otf/*.py $X
	cp ~/protocols/ALK2_otf/site/*.sh $X/site
	cp ~/protocols/ALK2_otf/water/*.sh $X/water
	cp ~/protocols/ALK2_otf/water/cpp* $X/water
	cd $X
	python3 write_scmask.py
	cd ..
done
