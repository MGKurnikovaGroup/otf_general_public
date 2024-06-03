#!/bin/bash
if [ $# -eq 0 ]; then
    echo "No arguments provided"
    exit 1
fi

for STEP in "$@"
do

	cd $STEP

	mkdir alchan
	cd alchan

	alchemical_analysis -a AMBER -g -e -p ../la*/prod/complex_prod. -q out -m ti+ti_cubic -s 500 -b 0.9 -t 300 -u kcal > std.b0.9.txt
	alchemical_analysis -a AMBER -g -e -p ../la*/prod/complex_prod. -q out -m ti+ti_cubic -s 500 -b 0.8 -t 300 -u kcal > std.b0.8.txt
	alchemical_analysis -a AMBER -g -e -p ../la*/prod/complex_prod. -q out -m ti+ti_cubic -s 500 -b 0.7 -t 300 -u kcal > std.b0.7.txt
	alchemical_analysis -a AMBER -g -e -p ../la*/prod/complex_prod. -q out -m ti+ti_cubic -s 500 -b 0.6 -t 300 -u kcal > std.b0.6.txt
	alchemical_analysis -a AMBER -g -e -p ../la*/prod/complex_prod. -q out -m ti+ti_cubic -s 500 -b 0.5 -t 300 -u kcal > std.b0.5.txt
	alchemical_analysis -a AMBER -g -e -p ../la*/prod/complex_prod. -q out -m ti+ti_cubic -s 500 -b 0.4 -t 300 -u kcal > std.b0.4.txt
	alchemical_analysis -a AMBER -g -e -p ../la*/prod/complex_prod. -q out -m ti+ti_cubic -s 500 -b 0.3 -t 300 -u kcal > std.b0.3.txt
	alchemical_analysis -a AMBER -g -e -p ../la*/prod/complex_prod. -q out -m ti+ti_cubic -s 500 -b 0.2 -t 300 -u kcal > std.b0.2.txt
	alchemical_analysis -a AMBER -g -e -p ../la*/prod/complex_prod. -q out -m ti+ti_cubic -s 500 -b 0.1 -t 300 -u kcal > std.b0.1.txt
	alchemical_analysis -a AMBER -g -e -p ../la*/prod/complex_prod. -q out -m ti+ti_cubic -s 500 -b 1.0 -t 300 -u kcal > std.b1.0.txt

	tail -n 1 results.txt | sed "s/TOTAL/$STEP/" > ../total.txt
	#awk 'BEGIN {printf "DCRG+VDW "} END{print}' results.txt > ../total.txt
	#sed -i 's/TOTAL://' ../total.txt

	cd ../../

done
