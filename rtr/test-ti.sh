#!/bin/bash

echo "|||||    ADDING RESTRAINTS (VBA)    |||||"

TIDIR=$1 # the directory with AMBER input files (.in)
echo Input files are in the directory $TIDIR

for LAMBDA in 1.00
# for LAMBDA in 0.0 0.65 0.75 0.85 0.95
do
	cd la-$LAMBDA/
	echo ">>>    lambda = $LAMBDA"
	cp ../k-la-$LAMBDA.RST ./
	cp ../md-lambda.sh ./	
	. md-lambda.sh $TIDIR la-$LAMBDA > std 2>&1
	cd ../
	echo 
done

