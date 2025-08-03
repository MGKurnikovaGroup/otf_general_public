import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname("otf_helper.py"), '..', '..')))
from otf_helper import parameters
import argparse
import shutil
import subprocess
from pathlib import Path

def run_rtr(lam):
    print("Reading in input files from the directory")

    target = f"la-{lam}"
    os.chdir(target)
    
    p_prod = parameters(
        Path.cwd(), "production", "..", "complex_prod", "prod",
        "complex_prod", "complex_prod", "prod", "complex"
    )
    cmd = p_prod.run_pmemd(first = True, last = True)

    path = "std.md.txt"
    with open(path, 'w') as f:
        subprocess.call(cmd, stdout = f)

    os.chdir("..")
