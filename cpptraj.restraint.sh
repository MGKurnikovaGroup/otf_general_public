#!/bin/bash
cd md-complex

cpptraj -p complex.prmtop <<END
        trajin nvt-7ns.nc 201
	hbond Backbone2 acceptormask :MOL donormask :2-357 avgout BB2.avg.dat series uuseries bbhbond.gnu
	hbond Backbone donormask :MOL acceptormask :2-357 avgout BB.avg.dat series uuseries bbhbond.gnu
	run
	quit
cd ..
