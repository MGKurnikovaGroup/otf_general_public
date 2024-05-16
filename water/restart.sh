#!/bin/bash

# 1st argument - path to the directory with input files
# 2nd argument - lambda
echo Reading in input files from the directory $DIR
cd $1
cpptraj -i ../cpp.autoimage.in -y prod/ligwat_prod_$3.rst -p ../ligwat.prmtop
mv autoimage.rst prod/ligwat_prod_$3.rst
#prod
echo "    production"
pmemd.cuda -O -i prod/restart.in -p ../ligwat.prmtop -c prod/ligwat_prod_$3.rst -x prod/ligwat_prod_$2.nc -o prod/ligwat_prod_$2.out -r prod/ligwat_prod_$2.rst -ref prod/ligwat_prod_$3.rst

cd ..
