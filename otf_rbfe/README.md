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
	a. This will create your file architecture, copy important files and generate the scmask from the ligwat.pdb file.
	b. Required directory architecture: The protein-ligand complex directory contains two directories: site, which contains complex.prmtop and complex.inpcrd, and water, which contains ligwat.prmtop, ligwat.inpcrd, and ligwat.pdb.


##### ***Running MD TI RBFE***
***
Run the script below (show help: ```./run_rbfe.sh -h```)

```
./run_rbfe.sh <options> <execution type ('site','water','all')> <data directories>
```

Note: Special treatment protocol uses the the output of the first minimization step from the reference lambda as the starting input for the target lambda. This was found to overcome numerical instability in our previous work. See Gusev et al. DOI: 10.1021/acs.jcim.2c01052 for details.

Options:

| Option | Description                                                  |
|--------|--------------------------------------------------------------|
| `-c`   | convergence cutoff (float)                                   |
| `-i`   | initial time (float)                                         |
| `-a`   | additional time (float)                                      |
| `-f`   | first max value (float)                                      |
| `-s`   | second max value (float)                                     |
| `-S`   | schedule ('equal' OR 'gaussian' OR 'custom')                 |
| `-n`   | number of windows (int)                                      |
| `-C`   | custom windows ([float],[float],[float],...)                 |
| `-r`   | rtr window ([float],[float],[float],...)                     |
| `-m`   | destination directory (string of path name)                  |
| `-A`   | Set additional restraints for equilibration (str)            |
| `-F`   | Set number of frames to save per ns (int)                    |
| `-o`   | Alpha and Beta parameters for SSSC(2), or no SSSC (0,1,2)    |
| `-sp`  | Indicates which step to use special treatment (site or water)|
| `-R`   | Reference lam for special treatment protocol (float)         |
| `-T`   | Target lam for special treatment protocol    (float)         |
| `-ctm1`| Custom Amber Mask for Site timask1 (str)                     |
| `-ctm2`| Custom Amber Mask for Site timask2 (str)                     |
|`-ctmw1`| Custom Amber Mask for Water timask1 (str)                    |
|`-ctmw2`| Custom Amber Mask for Water timask2 (str)                    |

Default values (if no input specified):

| Option                | Default Value                   |
|-----------------------|---------------------------------|
| `-c`                  | `0.1`                           |
| `-i`                  | `2.5`                           |
| `-a`                  | `0.5`                           |
| `-f`                  | `6.5`                           |
| `-s`                  | `10.5`                          |
| `-S`                  | `'equal'`                       |
| `-n`                  | `9`                             |
| `-m`                  | `.`                             |
| `-A`                  | `''`                            |
| `-F`                  | `0`                             |
| `-o`                  | `2`                             |
|  `-sp`                | `'site'`                        |
| `-R`                  | `-1`                            |
| `-T`                  | `-1`                            |
| `-ctm1`               | `''`                            |
| `-ctm2`               | `''`                            |
|`-ctmw1`               | `''`                            |
|`-ctmw2`               | `''`                            |

##### ***Example:***
```
./run_rbfe.sh -i 0.2 -a 0.5 -f 1 -s 2 -S equal -n 5 -m ~/data/cdk2_testing all *~*
```

#### ***Analysis:***
***
Copy otf_general/otf_rbfe/analysis/analysis_gt.sh to your working directory and run on completed RBFE simulations with option for gaussian quadrature or trapezoid integration. Output generated in `rbfe_summary.dat`.
Analysis performed using the bootstrap method. 

#### ***test_systems***
***
Contains starting structures for CDK2 and PLpro RBFE.

##### ***CDK2***
***
Contains input files to perform RBFE simulations. Do not run the write_scmask.py script on these files as the naming convention is different from what we typically use.
In order to replicate this work, `-o 0` should be employed. `-ctm1 :556`, `-ctm2 :557`, `-ctmw1 :1`, and `-ctmw2 :2` can be employed to simplify the thuse of `./run_rbfe.sh`

##### ***plpro_rbfe***
***
Contains input files to perform RBFE simulations on PLpro only
