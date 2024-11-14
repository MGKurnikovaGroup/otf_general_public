#!/bin/bash
mypcl=$(realpath $(find ~/ -type d -name "otf_abfe"))
show_help() {
    echo "Usage: $0 [options] dir1 dir2 ... dirN"
    echo "Options:"
    echo "  -p, --topology-file FILE     topology file (default: complex.prmtop)"
    echo "  -t, --trajectory-file FILE   trajectory file (default: nvt-7ns.nc)"
    echo "  -l, --ligand-res-name NAME   ligand residue name (default: MOL)"
    echo "  -s, --protein-res-id-start ID   protein residue id start (default: 2)"
    echo "  -e, --protein-res-id-end ID   protein residue id end (default: 163)"
    echo "  -f, --fraction-cutoff FLOAT  fraction cutoff (default: 0.5)"
    echo "  -L, --ligand-file FILE       ligand file (default: setup/lig_tleap.mol2)"
    echo "  -P, --pdb-file FILE          pdb file (default: complex-repres.pdb)"
    echo "  -h, --help                   display this help and exit"
}
#default values
topology_file="complex.prmtop"
trajectory_file="nvt-7ns.nc"
ligand_res_name="MOL"
protein_res_id_start="2"
protein_res_id_end="163"
fraction_cutoff="0.5"
ligand_file="setup/lig_tleap.mol2"
pdb_file="complex-repres.pdb"

#process parameters
while [[ $# -gt 0 ]]; do
    case "$1" in
        -p|--topology-file)
            topology_file="$2"
            shift 2
            ;;
        -t|--trajectory-file)
            trajectory_file="$2"
            shift 2
            ;;
        -l|--ligand-res-name)
            ligand_res_name="$2"
            shift 2
            ;;
        -s|--protein-res-id-start)
            protein_res_id_start="$2"
            shift 2
            ;;
        -e|--protein-res-id-end)
            protein_res_id_end="$2"
            shift 2
            ;;
        -f|--fraction-cutoff)
            fraction_cutoff="$2"
            shift 2
            ;;
        -L|--ligand-file)
            ligand_file="$2"
            shift 2
            ;;
        -P|--pdb-file)
            pdb_file="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        --)
            shift
            break
            ;;
        -*)
            echo "Unknown option: $1" >&2
            show_help
            exit 1
            ;;
        *)
            break
            ;;
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
	cp $mypcl/auto_restraint_files/auto_restraint.sh .
        cp $mypcl/auto_restraint_files/cpptraj.restraint.sh .
        cp $mypcl/auto_restraint_files/restraint_analysis.py .
        cp $mypcl/auto_restraint_files/restraint_analysis_functions.py .
        ./cpptraj.restraint.sh -P "$topology_file" -t "$trajectory_file" -l "$ligand_res_name" -r "$protein_res_id"
        python3 restraint_analysis.py "$fraction_cutoff" md-complex/BB.avg.dat md-complex/BB2.avg.dat "$ligand_file" "$pdb_file"
        echo =====  $X  Done =======================
done

