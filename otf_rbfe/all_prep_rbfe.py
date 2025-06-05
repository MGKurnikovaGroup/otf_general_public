##/bin/bash
import glob
import shutil
import os
import sys
import subprocess
import argparse
<<<<<<< HEAD


=======
>>>>>>> 23f29ceafff1db488d17cc5949e6776b30004a8e

# Below we go to the user's home directory and assign the path to "otf_rbfe" to the variable mypcl
home_dir = os.path.expanduser("~")
mypcl = os.path.join(home_dir, "otf_rbfe") #mypcl=$(realpath $(find ~/ -type d -name "otf_rbfe"))

parser = argparse.ArgumentParser()
parser.add_argument('-j', action='store_true')  # This defines a flag '-j'
args = parser.parse_args()


for X in sys.argv[1:]:
	for f in glob.glob(os.path.join(mypcl, "*.py")):  #cp $mypcl/*.py $X
		shutil.copy(f, X)

	for f in glob.glob(os.path.join(mypcl, "site", "*.sh")): #cp $mypcl/site/*.sh $X/site
		shutil.copy(f, os.path.join(X, "site"))

	for f in glob.glob(os.path.join(mypcl, "water", "cpp*")): #cp $mypcl/water/*.sh $X/water
		shutil.copy(f, os.path.join(X, "water"))

	for f in glob.glob(os.path.join(mypcl, "water", "*.sh")): #cp $mypcl/water/cpp* $X/water
		shutil.copy(f, os.path.join(X, "water"))

<<<<<<< HEAD
	os.chdir(X)
	subprocess.run(['python3', "otf_rbfe/write_scmask.py"], check = True) ##use argparse to make this optional. Default should be to run it unless otherwise specified
	os.chdir("..")	
=======

	if not args.j: 	#Only run below if -j not called
		os.chdir(X)
		subprocess.run(['python3', "otf_rbfe/write_scmask.py"], check = True)
		os.chdir("..")	
>>>>>>> 23f29ceafff1db488d17cc5949e6776b30004a8e
