import os
import sys
import argparse
from pathlib import Path
import shutil
import subprocess

# Below we go to the user's home directory and assign the path to "otf_rbfe" to the variable mypcl
_d = os.getcwd()
print(_d)
home_dir = os.path.expanduser("~")
mypcl = os.path.join(home_dir, "otf_rbfe") #mypcl=$(realpath $(find ~/ -type d -name "otf_rbfe"))

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

    parser.add_argument(
        '-c', '--convergance-cutoff', type = float, default = 0.1,
        help = "Set convergance cutoff" # echo "  -c, --convergence-cutoff VALUE   Set convergence cutoff"
    )
    parser.add_argument(
        '-i', '--initial-time', type = float, default = 2.5,
        help = "Set initial time"  # echo "  -i, --initial-time VALUE         Set initial time"
    )
    parser.add_argument(
        '-a', '--additional-time', type = float, default = 0.5,
        help = "Set additional time" # echo "  -a, --additional-time VALUE      Set additional time"
    )
    parser.add_argument(
        '-f', '--first-max', type = float, default = 6.5,
        help = "Set first max value" # echo "  -a, --additional-time VALUE      Set additional time"
    )
    parser.add_argument(
        '-s', '--second-max', type = float, default = 10.5,
        help = "Set second max value" # echo "  -a, --additional-time VALUE      Set additional time"
    )
    parser.add_argument(
        '-S', '--schedule', type = str, default = "equal",
        help = "Set schedule" # echo "  -a, --additional-time VALUE      Set additional time"
    )
    parser.add_argument(
        '-n', '--num-windows', type = int, default = 9,
        help = "Set number of windows" # echo "  -a, --additional-time VALUE      Set additional time"
    )
    parser.add_argument(
        '-C', '--custom-windows', type = str, default = "equal",
        help = "Set schedule" #  TODO check with ben
    )
    parser.add_argument(
        '-o', '--sssc', type = int, default = 2,
        help = "Set sssc alpha and beta options (1, 2)" # echo "  -a, --additional-time VALUE      Set additional time"
    )
    parser.add_argument(
        '-m', '--move-to', type = str, default = ".",
        help = "Set destination directory" # echo "  -a, --additional-time VALUE      Set additional time"
    )
    parser.add_argument(
        '-A', '--equil-restr', type = str, default = "",
        help = "Set additional restraints" # echo "  -a, --additional-time VALUE      Set additional time"
    )
    parser.add_argument(
        '-F', '--fpn-value', type = int, default = 0,
        help = "Set number of frames to save per ns" # echo "  -a, --additional-time VALUE      Set additional time"
    )
    parser.add_argument(
        '-R', '--referance_lam', type = int, default = -1,
        help = "Special treatment for broken trajectories" # echo "  -a, --additional-time VALUE      Set additional time"
    )
    parser.add_argument(
        '-sp', '--special', type = str, default = "site",
        help = "Use site or water" # echo "  -a, --additional-time VALUE      Set additional time"
    )
    parser.add_argument(
        '-T', '--target_lam', type = int, default = -1,
        help = "Special treatment for broken trajectory equil" # echo "  -a, --additional-time VALUE      Set additional time"
    )
    parser.add_argument(
        '-ctm1', '--custom_ti_mask', type = str, default = "",
        help = "Custom masks for protein-ligand complex TI for lig1" # echo "  -a, --additional-time VALUE      Set additional time"
    )
    parser.add_argument(
        '-ctm2', '--custom_ti_mask', type = str, default = "",
        help = "Custom masks for protein-ligand complex TI for lig2" # echo "  -a, --additional-time VALUE      Set additional time"
    )
    parser.add_argument(
        '-ctmw1', '--custom_ti_mask', type = str, default = "",
        help = "Custom masks for solvated ligand TI for lig1" # echo "  -a, --additional-time VALUE      Set additional time"
    )
    parser.add_argument(
        '-ctmw2', '--custom_ti_mask', type = str, default = "",
        help = "Custom masks for solvated ligand TI for lig2" # echo "  -a, --additional-time VALUE      Set additional time"
    )
    parser.add_argument(
        'dirs', nargs = '+',
        help = "Target directories to process" # Directory parameters stored in $@
    )
    print("See README.md for default inputs")
    return parser.parse_args() # Return parsed flags






