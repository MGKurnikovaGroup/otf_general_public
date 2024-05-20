#!/bin/bash
if [ $# -eq 0 ]; then
    echo "No arguments provided"
    exit 1
fi

TIDIRECTORY=$1 # the directory with AMBER input files (.in)
echo Input files are in the directory $TIDIRECTORY
echo

# running dcrg+vdw step (with prot-lig restraints)
date > std.date.txt

cd dcrg+vdw/
./ti.sh $TIDIRECTORY # This script run TI subsequently for each lambda indicated in it
cd ../

date >> std.date.txt

# running a step of adding prot-lig restraints
cd rtr/
cp ../dcrg+vdw/la-0.0/prod/complex_prod.inpcrd ./
./ti.sh $TIDIRECTORY # This script run TI subsequently for each lambda indicated in it
cd  ../

date >> std.date.txt
echo "|||||    ALL SIMULATIONS ARE DONE    |||||"
