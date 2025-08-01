import otf_helper
import os
import sys
import shutil
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "dirs", nargs = "+", type = Path
    )
    args = parser.parse_args()

    os.chdir(args.dirs[0])

    p_1min = parameters(
        args.dirs[0], "min1", "..", "ligwat", "1_min",
        "ligwat_min1", "ligwat", "1min", "ligwat"
    )
    p_1min.run_pmemd(first = True)

    p_2min = parameters(
        args.dirs[0], "min2", "1_min", "ligwat_min1", "1_min",
        "ligwat_min2", "ligwat_min2", "2min", "ligwat"
    )
    p_2min.run_pmemd()

    p_nvt = parameters(
        args.dirs[0], "nvt heating", "1_min", "ligwat_min2", "2_nvt",
        "ligwat_nvt", "ligwat_nvt", "nvt", "ligwat"
    )
    p_nvt.run_pmemd()

    p_1npt = parameters(
        args.dirs[0], "npt1", "2_nvt", "ligwat_nvt", "3_npt",
        "ligwat_1npt", "ligwat_1npt", "1_npt", "ligwat"
    )
    p_1npt.run_pmemd()

    p_2npt = parameters(
        args.dirs[0], "npt2", "3_npt", "ligwat_1npt", "3_npt",
        "ligwat_2npt", "ligwat_2npt", "2_npt", "ligwat"
    )
    p_2npt.run_pmemd()

    p_3npt = parameters(
        args.dirs[0], "npt3", "3_npt", "ligwat_2npt", "3_npt",
        "ligwat_3npt", "ligwat_3npt", "3_npt", "ligwat"
    )
    p_3npt.run_pmemd()

    p_prod = parameters(
        args.dirs[0], "production", "3_npt", "ligwat_3npt", "prod",
        "ligwat_prod", "ligwat_prod", "prod", "ligwat"
    )
    p_prod.run_pmemd(last = True)

    os.chdir("..")
