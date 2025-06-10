import os
import sys
import argparse
import shutil
import glob
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

def parse_args():
    parser = argparse.ArgumentParser(
        description = "",
        usage = "Usage: $0 [OPTIONS] [type: dcrg, water, rtr, all] dir1 dir2 ... dirN"
    ) # echo "Usage: ..."

    parser.add_argument(
        "type",
        choices = ["dcrg", "water", "rtr", "all"]
    ) # type = $1
    parser.add_argument(
        "dirs",
        nargs = "+"
    ) # shift 1

    parser.add_argument("-c", "--convergence-cutoff", type = float, default = 0.1,
                        help = "Set convergence cutoff")
    parser.add_argument("-i", "--initial-time", type = float, default = 2.5,
                        help = "Set initial time")
    parser.add_argument("-a", "--additional-time", type = float, default = 0.5,
                        help = "Set additional time")
    parser.add_argument("-f", "--first-max", type = float, default = 6.5,
                        help = "Set first max value")
    parser.add_argument("-s", "--second-max", type = float, default = 10.5,
                        help = "Set second max value")
    parser.add_argument("-S", "--schedule", default = "equal",
                        help = "Set schedule")
    parser.add_argument("-n", "--num-windows", type = int, default = 10,
                        help = "Set number of windows")
    parser.add_argument("-C", "--custom-windows", default = "",
                        metavar = "x,y,z", help = "Set custom windows")
    parser.add_argument("-r", "--rtr-window", default = "0.0,0.05,0.1,0.2,0.5,1.0",
                        metavar = "x,y,z", help = "Set rtr window")
    parser.add_argument("-o", "--sssc", type = int, default = 2,
                        help = "Set sssc alpha and beta options (1,2)")
    parser.add_argument("-m", "--move-to", default = ".",
                        metavar = "DEST", help = "Set destination directory")
    parser.add_argument("-A", "--equil_restr", default = "",
                        help = "Set additional restraints")
    parser.add_argument("-F", "--fpn", type = int,
                        dest = "frames_per_ns", default = 0,
                        help = "Set number of frames to save per ns")
    return parser.parse_args()

def main():
    mywd = Path.cwd().resolve() # mywd=$(pwd)
    mypcl = find_dir_abfe() # directory of otf_abfe
    args = parse_args() # process parameters

    print(f"""convergence_cutoff = {args.convergence_cutoff}
    initial_time = {args.initial_time}
    additional_time = {args.additional_time}
    first_max = {args.first_max}
    second_max = {args.second_max}
    schedule = {args.schedule}
    num_windows = {args.num_windows}
    custom_windows = {args.custom_windows}
    rtr_window = {args.}
