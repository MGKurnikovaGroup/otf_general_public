#!/bin/bash
#source  /export/home/egutkin/programs/amber20/amber.sh
date > date.10ns.txt

echo minimization: 2 steps, 2000 cycles each
pmemd.cuda -O -i min1.in -p complex.prmtop -c complex.inpcrd -o min_1.out -r min_1.rst -x min_1.nc -ref complex.inpcrd
pmemd.cuda -O -i min2.in -p complex.prmtop -c min_1.rst -o min_2.out -r min_2.rst -x min_2.nc -ref min_1.rst
echo heating: 1 step, 150 ps
pmemd.cuda -O -i heat.in -p complex.prmtop -c min_2.rst -o heat.out -r heat.rst -x heat.nc -ref min_2.rst
echo npt: 5 steps, 0.1 ns each
pmemd.cuda -O -i npt1.in -p complex.prmtop -c heat.rst -o npt1.out -r npt1.rst -x npt1.nc -ref heat.rst
pmemd.cuda -O -i npt2.in -p complex.prmtop -c npt1.rst -o npt2.out -r npt2.rst -x npt2.nc -ref npt1.rst
pmemd.cuda -O -i npt3.in -p complex.prmtop -c npt2.rst -o npt3.out -r npt3.rst -x npt3.nc -ref npt2.rst
pmemd.cuda -O -i npt4.in -p complex.prmtop -c npt3.rst -o npt4.out -r npt4.rst -x npt4.nc -ref npt3.rst
pmemd.cuda -O -i npt5.in -p complex.prmtop -c npt4.rst -o npt5.out -r npt5.rst -x npt5.nc -ref npt4.rst
#pmemd.cuda -O -i npt6.in -p complex.prmtop -c npt5.rst -o npt6.out -r npt6.rst -x npt6.nc -ref npt5.rst
echo nvt: 1 step, 10 ns
pmemd.cuda -O -i nvt-10ns.in -p complex.prmtop -c npt5.rst -o nvt-10ns.out -r nvt-10ns.rst -x nvt-10ns.nc -ref npt5.rst

date >> date.10ns.txt

