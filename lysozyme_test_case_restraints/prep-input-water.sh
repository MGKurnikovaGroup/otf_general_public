#!/bin/bash
if [ $# -eq 0 ]; then
    echo "No arguments provided"
    exit 1
fi

TIDIRECTORY=$1 # the directory with AMBER input files (.in)
echo Input files are in the directory $TIDIRECTORY
echo
# copy input coordinates
cp setup/ligwat.inpcrd ./water-dcrg+vdw/

# copy all executable files
cp $TIDIRECTORY/water-dcrg+vdw/*sh water-dcrg+vdw/

cp setup/ligwat.prmtop ./water-dcrg+vdw/

ls water-dcrg+vdw/
echo

