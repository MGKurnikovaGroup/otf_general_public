from otf_helper import parameters
import os
import sys
import shutil
import argparser
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname("otf_helper.py"), '..', '..')))

def run_dcrg(lam):
    target = f"la-{lam}"
    os.chdir(target)

    p_1min = parameters(
        Path(target), "min1", "..", "complex", "1_min",
        "complex_min1", "complex", "1min", "complex"
    )
    p_1min.run_pmemd(first = True)

    p_2min = parameters(
        Path(target), "min2", "1_min", "complex_min1", "1_min",
        "complex_min2", "complex_min2", "2min", "complex"
    )
    p_2min.run_pmemd()

    p_nvt = parameters(
        Path(target), "nvt heating", "1_min", "complex_min2", "2_nvt",
        "complex_nvt", "complex_nvt", "nvt", "complex"
    )
    p_nvt.run_pmemd()

    p_1npt = parameters(
        Path(target), "npt1", "2_nvt", "complex_nvt", "3_npt",
        "complex_1npt", "complex_1npt", "1_npt", "complex"
    )
    p_1npt.run_pmemd()

    p_2npt = parameters(
        Path(target), "npt2", "3_npt", "complex_1npt", "3_npt",
        "complex_2npt", "complex_2npt", "2_npt", "complex"
    )
    p_2npt.run_pmemd()

    p_3npt = parameters(
        Path(target), "npt3", "3_npt", "complex_2npt", "3_npt",
        "complex_3npt", "complex_3npt", "3_npt", "complex"
    )
    p_3npt.run_pmemd()

    p_prod = parameters(
        Path(target), "production", "3_npt", "complex_3npt", "prod",
        "complex_prod", "complex_prod", "prod", "complex"
    )
    p_prod.run_pmemd(last = True)

    os.chdir("..")
