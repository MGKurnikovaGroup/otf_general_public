#!/bin/bash
if [ $# -eq 0 ]; then
    echo "No arguments provided"
    exit 1
fi

TIDIRECTORY=$1 # the directory with AMBER input files (.in)
echo Input files are in the directory $TIDIRECTORY
echo

cd dcrg+vdw
echo ; echo "====  dcrg+vdw  ============="; echo
date > date.txt
./ti.sh $TIDIRECTORY # This script run TI subsequently for each lambda indicated in it
date >> date.txt
cd  ../

echo "|||||    ALL SIMULATIONS ARE DONE    |||||"

