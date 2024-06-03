#!/bin/bash
for LAMBDA in 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0 #0.75 0.85 0.95 0.65 0.5 0.4 0.1 0.2
#for LAMBDA in 0.85
do
	echo lambda = $LAMBDA 
	cd la-$LAMBDA/
	#mv equil*/* ./
	rm -rf equil*
	cd ../
	#cd prod/
	#echo lambda = $LAMBDA production
	#. ti_prod.sh > std 2>&1
	#cd ../../
	echo 
done

