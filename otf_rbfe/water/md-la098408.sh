#!/bin/bash

#1min
echo "    min1"
cp ../la-0.91802/1_min/ligwat_min2.rst 1_min/ligwat.inpcrd
cp 1_min/ligwat.inpcrd 1_min/ligwat_min1_ref.rst
pmemd.cuda -O -i 1_min/1min.in -p ../ligwat.prmtop -c 1_min/ligwat.inpcrd -x 1_min/ligwat_min1.nc -o 1_min/ligwat_min1.out -r 1_min/ligwat_min1.rst -ref 1_min/ligwat_min1_ref.rst

#2min
echo "    min2"
cp 1_min/ligwat_min1.rst 1_min/ligwat_min2.inpcrd
cp 1_min/ligwat_min2.inpcrd 1_min/ligwat_min2_ref.rst
pmemd.cuda -O -i 1_min/2min.in -p ../ligwat.prmtop -c 1_min/ligwat_min2.inpcrd -x 1_min/ligwat_min2.nc -o 1_min/ligwat_min2.out -r 1_min/ligwat_min2.rst -ref 1_min/ligwat_min2_ref.rst

#nvt
echo "    nvt heating"
cp 1_min/ligwat_min2.rst 2_nvt/ligwat_nvt.inpcrd
cp 2_nvt/ligwat_nvt.inpcrd 2_nvt/ligwat_nvt_ref.rst
pmemd.cuda -O -i 2_nvt/nvt.in -p ../ligwat.prmtop -c 2_nvt/ligwat_nvt.inpcrd -x 2_nvt/ligwat_nvt.nc -o 2_nvt/ligwat_nvt.out -r 2_nvt/ligwat_nvt.rst -ref 2_nvt/ligwat_nvt_ref.rst

#1npt
echo "    npt1"
cp 2_nvt/ligwat_nvt.rst 3_npt/ligwat_1npt.inpcrd
cp 3_npt/ligwat_1npt.inpcrd 3_npt/ligwat_1npt_ref.rst
pmemd.cuda -O -i 3_npt/1_npt.in -p ../ligwat.prmtop -c 3_npt/ligwat_1npt.inpcrd -x 3_npt/ligwat_1npt.nc -o 3_npt/ligwat_1npt.out -r 3_npt/ligwat_1npt.rst -ref 3_npt/ligwat_1npt_ref.rst

#2npt
echo "    npt2"
cp 3_npt/ligwat_1npt.rst 3_npt/ligwat_2npt.inpcrd
#. align.sh ../ligwat.prmtop 3_npt/ligwat_1npt.rst ../ligwat.inpcrd 3_npt/ligwat_2npt_ref_align
cp 3_npt/ligwat_2npt.inpcrd 3_npt/ligwat_2npt_ref.rst
pmemd.cuda -O -i 3_npt/2_npt.in -p ../ligwat.prmtop -c 3_npt/ligwat_2npt.inpcrd -x 3_npt/ligwat_2npt.nc -o 3_npt/ligwat_2npt.out -r 3_npt/ligwat_2npt.rst -ref 3_npt/ligwat_2npt_ref.rst

#3npt
echo "    npt3"
cp 3_npt/ligwat_2npt.rst 3_npt/ligwat_3npt.inpcrd
cp 3_npt/ligwat_3npt.inpcrd 3_npt/ligwat_3npt_ref.rst
#. align.sh ../ligwat.prmtop 3_npt/ligwat_2npt.rst ../ligwat.inpcrd 3_npt/ligwat_3npt_ref_align
pmemd.cuda -O -i 3_npt/3_npt.in -p ../ligwat.prmtop -c 3_npt/ligwat_3npt.inpcrd -x 3_npt/ligwat_3npt.nc -o 3_npt/ligwat_3npt.out -r 3_npt/ligwat_3npt.rst -ref 3_npt/ligwat_3npt_ref.rst

echo "   2fs production"
cp 3_npt/ligwat_3npt.rst prod-2fs/ligwat_prod-2fs.inpcrd
cp prod-2fs/ligwat_prod-2fs.inpcrd prod-2fs/ligwat_prod-2fs_ref.rst
#. align.sh ../ligwat.prmtop 3_npt/ligwat_3npt.rst ../ligwat.inpcrd prod-2fs/ligwat_prod-2fs_ref_align
pmemd.cuda -O -i prod-2fs/prod.in -p ../ligwat.prmtop -c prod-2fs/ligwat_prod-2fs.inpcrd -x prod-2fs/ligwat_prod.nc -o prod-2fs/ligwat_prod.out -r prod-2fs/ligwat_prod-2fs.rst -ref prod-2fs/ligwat_prod-2fs_ref.rst

