sys.path.append(os.path.abspath(os.path.join(os.path.dirname("otf_helper.py"), '..', '..')))
from otf_helper import parameters
import os
import argparse
import shutil
from pathlib import Path

def run_rtr(lam):
    print("Reading in input files from the directory")

    target = f"la-{lam}"
    os.chdir(target)
    
    p_prod = parameters(
        Path(target), "production", "..", "complex_prod", "prod",
        "complex_prod", "complex_prod", "prod", "complex"
    )
    p_prod.run_pmemd(first = True, last = True)

    os.chdir("..")
