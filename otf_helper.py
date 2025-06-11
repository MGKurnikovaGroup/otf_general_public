from pathlib import Path
import os
import sys
import shutil
import shutil
import argparse

class parameters():
    def __init__(self, cwd : Path, name : str, prev_dir : str, prev_name : str,
            curr_dir : str, curr_name : str, middle_name : str, 
            special_name : str):
        self.name = name # name in echo
        self.cwd = cwd # current working directory
        self.curr_dir = curr_dir # current directory in Path object
        self.curr_name = curr_name # current file name (file name of the destination of the first copy command, exclude filename extension)
        self.middle_name = middle_name # this variable is used to deal with the special case in the first run chunk
        self.prev_dir = prev_dir # previous directory (if previous directory is ../complex.inpcrd, then prev_dir is "..", prev_name is "complex" or "")
        self.prev_name = prev_name # previous file name
        self.special_name = special_name # name before .in that is different from all others

    def run_pmemd(self, last : bool = False):
        mywd = Path.cwd().resolve() # cwd
        cmd = [
            'pmemd.cuda', '-O',
            '-i', self.cwd / self.curr_dir / (self.special_name + '.in')
        ] # All flags and file names that is going to be run
        subprocess.run(cmd, cwd = mywd, check = True)
