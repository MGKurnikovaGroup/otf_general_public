#!/bin/bash

# Default flag value
FLAG=""

# Parse command-line arguments using getopts to extract the flag
while getopts ":tg" opt; do
  case ${opt} in
    t )
      FLAG="-t"
      ;;
    g )
      FLAG="-g"
      ;;
    \? )
      echo "Usage: $0 [-t | -g]"
      exit 1
      ;;
  esac
done
shift $((OPTIND -1))

# Store remaining arguments (directories) in an array
directories=("$@")

# Loop through each directory
for X in "$@"
do
    # Copy analysis.py to the directory
    cp analysis_gt.py "$X"
    
    # Change directory to $X
    cd "$X"
    
    # Run analysis.py with the flag
    python3 analysis_gt.py "$FLAG"
    
    # Change back to the original working directory
    cd ..
done

# Run rel_summary_seed.py with all original arguments
python3 rel_summary_seed.py "$@"

