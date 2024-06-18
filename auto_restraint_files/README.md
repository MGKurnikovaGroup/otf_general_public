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

-r: protein residue id

-f: fraction cutoff

-L: ligand file

-P: pdb file

### Default files:

topology_file="complex.prmtop"

trajectory_file="nvt-7ns.nc"

ligand_res_name="MOL"

protein_res_id_start="2"

protein_res_id_end="357"

fraction_cutoff="0.5"

ligand_file="setup/lig_tleap.mol2"

pdb_file="complex-repres.pdb"

### Example:

```
cd auto_restraint_files
./auto_restraint.sh -L setup/lig_tleap.mol2 -P complex-repres.pdb -f 0.5 ../lysozyme_test_case_restraints ../dir2
```