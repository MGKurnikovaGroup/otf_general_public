#!/bin/bash
if [ $# -eq 0 ]; then
    echo "No arguments provided"
    exit 1
fi

TIDIRECTORY=$1 # the directory with AMBER input files (.in)
echo Input files are in the directory $TIDIRECTORY
echo


date > std.date-rtr.txt

# running a step of adding prot-lig restraints
cd rtr/
./ti.sh $TIDIRECTORY # This script run TI subsequently for each lambda indicated in it
cd  ../

date >> std.date-rtr.txt
echo "|||||    ALL SIMULATIONS ARE DONE    |||||"
