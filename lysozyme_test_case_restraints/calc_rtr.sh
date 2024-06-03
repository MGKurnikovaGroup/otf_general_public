#!/bin/bash

# This script calculates dG for addition and removal of restraints
cd rtr/
###
mkdir add rmv

# calculating dG for addition of restraints (from MD simulations)
cp get_rst_dG.py add/
cp la*/rstr* add/
cp ../dcrg+vdw/la-0.0/rstr_prod.dat add/rstr_1.0
# files with restraint values should have names of view "rstrp_{float number}"
# e.g., rstrp_0.2 
cd add/
python3 ./get_rst_dG.py ../k.RST rstr*

echo "================================="
cat total.txt
cd ../

# calculating dG for removal of restraints (using analytical formula)
cp boresch_formula.py rmv/
cd rmv/
python2 ./boresch_formula.py ../k.RST
echo "================================="
cat total.txt
cd ../
###
cat add/total.txt rmv/total.txt > total.txt
cd ../

# write dG of all steps to a single file 
#cat dcrg+vdw/total.txt rtr/add/total.txt rtr/rmv/total.txt > final.txt
