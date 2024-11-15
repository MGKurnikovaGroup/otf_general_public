# auto_restraint

## Usage:

```
cd auto_restraint_files
./auto_restraint.sh <options> <directories>
```

### Options:

-p: topology file

-t: trajectory file

-l: ligand residue name

-s: protein residue id start of range

-e: protein residue id end of range

-f: fraction cutoff

-L: ligand file

-P: pdb file

### Default files:

topology_file="complex.prmtop"

trajectory_file="nvt-7ns.nc"

ligand_res_name="MOL"

protein_res_id_start="2"

protein_res_id_end="163"

fraction_cutoff="0.5"

ligand_file="setup/lig_tleap.mol2"

pdb_file="complex-repres.pdb"

### Example:

```
cd auto_restraint_files
./auto_restraint.sh -p complex.prmtop -t nvt-7ns.nc -l MOL -s 2 -e 357 -f 0.5 -L setup/lig_tleap.mol2 -P complex-repres.pdb ../lysozyme_test_case_restraints ../dir2 ../dir3
```
