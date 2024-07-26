#!/bin/bash
# 1st argument - lambda

cd $1
#1min
echo "    min1"
cp ../complex.inpcrd 1_min/complex.inpcrd
cp 1_min/complex.inpcrd 1_min/complex_min1_ref.rst
pmemd.cuda -O -i 1_min/1min.in -p ../complex.prmtop -c 1_min/complex.inpcrd -x 1_min/complex_min1.nc -o 1_min/complex_min1.out -r 1_min/complex_min1.rst -ref 1_min/complex_min1_ref.rst

#2min
echo "    min2"
cp 1_min/complex_min1.rst 1_min/complex_min2.inpcrd
cp 1_min/complex_min2.inpcrd 1_min/complex_min2_ref.rst
pmemd.cuda -O -i 1_min/2min.in -p ../complex.prmtop -c 1_min/complex_min2.inpcrd -x 1_min/complex_min2.nc -o 1_min/complex_min2.out -r 1_min/complex_min2.rst -ref 1_min/complex_min2_ref.rst

#nvt
echo "    nvt heating"
cp 1_min/complex_min2.rst 2_nvt/complex_nvt.inpcrd
cp 2_nvt/complex_nvt.inpcrd 2_nvt/complex_nvt_ref.rst
pmemd.cuda -O -i 2_nvt/nvt.in -p ../complex.prmtop -c 2_nvt/complex_nvt.inpcrd -x 2_nvt/complex_nvt.nc -o 2_nvt/complex_nvt.out -r 2_nvt/complex_nvt.rst -ref 2_nvt/complex_nvt_ref.rst

#1npt
echo "    npt1"
cp 2_nvt/complex_nvt.rst 3_npt/complex_1npt.inpcrd
cp 3_npt/complex_1npt.inpcrd 3_npt/complex_1npt_ref.rst
pmemd.cuda -O -i 3_npt/1_npt.in -p ../complex.prmtop -c 3_npt/complex_1npt.inpcrd -x 3_npt/complex_1npt.nc -o 3_npt/complex_1npt.out -r 3_npt/complex_1npt.rst -ref 3_npt/complex_1npt_ref.rst

#2npt
echo "    npt2"
cp 3_npt/complex_1npt.rst 3_npt/complex_2npt.inpcrd
cp 3_npt/complex_2npt.inpcrd 3_npt/complex_2npt_ref.rst
pmemd.cuda -O -i 3_npt/2_npt.in -p ../complex.prmtop -c 3_npt/complex_2npt.inpcrd -x 3_npt/complex_2npt.nc -o 3_npt/complex_2npt.out -r 3_npt/complex_2npt.rst -ref 3_npt/complex_2npt_ref.rst

#3npt
echo "    npt3"
cp 3_npt/complex_2npt.rst 3_npt/complex_3npt.inpcrd
cp 3_npt/complex_3npt.inpcrd 3_npt/complex_3npt_ref.rst
pmemd.cuda -O -i 3_npt/3_npt.in -p ../complex.prmtop -c 3_npt/complex_3npt.inpcrd -x 3_npt/complex_3npt.nc -o 3_npt/complex_3npt.out -r 3_npt/complex_3npt.rst -ref 3_npt/complex_3npt_ref.rst

#prod
echo "    production"
cp 3_npt/complex_3npt.rst prod/complex_prod.inpcrd
cp prod/complex_prod.inpcrd prod/complex_prod_ref.rst
pmemd.cuda -O -i prod/prod.in -p ../complex.prmtop -c prod/complex_prod.inpcrd -x prod/complex_prod_00.nc -o prod/complex_prod_00.out -r prod/complex_prod_00.rst -ref prod/complex_prod_ref.rst

cd ..
