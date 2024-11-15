# otf_rbfe

Implementation of On-The-Fly (OTF) Optimization for alchemical relative binding free energy simulations using thermodynamic integration in AMBER20. See 10.26434/chemrxiv-2023-rtpsz for details.
See test_cases for PLpro and CDK2 example systems and directory architecture.
Assumes pre-aligned and parameterized system as input!

#### ***Directory Architecture***
site: contains AMBER input files for the mutation of ligand 1 (:L0) to  ligand 2 (:L1) in complex. Files are copied on the fly to protein-ligand complex directory and updated to contain user specified parameters.
water: contains AMBER input files for the mutation of ligand 1 (:L0) to  ligand 2  in solution. Files are copied on the fly to protein-ligand complex directory and updated to contain user specified parameters.

##### ***Setup:***
***
1. Copy otf_general/otf_rbfe/*sh to your working directory
2. Run ./rbfe_all_prep.sh on all protein-ligand complex directories.
	a. This will create your file architecture, copy important files and generate the scmask (Boresch restraints).
	b. Use associated options to select proper values of force constants for Boresch restraints. Note that values are in AMBER format and are equivalent to k/2.


##### ***Running MD TI ABFE***
***
Run the script below (show help: ```./run_abfe.sh -h```)

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
| `-S`   | schedule ('equal' OR 'gaussian' OR 'custom') |
| `-n`   | number of windows (int)                      |
| `-C`   | custom windows ([float],[float],[float],...) |
| `-r`   | rtr window ([float],[float],[float],...)     |
| `-m`   | destination directory (string of path name)  |
| `-A`   | Set additional restraints for equilibration  |
| `-F`   | Set number of frames to save per ns (int)    |
| `-o`   | Alpha and Beta parameters for SSSC(2) (1,2)  |

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
| `equil_restr`         | `''`                            |
| `fpn`                 | `0`                             |
| `sssc`                | `2`                             |

##### ***Example:***
```
./run_abfe.sh -i 0.2 -a 0.5 -f 1 -s 2 -S equal -n 5 -m ~/data/lysozyme_testing all lysozyme*
```

#### ***Analysis:***
***
Copy otf_general/otf_abfe/analysis/analysis.sh to your working directory and run on completed ABFE simulations. Output generated in `abfe_summary.dat`.
Analysis performed using the bootstrap method. 

#### ***test_systems***
***
Contains starting structures for T4 Lysozyme and PLpro ABFE.

##### ***lysozyme_abfe***
***
Contains input files to perform parameterization using both GAUSSIAN 09 or GAUSSIAN 16, as well as conventional MD and ABFE on both systems. Each step can be performed in a stand alone manner.

##### ***plpro_abfe***
***
Contains input files to perform ABFE simulations on PLpro only
