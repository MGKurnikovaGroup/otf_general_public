#!/bin/bash

TIDIR=$1 # the directory with AMBER input files (.in)
echo "|||||    DCRG+VDW    |||||"
#echo Input files are in the directory $TIDIR

for LAMBDA in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9
#for LAMBDA in 0.2 0.5 0.8 1.0
do
        cd la-$LAMBDA/
        echo ">>>    lambda = $LAMBDA "
        cp ../md-equil.sh ../align.sh ./
		. md-equil.sh $TIDIR la-$LAMBDA > std.md.txt # 2>&1
        cd ../
        echo -------------------------------------------
done
