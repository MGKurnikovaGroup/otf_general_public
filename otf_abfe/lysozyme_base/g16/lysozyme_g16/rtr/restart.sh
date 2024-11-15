#!/bin/bash

echo Reading in input files from the directory $DIR

#prod
echo "    production"
cd $1
pmemd.cuda -O -i prod/restart.in -p ../complex.prmtop -c prod/complex_prod_$3.rst -x prod/complex_prod_$2.nc -o prod/complex_prod_$2.out -r prod/complex_prod_$2.rst -ref prod/complex_prod_$3.rst

cd ..
