#!/bin/bash

# 1st argument - path to the directory with input files
# 2nd argument - lambda
echo Reading in input files from the directory $DIR
cd $1
#prod
echo "    production"
pmemd.cuda -O -i prod/restart.in -p ../complex.prmtop -c prod/complex_prod_$3.rst -x prod/complex_prod_$2.nc -o prod/complex_prod_$2.out -r prod/complex_prod_$2.rst -ref prod/complex_prod_$3.rst

cd ..
