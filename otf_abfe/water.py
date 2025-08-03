import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname("otf_helper.py"), '..', '..')))
from otf_helper import parameters
import shutil
import argparse
import subprocess
from pathlib import Path

def run_water(lam):
    target = f"la-{lam}"
    os.chdir(target)
    output = "std.md.txt"

    p_1min = parameters(
        cwd = Path(target),
        name = "min1",
        prev_dir = "..",
        prev_name = "ligwat",
        curr_dir = "1_min",
        curr_name = "ligwat_min1",
        middle_name = "ligwat",
        special_name = "1min",
        raw_name = "ligwat"
    )
    cmd = p_1min.run_pmemd(first = True)
    with open(output, 'w') as f:
        subprocess.run(cmd, stdout = f)

    p_2min = parameters(
        cwd = Path(target),
        name = "min2",
        prev_dir = "1_min",
        prev_name = "ligwat_min1",
        curr_dir = "1_min",
        curr_name = "ligwat_min2",
        middle_name = "ligwat_min2",
        special_name = "2min",
        raw_name = "ligwat"
    )
    cmd = p_2min.run_pmemd()
    with open(output, 'a') as f:
        subprocess.run(cmd, stdout = f)

    p_nvt = parameters(
        cwd = Path(target),
        name = "nvt heating",
        prev_dir = "1_min",
        prev_name = "ligwat_min2",
        curr_dir = "2_nvt",
        curr_name = "ligwat_nvt",
        middle_name = "ligwat_nvt",
        special_name = "nvt",
        raw_name = "ligwat"
    )
    cmd = p_nvt.run_pmemd()
    with open(output, 'a') as f:
        subprocess.run(cmd, stdout = f)

    p_1npt = parameters(
        cwd = Path(target),
        name = "npt1",
        prev_dir = "2_nvt",
        prev_name = "ligwat_nvt",
        curr_dir = "3_npt",
        curr_name = "ligwat_1npt",
        middle_name = "ligwat_1npt",
        special_name = "1_npt",
        raw_name = "ligwat"
    )
    cmd = p_1npt.run_pmemd()
    with open(output, 'a') as f:
        subprocess.run(cmd, stdout = f)

    p_2npt = parameters(
        cwd = Path(target),
        name = "npt2",
        prev_dir = "3_npt",
        prev_name = "ligwat_1npt",
        curr_dir = "3_npt",
        curr_name = "ligwat_2npt",
        middle_name = "ligwat_2npt",
        special_name = "2_npt",
        raw_name = "ligwat"
    )
    cmd = p_2npt.run_pmemd()
    with open(output, 'a') as f:
        subprocess.run(cmd, stdout = f)

    p_3npt = parameters(
        cwd = Path(target),
        name = "npt3",
        prev_dir = "3_npt",
        prev_name = "ligwat_2npt",
        curr_dir = "3_npt",
        curr_name = "ligwat_3npt",
        middle_name = "ligwat_3npt",
        special_name = "3_npt",
        raw_name = "ligwat"
    )
    cmd = p_3npt.run_pmemd()
    with open(output, 'a') as f:
        subprocess.run(cmd, stdout = f)

    p_prod = parameters(
        cwd = Path(target),
        name = "production",
        prev_dir = "3_npt",
        prev_name = "ligwat_3npt",
        curr_dir = "prod",
        curr_name = "ligwat_prod",
        middle_name = "ligwat_prod",
        special_name = "prod",
        raw_name = "ligwat"
    )
    cmd = p_prod.run_pmemd(last = True)
    with open(output, 'a') as f:
        subprocess.run(cmd, stdout = f)

    os.chdir("..")
