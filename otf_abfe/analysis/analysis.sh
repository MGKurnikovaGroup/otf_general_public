#!/bin/bash
mypcl=$(realpath $(find ~/ -type d -name "otf_abfe"))
mywd=$(pwd)
for X in "$@"
do	
	cp $mypcl/analysis.py $X
	cd $X
        python3 analysis.py
	cd ..
done
cp $mypcl/compile_analysis.py .
python3 compile_analysis.py "$@"
ls
