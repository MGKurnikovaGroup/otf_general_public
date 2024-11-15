#!/bin/bash

myframe=$(awk '{print $6}' rmsd-avglig.avg | tail -n 1)
echo $myframe

myframe2=$((myframe + 200))
echo $myframe2

cpptraj -p complex.prmtop <<END
	trajin nvt-7ns.nc 251 last
	autoimage
	trajout complex-repres.pdb
	trajout complex-repres.rst7
END

