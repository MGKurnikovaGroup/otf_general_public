#!/bin/sh
pmemd.cuda -O -i run*in -p ../../ac-101.prmtop -c ../../ac-101-eq.rst7 -o ac-101-0.0.out -r ac-101_0.0.rst -x ac-101_0.0.mdcrd -ref ../../ac-101.inpcrd -inf ac-101_0.0.mdinfo -e ac-101_0.0.mded
