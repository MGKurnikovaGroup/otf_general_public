import argparse

from restraint_analysis_functions import *

def main(frac):

    execute(frac)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some data.")
    parser.add_argument('argument', type=str, help="An argument for the script")
    args = parser.parse_args()
    frac = args.argument
    main(frac)


