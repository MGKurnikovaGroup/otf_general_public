import sys
import rbfe_simulate as rbfe
import argparse
import numpy as np
import glob
from alchemlyb.parsing.amber import extract_dHdl
import pymbar.timeseries as timeseries

# constants
temp=300.0
k_b = 1.9872041e-3
K = 8.314472*0.001  # Gas constant in kJ/mol/K
V = 1.66            # standard volume in nm^3

def lambda_ends_index(i, lam_set):
    for j in range(len(lam_set)-1):
        if i <= lam_set[j+1]:
            return (j,j+1)
def linear_int(l,r,fl,fr,x):
    return ((fr-fl)/(r-l))*(x-l)+fl

#Global Variables
parser = argparse.ArgumentParser()
parser.add_argument('directory_path', type=str, help='absolute path to protocol directory')
parser.add_argument('in_loc', type=str, help='absolute path scmask fields')
parser.add_argument('--convergence_cutoff', type=float, default = .1, help='convergence criteria')
parser.add_argument('--initial_time', type=float, default=2.5, help='initial simulation time in ns')
parser.add_argument('--additional_time', type=float, default=0.5, help='simulation time of additional runs in ns')
parser.add_argument('--first_max', type=float, default=6.5, help='first maximum amount of simulation time')
parser.add_argument('--sec_max', type=float, default=6.5, help='second maximum amount of simulation time')
args=parser.parse_args()


#Initial Simulations at lambda = [.3, .5, .7]
for l in [0.01592, 0.08198, 0.19331, 0.33787, 0.5, 0.66213, 0.80669, 0.91802,0.98408]:
    if l != 0.98408:
        rbfe.site_rbfe(l, args.directory_path, args.convergence_cutoff, args.in_loc, args.initial_time, args.additional_time, args.first_max, args.sec_max)
        rbfe.water_rbfe(l, args.directory_path, args.convergence_cutoff, args.in_loc, args.initial_time, args.additional_time, args.first_max, args.sec_max)
    else:
        rbfe.site_rbfe(l, args.directory_path, args.convergence_cutoff, args.in_loc, args.initial_time, args.additional_time, args.first_max, args.sec_max,reference_lam=0.91802)
        rbfe.water_rbfe(l, args.directory_path, args.convergence_cutoff, args.in_loc, args.initial_time, args.additional_time, args.first_max, args.sec_max,reference_lam=0.91802)
