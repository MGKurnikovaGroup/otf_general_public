import sys
import os
import argparse
import shutil
from pathlib import Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname("otf_helper.py"), '..', '..')))
from otf_helper import parameters

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "dirs", nargs = "+", type = Path
    )
    args = parser.parse_args()

    os.chdir(args.dirs[0])
    #1min
    min1 = parameters(
        args.dirs[0], "min1", "..", "complex", "1_min",
        "complex", "complex", "complex_min1", "complex"
    )
    min1.run_pmemd(first = True, last = True)

    #2min
    min2 = parameters(
        args.dirs[0], "min2", "1_min", "complex_min1", "1_min",
        "complex_min2", "complex_min2", "complex_min2", "complex"
    )
    min2.run_pmemd(first = True, last = True)

    #nvt
    nvt = parameters(
        args.dirs[0], "nvt", "1_min", "complex_min2", "2_nvt",
        "complex_nvt", "complex_nvt", "complex_nvt", "complex"
    )
    nvt.run_pmemd(first = True, last = True)

    #1npt
    npt1 = parameters(
        args.dirs[0], "npt", "2_nvt", "complex_nvt", "3_npt",
        "complex_1npt", "complex_1npt", "complex_1npt", "complex"
    )
    npt1.run_pmemd(first = True, last = True)

    #2npt
    npt2 = parameters(
        args.dirs[0], "npt2", "3_npt", "complex_1npt", "3_npt",
        "complex_2npt", "complex_2npt", "complex_2npt", "complex"
    )
    npt2.run_pmemd(first = True, last = True)

    #3npt
    npt3 = parameters(
        args.dirs[0], "npt3", "3_npt", "complex_2npt", "3_npt",
        "complex_3npt", "complex_3npt", "complex_3npt", "complex"
    )
    npt3.run_pmemd(first = True, last = True)

    #prod
    prod = parameters(
        args.dirs[0], "production", "3_npt", "complex_3npt", "prod",
        "complex_prod", "complex_prod", "complex_prod", "complex"
    )
    prod.run_pmemd(last = True)


    os.chdir("..")
	
