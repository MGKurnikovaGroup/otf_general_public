#!/bin/bash

# 1st argument - path to the directory with input files
# 2nd argument - lambda
DIR=$1/dcrg+vdw/$2
echo Reading in input files from the directory $DIR


#1npt
echo "    npt1"
cd $1
cp 2_nvt/complex_nvt.rst 3_npt/complex_1npt.inpcrd
cp 3_npt/complex_1npt.inpcrd 3_npt/complex_1npt_ref.rst
pmemd.cuda -O -i 3_npt/1_npt.in -p ../complex.prmtop -c 3_npt/complex_1npt.inpcrd -x 3_npt/complex_1npt.nc -o 3_npt/complex_1npt.out -r 3_npt/complex_1npt.rst -ref 3_npt/complex_1npt_ref.rst
cd ..

