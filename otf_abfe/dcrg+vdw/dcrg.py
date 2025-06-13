from otf_helper import parameters
import os
import shutil
import argparser
from pathlib import Path

def run_dcrg():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "dirs", nargs = "+", type = Path
    )
    args = parser.parse_args()

    os.chdir(args.dirs[0])

    p_1min = parameters(
        args.dirs[0], "min1", "..", "complex", "1_min",
        "complex_min1", "complex", "1min", "complex"
    )
    p_1min.run_pmemd(first = True)

    p_2min = parameters(
        args.dirs[0], "min2", "1_min", "complex_min1", "1_min",
        "complex_min2", "complex_min2", "2min", "complex"
    )
    p_2min.run_pmemd()

    p_nvt = parameters(
        args.dirs[0], "nvt heating", "1_min", "complex_min2", "2_nvt",
        "complex_nvt", "complex_nvt", "nvt", "complex"
    )
    p_nvt.run_pmemd()

    p_1npt = parameters(
        args.dirs[0], "npt1", "2_nvt", "complex_nvt", "3_npt",
        "complex_1npt", "complex_1npt", "1_npt", "complex"
    )
    p_1npt.run_pmemd()

    p_2npt = parameters(
        args.dirs[0], "npt2", "3_npt", "complex_1npt", "3_npt",
        "complex_2npt", "complex_2npt", "2_npt", "complex"
    )
    p_2npt.run_pmemd()

    p_3npt = parameters(
        args.dirs[0], "npt3", "3_npt", "complex_2npt", "3_npt",
        "complex_3npt", "complex_3npt", "3_npt", "complex"
    )
    p_3npt.run_pmemd()

    p_prod = parameters(
        args.dirs[0], "production", "3_npt", "complex_3npt", "prod",
        "complex_prod", "complex_prod", "prod", "complex"
    )
    p_prod.run_pmemd(last = True)

    os.chdir("..")
