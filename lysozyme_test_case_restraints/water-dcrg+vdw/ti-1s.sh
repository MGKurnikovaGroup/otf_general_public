#!/bin/bash
if [ $# -eq 0 ]; then
    echo "No arguments provided"
    exit 1
fi

TIDIRECTORY=$1 # the directory with AMBER input files (.in)
echo Input files are in the directory $TIDIRECTORY
echo
# create directory structure
cp $TIDIRECTORY/dirs.txt ./  # copy the list of directories
xargs mkdir -p < dirs.txt  # create the directories

# copy all executable files
cp $TIDIRECTORY/*sh ./
cp $TIDIRECTORY/dcrg+vdw/*sh dcrg+vdw/ 
cp $TIDIRECTORY/rtr/*sh rtr/ 
cp $TIDIRECTORY/rtr/*py rtr/ 

ls */
echo

# create protein-ligand restraints
cpptraj -i cpp.get-vb.in > std.get-vb.txt
echo "PROTEIN-LIGAND RESTRAINTS:"
grep r2 k.RST
cp k.RST dcrg+vdw/
cp k.RST rtr/
echo 

# create topology for 4 fs simulations by HMassRepartitioning
parmed -i $TIDIRECTORY/parmed.hmass.in

# running dcrg+vdw step (with prot-lig restraints)
date > std.date.txt

cd dcrg+vdw/
cp ../complex.prmtop ../complex4fs.prmtop ../complex.inpcrd ./
./ti.sh $TIDIRECTORY # This script run TI subsequently for each lambda indicated in it
cd ../

date >> std.date.txt

# running a step of adding prot-lig restraints
cd rtr/
cp ../complex4fs.prmtop ./
cp ../dcrg+vdw/la-0.0/prod/complex_prod.inpcrd ./
./py.set-vb.py k.RST  # create .RST files for different lambdas
./ti.sh $TIDIRECTORY # This script run TI subsequently for each lambda indicated in it
cd  ../

date >> std.date.txt
echo "|||||    ALL SIMULATIONS ARE DONE    |||||"
