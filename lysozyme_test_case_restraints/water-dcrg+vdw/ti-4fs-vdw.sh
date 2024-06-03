#!/bin/bash
if [ $# -eq 0 ]; then
    echo "No arguments provided"
    exit 1
fi

TIDIRECTORY=$1 # the directory with AMBER input files (.in)
echo Input files are in the directory $TIDIRECTORY
echo

# running dcrg+vdw step (with prot-lig restraints)
date > std.date-dcrgvdw.txt

cd dcrg+vdw/
./ti.sh $TIDIRECTORY # This script run TI subsequently for each lambda indicated in it
cd ../

date >> std.date-dcrgvdw.txt

echo "|||||    ALL SIMULATIONS ARE DONE    |||||"
