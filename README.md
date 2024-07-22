# otf_general

[Description] ... using AMBER20. 

## Setup

1. Create a directory, clone otf_general into that directory. A parent directory will be needed for the simulations.
2. Install [Anaconda](https://docs.anaconda.com/anaconda/install/)
3. Install pymbar and alchemlyb:
```
pip install pymbar
pip install alchemlyb
```


## Simulations
***
### **Absolute binding free energy**
***
[Description]

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
```
cd otf_abfe/auto_restraint_files
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