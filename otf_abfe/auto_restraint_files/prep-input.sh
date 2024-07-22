#!/bin/bash
if [ $# -eq 0 ]; then
    echo "No arguments provided"
    exit 1
fi

TIDIRECTORY=$1 # the directory with AMBER input files (.in)
echo Input files are in the directory $TIDIRECTORY
echo
#Create directory structure
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
#cp $TIDIRECTORY/cpp.get-vb.in ./
#cp $TIDIRECTORY/parmed.hmass.in ./
cp $TIDIRECTORY/sample* ./
cp $TIDIRECTORY/*sh ./
cp $TIDIRECTORY/dcrg+vdw/*sh dcrg+vdw/
cp $TIDIRECTORY/rtr/*sh rtr/
cp $TIDIRECTORY/rtr/*py rtr/

# use names of selected ligand atoms to generate cpp.get-vb.in
myla1=$(awk '{print $1}' vbla.txt)
myla2=$(awk '{print $2}' vbla.txt)
myla3=$(awk '{print $3}' vbla.txt)

mypa1=$(awk '{print $1}' vbla2.txt)
mypa2=$(awk '{print $2}' vbla2.txt)
mypa3=$(awk '{print $3}' vbla2.txt)

#echo awk:   $myla1    $myla2    $myla3
echo "____ vbla.txt:"
cat vbla.txt; echo

sed "s/LATOM1/$myla1/" samplep.cpp.get-vb.in > cpp.get-vb.in
sed -i "s/LATOM2/$myla2/" cpp.get-vb.in
sed -i "s/LATOM3/$myla3/" cpp.get-vb.in
sed -i "s/PROTATOM1/$mypa1/" cpp.get-vb.in
sed -i "s/PROTATOM2/$mypa2/" cpp.get-vb.in
sed -i "s/PROTATOM3/$mypa3/" cpp.get-vb.in


echo "_____ cpp.get-vb.txt:"
cat cpp.get-vb.in; echo

# create protein-ligand restraints
cpptraj -i cpp.get-vb.in > std.get-vb.txt
echo "PROTEIN-LIGAND RESTRAINTS:"
grep r2 k.RST
cp k.RST dcrg+vdw/
cp k.RST rtr/
echo

# create .RST files for different lambdas
cd rtr/
python3 py.set-vb.py k.RST
cp k.RST k-la-1.00.RST
cd ../

ls dcrg+vdw/ rtr/
echo
