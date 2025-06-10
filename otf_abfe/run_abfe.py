import os
import sys
import argparse
from pathlib import Path
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
        if path.is_dir():
            return path.resolve() # mypcl=$(realpath $(find ~/ -type d -name "otf_abfe"))
    sys.stderr.write("Error: Cannot find otf_abfe directory\n")
    sys.exit(1)

def parse_args():
    parser = argparse.ArgumentParser(
        usage = "$0 [OPTIONS] [type: dcrg, water, rtr, all] dir1 dir2 ... dirN",
        epilog = "See README.md for default inputs."
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
                        metavar = "x,y,z", help = "Set explicit custom windows")
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
    rtr_window = {args.rtr_window}
    type = {args.type}
    sssc = {args.sssc}
    directories = {args.dirs}
    otf_abfe directory: {mypcl}
    moving to: {args.move_to}""") # echo "..."

    for X in args.dirs: # for X in "$@" do ... done
        print(f"===== {X} =======================")
        target = Path(X)
        if not target.is_absolute():
            target = mywd / target
        target = target.resolve()
        if not target.is_dir():
            sys.stderr.write(f"Warning: {target} is not a directory, skipping.\n")
            continue
        os.chdir(target) # cd $X

        for f in mypcl.glob('*.py'):
            shutil.copy(f, target) # cp $mypcl/*.py .
        shutil.copy(mypcl.parent / "convergence_test.py", target) # cp $mypcl/../convergence_test.py .

        cmd = [
            "python3", "abfe_main.py",
            mypcl, args.type,
            "--convergence-cutoff", str(args.convergence_cutoff),
            "--initial_time", str(args.initial_time),
            "--additional_time", str(args.additional_time),
            "--first_max", str(args.first_max),
            "--second_max", str(args.second_max),
            "--schedule", str(args.schedule),
            "--num_windows", str(args.num_windows),
            "--custom_windows", str(args.custom_windows),
            "--rtr_window", str(args.rtr_window),
            "--sssc", str(args.sssc),
            "--equil_rest", str(args.equil_restr),
            "--fpn", str(args.frames_per_ns)
        ]
        subprocess.run(cmd, cwd = target, check = True) # python3 abfe_main.py ...
        
        os.chdir(target.parent) # cd ..
        dst_parent = Path(args.move_to)
        dst_parent.mkdir(parents = True, exist_ok = True) # Make the directory args.move_to if it does not exist
        shutil.move(target, dst_parent) # mv $X "$move_to"

if __name__ == '__main__':
    main()
