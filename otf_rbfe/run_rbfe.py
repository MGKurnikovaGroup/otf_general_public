import os
import sys
import glob
import argparse
from pathlib import Path
import shutil
import subprocess


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run RBFE setup and simulation",
        usage="run_rbfe.py [OPTIONS] [type: dcrg, water, rtr, all] dir1 dir2 ... dirN"
    )

    parser.add_argument("type", choices=["dcrg", "water", "rtr", "all"])
    parser.add_argument("dirs", nargs="+")

    parser.add_argument('-c', '--convergence-cutoff', type=float, default=0.1)
    parser.add_argument('-i', '--initial-time', type=float, default=2.5)
    parser.add_argument('-a', '--additional-time', type=float, default=0.5)
    parser.add_argument('-f', '--first-max', type=float, default=6.5)
    parser.add_argument('-s', '--second-max', type=float, default=10.5)
    parser.add_argument('-S', '--schedule', type=str, default="equal")
    parser.add_argument('-n', '--num-windows', type=int, default=9)
    parser.add_argument('-C', '--custom-windows', type=str, default="")
    parser.add_argument('-o', '--sssc', type=int, default=2)
    parser.add_argument('-m', '--move-to', type=str, default=".")
    parser.add_argument('-A', '--equil-restr', type=str, default="")
    parser.add_argument('-F', '--fpn-value', type=int, default=0)
    parser.add_argument('-R', '--referance_lam', type=int, default=-1)
    parser.add_argument('-sp', '--special', type=str, default="site")
    parser.add_argument('-T', '--target_lam', type=int, default=-1)
    parser.add_argument('-ctm1', '--custom_ti_mask1', type=str, default="")
    parser.add_argument('-ctm2', '--custom_ti_mask2', type=str, default="")
    parser.add_argument('-ctmw1', '--custom_ti_mask_wat1', type=str, default="")
    parser.add_argument('-ctmw2', '--custom_ti_mask_wat2', type=str, default="")

    print("See README.md for default inputs")
    return parser.parse_args()


# Parse arguments first
args = parse_args()

# Store current working directory
_d = os.getcwd()
print(_d)

# Get full path to otf_rbfe
home_dir = os.path.expanduser("~")
mypcl = os.path.join(home_dir, "otf_rbfe")

# Process each directory
for X in args.dirs:
    os.chdir(X)

    # Copy necessary Python files
    for f in glob.glob(os.path.join(mypcl, "*.py")):
        shutil.copy(f, X)

    shutil.copy("convergence_test.py", os.path.join(X, ".."))

    # Construct full path to scmask.txt
    scmask_path = os.path.join(_d, X, "scmask.txt")

    # Run the main RBFE command
    subprocess.run([
        'python3', "rbfe_main.py", mypcl, args.type, scmask_path,
        "--convergence_cutoff", str(args.convergence_cutoff),
        "--initial_time", str(args.initial_time),
        "--additional_time", str(args.additional_time),
        "--first_max", str(args.first_max),
        "--second_max", str(args.second_max),
        "--schedule", args.schedule,
        "--num_windows", str(args.num_windows),
        "--custom_windows", args.custom_windows,
        "--sssc", str(args.sssc),
        "--special", args.special,
        "--equil_restr", args.equil_restr,
        "--fpn", str(args.fpn_value),
        "--reference_lam", str(args.referance_lam),
        "--target_lam", str(args.target_lam),
        "--ctm1", args.custom_ti_mask1,
        "--ctm2", args.custom_ti_mask2,
        "--ctmw1", args.custom_ti_mask_wat1,
        "--ctmw2", args.custom_ti_mask_wat2
    ], check=True)

    os.chdir("..")
    shutil.move(X, args.move_to)

