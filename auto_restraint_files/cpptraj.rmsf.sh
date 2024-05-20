#!/bin/bash

myframe=$(awk '{print $6}' rmsd-avglig.avg | tail -n 1)
echo $myframe

myframe2=$((myframe + 200))
echo $myframe2

cp complex-repres.* md-complex
cd md-complex
cpptraj -p complex.prmtop <<END
        trajin nvt-7ns.nc $myframe $myframe2
        reference complex-repres.rst7
	rms :MOL ref complex-repres.rst7
	atomicfluct out rmsf :MOL 
	run

