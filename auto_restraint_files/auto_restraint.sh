#!/bin/bash

# -p: topology file
# -t: trajectory file
# -l: ligand residue name
# -s: protein residue id start
# -e: protein residue id end
# -f: fraction cutoff
# -L: ligand file
# -P: pdb file

#above flag parameters come first, then the directory parameter (../lysozyme_test_case_restraints)

#default values
topology_file="complex.prmtop"
trajectory_file="nvt-7ns.nc"
ligand_res_name="MOL"
protein_res_id_start="2"
protein_res_id_end="357"
fraction_cutoff="0.5"
ligand_file="setup/lig_tleap.mol2"
pdb_file="complex-repres.pdb"

#process parameters
while getopts "p:t:l:s:e:f:L:P:" opt; do
  case $opt in
    p) 
        topology_file="$OPTARG";;
    t) 
        trajectory_file="$OPTARG";;
    l) 
        ligand_res_name="$OPTARG";;
    s)
        protein_res_id_start="$OPTARG";;
    e) 
        protein_res_id_end="$OPTARG";;
    f)
        fraction_cutoff="$OPTARG";;
    L)
        ligand_file="$OPTARG";;
    P)
        pdb_file="$OPTARG";;
  esac
done

protein_res_id="$protein_res_id_start-$protein_res_id_end"

#confirm to user the parameters
echo "topology_file = $topology_file"
echo "trajectory_file = $trajectory_file"
echo "ligand_res_name = $ligand_res_name"
echo "protein_res_id = $protein_res_id"
echo "fraction_cutoff = $fraction_cutoff"
echo "ligand_file = $ligand_file"
echo "pdb_file = $pdb_file"

# Shift options so that $1 will refer to the first non-option argument
shift "$((OPTIND -1))"

for X in "$@"
do
        echo =====  $X  =======================
        
        cd $X
	    cp ../auto_restraint_files/* .
        ./cpptraj.restraint.sh -P "$topology_file" -t "$trajectory_file" -l "$ligand_res_name" -r "$protein_res_id"
        python3 restraint_analysis.py "$fraction_cutoff" md-complex/BB.avg.dat md-complex/BB2.avg.dat "$ligand_file" "$pdb_file"
done

