##/bin/bash
import glob
import shutil
import os
import sys
import subprocess
import argparse



# Below we go to the user's home directory and assign the path to "otf_rbfe" to the variable mypcl
home_dir = os.pathexpanduser("~")
mypcl = os.path.join(home_dir, "otf_rbfe") #mypcl=$(realpath $(find ~/ -type d -name "otf_rbfe"))



for X in sys.argv[1:]:
	for f in glob.glob(os.path.join(mypcl, "*.py")):  #cp $mypcl/*.py $X
		shutil.copy(f, X)

	for f in glob.glob(os.path.join(mypcl, "site", "*.sh")): #cp $mypcl/site/*.sh $X/site
		shutil.copy(f, os.path.join(X, "site"))

	for f in glob.glob(os.path.join(mypcl, "site" "cpp*")): #cp $mypcl/water/*.sh $X/water
		shutil.copy(f, os.path.join(X, "water"))

	for f in glob.glob(os.path.join(mypcl, "site", "*.sh")): #cp $mypcl/water/cpp* $X/water
		shutil.copy(f, os.path.join(X, "water"))

	os.chdir(X)
	subprocess.run(['python3', "otf_rbfe/write_scmask.py"], check = True) ##use argparse to make this optional. Default should be to run it unless otherwise specified
	os.chdir("..")	
