#!/bin/bash

echo Reading in input files from the directory $DIR

#prod
echo "    production"
cd $1
cp ../complex_prod.inpcrd prod/complex_prod.inpcrd
cp prod/complex_prod.inpcrd prod/complex_prod_ref.rst
pmemd.cuda -O -i prod/prod.in -p ../complex.prmtop -c prod/complex_prod.inpcrd -x prod/complex_prod.nc -o prod/complex_prod_00.out -r prod/complex_prod_00.rst -ref prod/complex_prod_ref.rst

cd ..
