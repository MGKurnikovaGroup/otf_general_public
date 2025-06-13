sys.path.append(os.path.abspath(os.path.join(os.path.dirname("otf_helper.py"), '..', '..')))
from otf_helper import parameters
import os
import argparse
import shutil
from pathlib import Path

def run_rtr():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "dirs", nargs = "+", type = Path
    )
    args = parser.parse_args()

    print("Reading in input files from the directory")

    os.chdir(args.dirs[0])
    
    p_prod = parameters(
        args.dirs[0], "production", "..", "complex_prod", "prod",
        "complex_prod", "complex_prod", "prod", "complex"
    )
    p_prod.run_pmemd(first = True, last = True)

    os.chdir("..")
