import os
import sys
import argparse
from pathlib import Path
import shutil
import subprocess

"""
Find directory that contains otf_abfe within the home directory,
and return the resolved path.

If the directory is not found, display an error.
"""
def find_dir_abfe():
    home = Path.home()
    for path in home.rglob('otf_abfe'):
        if path.isdir():
            return path.resolve() # mypcl=$(realpath $(find ~/ -type d -name "otf_abfe"))
    sys.stderr.write("Error: Cannot find otf_abfe directory\n")
    sys.exit(1)

"""
Options for writing values of angle, distance, and dihedral to
samplep.cpp.get-vb.in file

Help messages are specified in the description and help variables
"""
def parse_args():
    parser = argparse.ArgumentParser(
            description = "" # Comment displayed at the top when --help is called
            formatter_class = RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '-d', '--distance', type = float, default = 2.0,
        help = "distance (default: 2.0)" # echo "  -d, --distance FLOAT     distance (default: 2.0)"
    )
    parser.add_argument(
        '-a', '--angle', type = float, default = 10.0,
        help = "angle (default: 10.0)" # echo "  -a, --angle FLOAT   angle (default: 10.0)"
    )
    parser.add_argument(
        '-D', '--dihedral', type = float, default = 20.0,
        help = "dihedral (default: 20.0)" # echo "  -D, --dihedral FLOAT   dihedral (default: 20.0)"
    )
    parser.add_argument(
        'dirs', nargs = '+',
        help = "Target directories to process" # Directory parameters stored in $@
    )
    return parser.parse_args() # Return parsed flags

"""
Open vbla.txt and vbla2.txt, splits each line on whitespace, and
returns a list of three strings
"""
def read_atoms(file_path):
    with open(file_path) as f:
        for line in f:
            parts = line.split()
            if len(parts) >= 3:
                return parts[:3] # Values in myla1, myla2, and myla3
        sys.stderr.write(f"Error: {file_path} has less than 3 fields.\n")
        sys.exit(1)

"""
Main procedure
"""
def main():

