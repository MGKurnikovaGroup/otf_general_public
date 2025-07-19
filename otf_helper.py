from pathlib import Path
import os
import sys
import subprocess
import shutil

class parameters():
    def __init__(self, cwd : Path, name : str, prev_dir : str, prev_name : str,
            curr_dir : str, curr_name : str, middle_name : str,
            special_name : str, raw_name : str):
        self.name = name # name in echo
        self.cwd = cwd # current working directory
        self.curr_dir = curr_dir # current directory in Path object
        self.curr_name = curr_name # current file name (file name of the destination of the first copy command, exclude filename extension)
        self.prev_dir = prev_dir # previous directory (if previous directory is ../complex.inpcrd, then prev_dir is "..", prev_name is "complex" or "")
        self.prev_name = prev_name # previous file name
        self.middle_name = middle_name # file name between copies
        self.special_name = special_name # name before .in that is different from all others
        self.raw_name = raw_name # name just before .prmtop

    def run_pmemd(self, first : bool = False, last : bool = False):
        print(f"    {self.name}")
        if first:
            shutil.copy(f"{self.prev_dir}/{self.prev_name}.inpcrd", f"{self.curr_dir}/{self.middle_name}.inpcrd") # First copy ...
        else:
            shutil.copy(f"{self.prev_dir}/{self.prev_name}.rst", f"{self.curr_dir}/{self.middle_name}.inpcrd") # First copy ...
        shutil.copy(f"{self.curr_dir}/{self.middle_name}.inpcrd", f"{self.curr_dir}/{self.curr_name}_ref.rst") # Second copy ...
        if last:
            cmd = [
                'pmemd.cuda', '-O',
                '-i', f"{self.curr_dir}/{self.special_name}.in",
                '-p', f"../{self.raw_name}.prmtop",
                '-c', f"{self.curr_dir}/{self.middle_name}.inpcrd",
                '-x', f"{self.curr_dir}/{self.curr_name}_00.nc",
                '-o', f"{self.curr_dir}/{self.curr_name}_00.out",
                '-r', f"{self.curr_dir}/{self.curr_name}_00.rst",
                '-ref', f"{self.curr_dir}/{self.curr_name}_ref.rst"
            ]
        else:
            cmd = [
                'pmemd.cuda', '-O',
                '-i', f"{self.curr_dir}/{self.special_name}.in",
                '-p', f"../{self.raw_name}.prmtop",
                '-c', f"{self.curr_dir}/{self.middle_name}.inpcrd",
                '-x', f"{self.curr_dir}/{self.curr_name}.nc",
                '-o', f"{self.curr_dir}/{self.curr_name}.out",
                '-r', f"{self.curr_dir}/{self.curr_name}.rst",
                '-ref', f"{self.curr_dir}/{self.curr_name}_ref.rst"
            ]
        return cmd
