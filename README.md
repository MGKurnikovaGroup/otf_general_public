# otf_general

Implementation of On-The-Fly (OTF) Optimization for alchemical binding free energy simulations using thermodynamic integration in AMBER20. See 10.26434/chemrxiv-2023-rtpsz for details.

## Setup

1. Create a directory, clone otf_general.
2. Install [Anaconda](https://docs.anaconda.com/anaconda/install/)
3. Install dependencies: pymbar==4.0.3, alchemlyb==2.3.1, scipy==1.8.1, AMBER20, GAUSSIAN 09 or GAUSSIAN 16 (for ligand parameterization):


### **Absolute binding free energy**

#### **Parameterization**
***
Parameterization of Protein-Ligand Complex and Solvated Ligand for absolute binding free energy simulations.

Usage:

1. Create working directory outside of otf_general.
2. Copy otf_general/otf_abfe/parameterization directory to working directory. Copy parameterization/*.sh to working directory.
3. Copy a pdb of your protein with hydrogens added and without the ligand as input-for-prep/protein_H.pdb. Note: This pdb can be solvated with ions added or not. If not, make the required changes to tleap.complex.in to solvated and neutralize your system.
4. Run ./all-prep-lig-g16.sh or ./all-prep-lig-g09.sh as required by your Gaussian installation with your ligand files as input. Update the parameters within these shell scripts as needed to match your machine, ligand charge, etc.
5. Note: If no waters are within 1.0 angstroms of your molecule, complex.prmtop and complex.inpcrd will fail to generate. One should simply copy the complex0.prmtop and complex0.inpcrd from the ligand setup directory to the ligand md-complex directory as complex.prmtop and complex.inpcrd

#### **Conventional MD**
***
Protocol for performing short conventional MD simulations of the protein-ligand complex to extract representative structures and heavy atoms for Boresch restraints. Performs 7ns of MD, see preprint for details.

Usage:

1. Copy otf_general/otf_abfe/conventional_MD/*sh to working directory. Working directory should be outside of otf_abfe.
2. Run ./all-copy-pcl.sh on all protein-ligand complex directories obtained from Parameterization Step.
3. Run ./all-run-7ns.sh on all protein-ligand complex directories.
***

#### Automated restraint analysis
Implementation of algorithm for the automated selection of protein and ligand atoms for Boresch restraints from Chen et al.: 10.1021/acs.jcim.3c00013

Show Help: ```./auto_restraint.sh -h```
##### Usage:

1. Copy otf_general/otf_abfe/auto_restraint_files/auto_restraint.sh to your working directory. Note: Working directory should be outside of otf_general.
2. Run the following
3. Note: the inputed directories should contain all the data files (see Options below). They should also be located just one level under otf_general, like otf_abfe.

```
./auto_restraint.sh <options> <directories>
```
##### Options:

| Option | Description                                |
|--------|--------------------------------------------|
| `-p`   | topology file (string of path name)        |
| `-t`   | trajectory file (string of path name)      |
| `-l`   | ligand residue name (string)               |
| `-s`   | protein residue id, start of range (int)   |
| `-e`   | protein residue id, end of range (int)     |
| `-f`   | fraction cutoff (float)                    |
| `-L`   | ligand file (string of path name)          |
| `-P`   | pdb file (string of path name)             |

Default values (if no input specified):


| Option                 | Default Value              |
|------------------------|----------------------------|
| `topology_file`        | `complex.prmtop`           |
| `trajectory_file`      | `nvt-7ns.nc`               |
| `ligand_res_name`      | `MOL`                      |
| `protein_res_id_start` | `2`                        |
| `protein_res_id_end`   | `163`                      |
| `fraction_cutoff`      | `0.5`                      |
| `ligand_file`          | `setup/lig_tleap.mol2`     |
| `pdb_file`             | `complex-repres.pdb`       |

Example:
```
cd auto_restraint_files
./auto_restraint.sh -p complex.prmtop -t nvt-7ns.nc -l MOL -s 2 -e 357 -f 0.5 -L setup/lig_tleap.mol2 -P complex-repres.pdb ../lysozyme_test_case_restraints ../dir2 ../dir3

Implementation of OTF Optimization for absolute binding free energy simulations. Protocol begins with parameterization of ligand and protein-ligand complex.

Usage:

1. Create a directory outside of otf_general, inside the parent directory
2. Copy the ./run_abfe.sh file in: cp ../otf_general/otf_abfe/run_abfe.sh .
3. Copy in desired abfe data directories
4. Create another directory as the destination for the simulation to write to (-m option)
5. Run the script below (show help: ```./run_abfe.sh -h```)

```
./run_abfe.sh <options> <execution type ('dcrg','water','rtr','all')> <data directories>
```

Options:

| Option | Description                                  |
|--------|----------------------------------------------|
| `-c`   | convergence cutoff (float)                   |
| `-i`   | initial time (float)                         |
| `-a`   | additional time (float)                      |
| `-f`   | first max value (float)                      |
| `-s`   | second max value (float)                     |
| `-S`   | schedule ('equal' OR 'gaussian' OR 'custom')  |
| `-n`   | number of windows (int)                      |
| `-C`   | custom windows ([float],[float],[float],...)  |
| `-r`   | rtr window ([float],[float],[float],...)      |
| `-m`   | destination directory (string of path name)   |

Default values (if no input specified):

| Option                | Default Value                   |
|-----------------------|---------------------------------|
| `convergence_cutoff`  | `0.1`                           |
| `initial_time`        | `2.5`                           |
| `additional_time`     | `0.5`                           |
| `first_max`           | `6.5`                           |
| `second_max`          | `10.5`                          |
| `schedule`            | `'equal'`                       |
| `num_windows`         | `10`                            |
| `rtr_window`          | `'0.0,0.05,0.1,0.2,0.5,1.0'`    |
| `move_to`             | `.`                             |

Example:
```
cd otf_abfe/
./run_abfe.sh -i 0.2 -a 0.5 -f 1 -s 2 -S equal -n 5 -m ~/data/lysozyme_testing all lys_0 lys_1
```


#### Automated restraint analysis
[Description]

Show Help: ```./auto_restraint.sh -h```
##### Usage:

1. Navigate to otf_abfe/auto_restraint_files
2. Run the following
3. Note: the inputted directories should contain all the data files (see Options below). They should also be located just one level under otf_general, like otf_abfe.

```
./auto_restraint.sh <options> <directories>
```
##### Options:

| Option | Description                                |
|--------|--------------------------------------------|
| `-p`   | topology file (string of path name)        |
| `-t`   | trajectory file (string of path name)      |
| `-l`   | ligand residue name (string)               |
| `-s`   | protein residue id, start of range (int)   |
| `-e`   | protein residue id, end of range (int)     |
| `-f`   | fraction cutoff (float)                    |
| `-L`   | ligand file (string of path name)          |
| `-P`   | pdb file (string of path name)             |

Default values (if no input specified):


| Option                 | Default Value              |
|------------------------|----------------------------|
| `topology_file`        | `complex.prmtop`           |
| `trajectory_file`      | `nvt-7ns.nc`               |
| `ligand_res_name`      | `MOL`                      |
| `protein_res_id_start` | `2`                        |
| `protein_res_id_end`   | `357`                      |
| `fraction_cutoff`      | `0.5`                      |
| `ligand_file`          | `setup/lig_tleap.mol2`     |
| `pdb_file`             | `complex-repres.pdb`       |

Example:
```
cd auto_restraint_files
./auto_restraint.sh -p complex.prmtop -t nvt-7ns.nc -l MOL -s 2 -e 357 -f 0.5 -L setup/lig_tleap.mol2 -P complex-repres.pdb ../lysozyme_test_case_restraints ../dir2 ../dir3
```


***


### **Relative binding free energy**
***
[Description]

## 
