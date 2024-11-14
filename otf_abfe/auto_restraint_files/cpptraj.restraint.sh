#!/bin/bash
cd md-complex

while getopts "P:t:l:r:" opt; do
  case $opt in
    P) 
        topology_file="$OPTARG";;
    t) 
        trajectory_file="$OPTARG";;
    l) 
        ligand_res_name="$OPTARG";;
    r)
        protein_res_id="$OPTARG";;
  esac
done

cpptraj -p "$topology_file" <<END
        trajin "$trajectory_file" 201
	hbond Backbone2 acceptormask ":$ligand_res_name" donormask ":$protein_res_id" avgout BB2.avg.dat series uuseries bbhbond.gnu
	hbond Backbone donormask ":$ligand_res_name" acceptormask ":$protein_res_id" avgout BB.avg.dat series uuseries bbhbond.gnu
	run
	quit
cd ..
