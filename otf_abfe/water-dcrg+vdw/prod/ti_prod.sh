#!/bin/sh
pmemd.cuda -O -i run_0.3.in -p ../../ac-101.prmtop -c ../ac-101_3npt.rst -o ac-101-0.3.out -r ac-101_0.3.rst -x ac-101_0.3.mdcrd -ref ../ac-101_3npt.rst -inf ac-101_0.3.mdinfo -e ac-101_0.3.mded
