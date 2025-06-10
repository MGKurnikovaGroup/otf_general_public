import os
import sys
import argparse
from pathlib import Path
import shutil
import subprocess

# Below we go to the user's home directory and assign the path to "otf_rbfe" to the variable mypcl
home_dir = os.path.expanduser("~")
mypcl = os.path.join(home_dir, "otf_rbfe") #mypcl=$(realpath $(find ~/ -type d -name "otf_rbfe"))
