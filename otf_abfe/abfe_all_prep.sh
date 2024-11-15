#!/bin/bash

##Prepares all protein-ligand complex directories for ABFE by creating valid input files, generating proper file archetecture, and generating k.RST file for Boresch restraints.
##Note: force constants are in AMBER FORMAT meaning they are equivalent to k/2 in the standard spring force equation


mywd=$(pwd)
mypcl=$(realpath $(find ~/ -type d -name "otf_abfe"))

show_help() {
    echo "Usage: $0 [options] dir1 dir2 ... dirN"
    echo "Options:"
    echo "  -d, --distance FLOAT     distance (default: 2.0)"
    echo "  -a, --angle FLOAT   angle (default: 10.0)"
    echo "  -D, --dihedral FLOAT   dihedral (default: 20.0)"
}

distance=2.0
angle=10.0
dihedral=20.0

#options for writing values of angle, distance, and dihedral to samplep.cpp.get-vb.in file
while [[ $# -gt 0 ]]; do
    case "$1" in
        -d|--distance)
            distance="$2"
            shift 2
            ;;
        -a|--angle)
            angle="$2"
            shift 2
            ;;
		-D|--dihedral)
			dihedral="$2"
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

for X in "$@"
do
    echo =====  $X  =======================
    cd $X/

    mkdir dcrg+vdw
    mkdir water-dcrg+vdw
    mkdir rtr

    # copy input coordinates
    cp complex-repres.rst7 ./complex.inpcrd
    cp complex-repres.rst7 ./dcrg+vdw/complex.inpcrd
    cp complex-repres.rst7 ./rtr/complex_prod.inpcrd

    # copy topologies
    cp md-complex/complex.prmtop ./
    cp md-complex/complex.prmtop ./dcrg+vdw/
    cp md-complex/complex.prmtop ./rtr/

    # copy all executable files
    cp $mypcl/template.cpp.get-vb.in ./
    cp $mypcl/dcrg+vdw/*sh dcrg+vdw/
    cp $mypcl/rtr/*sh rtr/
    cp $mypcl/rtr/*py rtr/

    # use names of selected ligand atoms to generate cpp.get-vb.in
    myla1=$(awk '{print $1}' vbla.txt)
    myla2=$(awk '{print $2}' vbla.txt)
    myla3=$(awk '{print $3}' vbla.txt)

    mypa1=$(awk '{print $1}' vbla2.txt)
    mypa2=$(awk '{print $2}' vbla2.txt)
    mypa3=$(awk '{print $3}' vbla2.txt)

    echo
    echo "vbla.txt:"
    cat vbla.txt; 
    echo

    #edit template.cpp.get-vb.in to user inputted angle, distance, dihedral values
    cat <<EOF > template.cpp.get-vb.in
    parm complex.prmtop
    reference complex.inpcrd

    rst :MOL@LATOM1 :PROTATOM1 reference width 10.0 rk2 $distance rk3 $distance out k.RST
    rst :MOL@LATOM1 :PROTATOM1 :PROTATOM2 reference width 90.0 rk2 $angle rk3 $angle out k.RST
    rst :MOL@LATOM1 :PROTATOM1 :PROTATOM2 :PROTATOM3 reference width 90.0 rk2 $dihedral rk3 $dihedral out k.RST
    rst :MOL@LATOM2 :MOL@LATOM1 :PROTATOM1 reference width 90.0 rk2 $angle rk3 $angle out k.RST
    rst :MOL@LATOM2 :MOL@LATOM1 :PROTATOM1 :PROTATOM2 reference width 90.0 rk2 $dihedral rk3 $dihedral out k.RST
    rst :MOL@LATOM3 :MOL@LATOM2 :MOL@LATOM1 :PROTATOM1 reference width 90.0 rk2 $dihedral rk3 $dihedral out k.RST

    run

EOF

    sed "s/LATOM1/$myla1/" template.cpp.get-vb.in > cpp.get-vb.in
    sed -i "s/LATOM2/$myla2/" cpp.get-vb.in
    sed -i "s/LATOM3/$myla3/" cpp.get-vb.in
    sed -i "s/PROTATOM1/$mypa1/" cpp.get-vb.in
    sed -i "s/PROTATOM2/$mypa2/" cpp.get-vb.in
    sed -i "s/PROTATOM3/$mypa3/" cpp.get-vb.in

    echo
    echo "cpp.get-vb.txt:"
    cat cpp.get-vb.in; 
    echo

    # create protein-ligand restraints
    cpptraj -i cpp.get-vb.in > std.get-vb.txt
    echo "PROTEIN-LIGAND RESTRAINTS:"
    grep r2 k.RST
    cp k.RST dcrg+vdw/
    cp k.RST rtr/

    #======water============

    cp setup/ligwat.inpcrd ./water-dcrg+vdw/
    # copy all executable files
    cp $mypcl/water-dcrg+vdw/*sh water-dcrg+vdw/
    cp setup/ligwat.prmtop ./water-dcrg+vdw/

    cd $mywd
done
