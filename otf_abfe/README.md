# OTF-ABFE

Implementation of On-The-Fly (OTF) Optimization for alchemical absolute binding free energy simulations using thermodynamic integration in AMBER20. See [10.26434/chemrxiv-2023-rtpsz](https://doi.org/10.26434/chemrxiv-2023-rtpsz) for details.

See `test_cases` for PLpro and lysozyme example systems and directory architecture.

## Table of Contents
- [Parameterization](#parameterization)
- [Conventional MD](#conventional-md)
- [Automated Restraint Analysis](#automated-restraint-analysis)
- [ABFE Simulation](#abfe)
- [Test Systems](#test-systems)

## Parameterization

Parameterization of Protein-Ligand Complex and Solvated Ligand for absolute binding free energy simulations.

### Usage

1. Create working directory outside of `otf_general_public`
2. Copy `otf_general_public/otf_abfe/parameterization` directory to working directory. Copy `parameterization/*.sh` to working directory
3. Copy a PDB of your protein with hydrogens added and without the ligand as `input-for-prep/protein_H.pdb`. 
   > **Note**: This PDB can be solvated with ions added or not. If not, make the required changes to `tleap.complex.in` to solvate and neutralize your system.
4. Run `./all-prep-lig-g16.sh` or `./all-prep-lig-g09.sh` as required by your Gaussian installation with your ligand files as input. Update the parameters within these shell scripts as needed to match your machine, ligand charge, etc.
   ```bash
   ./all-prep-lig-g16.sh <directories>
   ```
5. **Note**: If no waters are within 1.0 angstroms of your molecule, `complex.prmtop` and `complex.inpcrd` will fail to generate. One should simply copy the `complex0.prmtop` and `complex0.inpcrd` from the ligand setup directory to the ligand md-complex directory as `complex.prmtop` and `complex.inpcrd`

### Required Output

1. `complex.[pdb, inpcrd, prmtop]`
2. `ligwat.[pdb, inpcrd, prmtop]`
3. `lig_tleap.mol2`

## Conventional MD

Protocol for performing short conventional MD simulations of the protein-ligand complex to extract representative structures and heavy atoms for Boresch restraints. Performs 7ns of MD, see preprint for details.

### Usage

1. Copy `otf_general_public/otf_abfe/conventional_MD/*sh` to working directory. Working directory should be outside of `otf_abfe`
2. Run `./all-copy-pcl.sh` on all protein-ligand complex directories obtained from Parameterization Step
3. Run `./all-run-7ns.sh` on all protein-ligand complex directories
4. Run `./all-rmsd-avg.sh` on all protein-ligand complex directories with completed MD simulations
   > **Note**: You must update the respective cpptraj input script if you change the length/ligand name/simulation details
5. Run `./all-get-repres.sh` on all protein-ligand complex directories with completed RMSD analysis to extract representative structures for ABFE

```bash
./all-copy-pcl.sh <directories>
./all-run-7ns.sh <directories>
./all-rmsd-avg.sh <directories>
./all-get-repres.sh <directories>
```

### Required Output

1. `complex-repres.[pdb, rst7, prmtop]` or equivalent files

## Automated Restraint Analysis

Implementation of algorithm for the automated selection of protein and ligand atoms for Boresch restraints from Chen et al.: [10.1021/acs.jcim.3c00013](https://doi.org/10.1021/acs.jcim.3c00013). Assumes completed conventional MD with extracted representative structures.

### Usage

1. Copy `otf_general_public/otf_abfe/auto_restraint_files/auto_restraint.sh` to your working directory
   > **Note**: Working directory should be outside of `otf_general_public`
2. Run `./auto_restraint.sh` on all protein-ligand complex directories
3. **Note**: The input directories should contain all the data files (see Options below)

```bash
./auto_restraint.sh <options> <directories>
```

Show Help: `./auto_restraint.sh -h`

### Options

| Option | Description                                |
|--------|--------------------------------------------|
| `-p`   | Topology file (string of path name)        |
| `-t`   | Trajectory file (string of path name)      |
| `-l`   | Ligand residue name (string)               |
| `-s`   | Protein residue id, start of range (int)   |
| `-e`   | Protein residue id, end of range (int)     |
| `-f`   | Fraction cutoff (float)                    |
| `-L`   | Ligand file (string of path name)          |
| `-P`   | PDB file (string of path name)             |

### Default Values

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

### Example

```bash
cd auto_restraint_files
./auto_restraint.sh -p complex.prmtop -t nvt-7ns.nc -l MOL -s 2 -e 163 -f 0.5 -L setup/lig_tleap.mol2 -P complex-repres.pdb lysozyme*
```

### Required Outputs

1. `vbla.txt`: List of ligand heavy atoms for Boresch restraints
2. `vbla2.txt`: List of protein backbone atoms for Boresch restraints

## ABFE

Implementation of OTF Optimization for absolute binding free energy simulations. Assumes generation of `vbla.txt` and `vbla2.txt` for Boresch restraints.

### Directory Architecture

- **dcrg+vdw**: Contains AMBER input files for decoupling of ligand in complex. Files are copied on the fly to protein-ligand complex directory and updated to contain user specified parameters.
- **rtr**: Contains AMBER input files for the addition of the Boresch restraints. Files are copied on the fly to protein-ligand complex directory and updated to contain user specified parameters.
- **water-dcrg+vdw**: Contains AMBER input files for the decoupling of the ligand in solution. Files are copied on the fly to protein-ligand complex directory and updated to contain user specified parameters.

### Setup

1. Copy `otf_general_public/otf_abfe/*sh` to your working directory
2. Run `./abfe_all_prep.sh` on all protein-ligand complex directories
   - This will create your file architecture, copy important files and generate `k.RST` file (Boresch restraints)
   - Use associated options to select proper values of force constants for Boresch restraints. Note that values are in AMBER format and are equivalent to k/2

### Running MD TI ABFE

Run the script below:

```bash
./run_abfe.sh <options> <execution type ('dcrg','water','rtr','all')> <data directories>
```

Show Help: `./run_abfe.sh -h`

### Options

| Option | Description                                  |
|--------|----------------------------------------------|
| `-c`   | Convergence cutoff (float)                   |
| `-i`   | Initial time (float)                         |
| `-a`   | Additional time (float)                      |
| `-f`   | First max value (float)                      |
| `-s`   | Second max value (float)                     |
| `-S`   | Schedule ('equal' OR 'gaussian' OR 'custom') |
| `-n`   | Number of windows (int)                      |
| `-C`   | Custom windows ([float],[float],[float],...) |
| `-r`   | RTR window ([float],[float],[float],...)     |
| `-m`   | Destination directory (string of path name)  |
| `-A`   | Set additional restraints for equilibration  |
| `-F`   | Set number of frames to save per ns (int)    |
| `-o`   | Alpha and Beta parameters for SSSC(2) (1,2)  |

### Default Values

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

### Example

```bash
./run_abfe.sh -i 0.2 -a 0.5 -f 1 -s 2 -S equal -n 5 -m ~/data/lysozyme_testing all lysozyme*
```

### Analysis

Copy `otf_general_public/otf_abfe/analysis/analysis.sh` to your working directory and run on completed ABFE simulations. Output generated in `abfe_summary.dat`.
Analysis performed using the bootstrap method.

## Test Systems

Contains starting structures for T4 Lysozyme and PLpro ABFE.

### Lysozyme ABFE

Contains input files to perform parameterization using both GAUSSIAN 09 or GAUSSIAN 16, as well as conventional MD and ABFE on both systems. Each step can be performed in a stand alone manner.

### PLpro ABFE

Contains input files to perform ABFE simulations on PLpro only.
