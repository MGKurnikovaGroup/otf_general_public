#!/bin/bash
# Exit immediately if a command exits with a non-zero status
set -e
# install the package using setup.py from the repo root
$PYTHON -m pip install . --no-deps --ignore-installed -vv

