import argparse

from restraint_analysis_functions import *

def main(frac, bb, bb2, ligand, pdb):

    execute(frac, bb, bb2, ligand, pdb)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some data.")
    
    parser.add_argument('frac', type=str, help="cutoff fraction")
    parser.add_argument('bb', type=str, help="BB file")
    parser.add_argument('bb2', type=str, help="BB2 file")
    parser.add_argument('ligand', type=str, help="ligand file")
    parser.add_argument('pdb', type=str, help="pdb file")

    args = parser.parse_args()
    
    frac = float(args.frac)
    bb = args.bb
    bb2 = args.bb2
    ligand = args.ligand
    pdb = args.pdb

    main(frac, bb, bb2, ligand, pdb)


