#!/bin/bash
if [ $# -eq 0 ]; then
    echo "No arguments provided"
    exit 1
fi

TIDIRECTORY=$1 # the directory with AMBER input files (.in)
echo Input files are in the directory $TIDIRECTORY
echo
# create directory structure
#cp $TIDIRECTORY/dirs.txt ./  # copy the list of directories
#xargs mkdir -p < dirs.txt  # create the directories

# copy all executable files
mkdir water-dcrg+vdw
rsync -av --include="*/" --include="*.sh" --exclude="*" $TIDIRECTORY/water-dcrg+vdw/ ./water-dcrg+vdw/ 

ls water-dcrg+vdw/
echo


# running water-dcrg+vdw step
cd water-dcrg+vdw/
date > std.date.txt

cp ../complex.prmtop ../complex.inpcrd ./
./ti.sh $TIDIRECTORY # This script run TI subsequently for each lambda indicated in it

date >> std.date.txt
cd ../

echo "|||||    ALL SIMULATIONS ARE DONE    |||||"
