#!/bin/sh
pmemd.cuda -O -i run_0.6.in -p ../../ac-101.prmtop -c ../ac-101_3npt.rst -o ac-101-0.6.out -r ac-101_0.6.rst -x ac-101_0.6.mdcrd -ref ../ac-101_3npt.rst -inf ac-101_0.6.mdinfo -e ac-101_0.6.mded
