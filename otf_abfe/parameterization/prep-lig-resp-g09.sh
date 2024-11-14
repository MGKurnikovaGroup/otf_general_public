#!/bin/bash

# separate filename and its extension
FULL_LIGNAME=$(basename -- "$1")
LIGNAME="${FULL_LIGNAME%.*}"
LIGEXT="${FULL_LIGNAME##*.}"
echo ligand name: $LIGNAME        extension: $LIGEXT

# create directory for ligand and copy files
mkdir $LIGNAME
mkdir $LIGNAME/setup
cp $1 $LIGNAME/setup/lig_H.$LIGEXT
cp input-for-prep/* $LIGNAME/setup
cd $LIGNAME/setup

# generate gaussian input
antechamber -i lig_H.$LIGEXT -fi $LIGEXT -o lig_gcrt.com -fo gcrt -gv 1 -ge lig_gcrt.gesp -gn "%CPU=0-21" -gm "%Mem=1000MW" -s 2

#run gaussian
date > date.g09.txt
echo "GAUSSIAN: START"
g09 <lig_gcrt.com >lig_gcrt.log
echo "GAUSSIAN: END"
date >> date.g09.txt
grep time lig_gcrt.log
echo

# fit resp charges
antechamber -i lig_gcrt.log -fi gout -o lig_ac.prep -fo prepi -at gaff2 -c resp -s 2 -eq 2 -nc 0

# check for missing parameters
parmchk2 -i lig_ac.prep -f prepi -o lig_ac.frcmod -s gaff2

# generate .pdb file (used as input for tleap)
antechamber -i lig_H.$LIGEXT -fi $LIGEXT -o lig_H.pdb -fo pdb

# generate .lib file
tleap -f tleap.lig_ac.in

## MD input for ligand in water
tleap -f tleap.ligwat.in

## MD input for complex
# here there may be some procedure to
# add waters to the binding site around ligand (e.g. "solvate" program)
tleap -f tleap.complex.in

# delete waters within 1 angstrom of ligand
# otherwise GPU simulations can fail
cpptraj -i cpp.strip-wat.in

# create directory for conventional md simulations
mkdir ../md-complex
mv complex.* ../md-complex/


