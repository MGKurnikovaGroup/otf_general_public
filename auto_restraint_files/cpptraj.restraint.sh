#!/bin/bash

myframe=$(awk '{print $6}' rmsd-avglig.avg | tail -n 1)
echo $myframe

myframe2=$((myframe + 200))
echo $myframe2

cd md-complex
cpptraj -p complex.prmtop <<END
        trajin nvt-7ns.nc $myframe $myframe2
	hbond Backbone2 acceptormask :MOL donormask :2-357 avgout BB2.avg.dat series uuseries bbhbond.gnu
	hbond Backbone donormask :MOL acceptormask :2-357 avgout BB.avg.dat series uuseries bbhbond.gnu
	run
