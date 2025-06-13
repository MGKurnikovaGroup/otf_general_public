import sys
import os
import shutil
import subprocess
import argparse
from pathlib import Path

# Setup sys.path to import from parent
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from otf_helper import parameters

def run_pmemd(params: parameters, step: str, prev_step: str):
    cmd = [
        "pmemd.cuda", "-O",
        "-i", str(params.curr_dir / f"{params.special_name}.in"),
        "-p", str(Path(params.prev_dir) / f"{params.raw_name}.prmtop"),
        "-c", str(params.curr_dir / f"{params.curr_name}_{prev_step}.rst"),
        "-x", str(params.curr_dir / f"{params.curr_name}_{step}.nc"),
        "-o", str(params.curr_dir / f"{params.curr_name}_{step}.out"),
        "-r", str(params.curr_dir / f"{params.curr_name}_{step}.rst"),
        "-ref", str(params.curr_dir / f"{params.curr_name}_{prev_step}.rst")
    ]
    subprocess.run(cmd, check=True)

def run_restart():
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", type=Path)
    parser.add_argument("step", type=str)       # corresponds to $2
    parser.add_argument("prev_step", type=str)  # corresponds to $3
    args = parser.parse_args()

    os.chdir(args.dir)
    print(f"echo Reading in input files from the directory {args.dir}")
    print("    production")

    param1 = parameters(
        cwd=Path.cwd(),
        name="production",
        prev_dir="..",
        prev_name="complex",
        curr_dir=Path("prod"),
        curr_name="complex_prod",
        middle_name="",
        special_name="restart",
        raw_name="complex"
    )

    run_pmemd(param1, step=args.step, prev_step=args.prev_step)
    os.chdir("..")

run_restart()



