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
parser.add_argument('type', type=str, help='type of execution: site, water, all')
parser.add_argument('in_loc', type=str, help='absolute path scmask fields')
parser.add_argument('--convergence_cutoff', type=float, default = .1, help='convergence criteria')
parser.add_argument('--initial_time', type=float, default=2.5, help='initial simulation time in ns')
parser.add_argument('--additional_time', type=float, default=0.5, help='simulation time of additional runs in ns')
parser.add_argument('--first_max', type=float, default=6.5, help='first maximum amount of simulation time')
parser.add_argument('--second_max', type=float, default=6.5, help='second maximum amount of simulation time')

parser.add_argument('--schedule', type=str, default='equal', help='schedule for lambda windows')
parser.add_argument('--num_windows', type=int, default=9, help='number of lambda windows')
parser.add_argument('--custom_windows', type=str, default=None, help='list of lambda windows for dcrg and water (comma delimited)')
parser.add_argument('--sssc', type=int, default=2, help='sssc option (1, 2)')
parser.add_argument('--special', type=str, default='site', help='special option for site or water (only relevant when target_lam =! -)')
parser.add_argument('--equil_restr', type=str, default='', help='additional restraints to add for equilibration, amber mask format')
parser.add_argument('--target_lam', type=float, default='-1', help='enter the target lambda window for special treatment pf lambda equilibration')
parser.add_argument('--reference_lam', type=float, default='-1', help='enter the lambda window to be referenced for special treatment of lambda equilibration')
parser.add_argument('--fpn', type=int, default=0, help='trajectory frames per nanosecond to be saved')
parser.add_argument('--ctm1', type=str, default='', help='custom amber mask for timask1 for protein-ligand complex')
parser.add_argument('--ctm2', type=str, default='', help='custom amber mask for timask2 for protein-ligand complex')
parser.add_argument('--ctmw1', type=str, default='', help='custom amber mask for timask1 for solvated ligand')
parser.add_argument('--ctmw2', type=str, default='', help='custom amber mask for timask2 for solvated ligand')

args=parser.parse_args()

gaussian_windows = {1:[0.5],
                    2:[0.21132,0.78867],
                    3:[0.11270,0.5,0.88729],
                    5:[0.04691,0.23076,0.5,0.76923,0.95308],
                    7:[0.02544,0.12923,0.29707,0.5,0.70292,0.87076,0.97455],
                    9:[0.01592,0.08198,0.19331,0.33787,0.5,0.66213,0.80669,0.91802,0.98408],
                    12:[0.00922,0.04794,0.11505,0.20634,0.31608,0.43738,0.56262,0.68392,0.79366,0.88495,0.95206,0.99078]}

ctm = [args.ctm1, args.ctm2]
ctmw= [args.ctmw1, args.ctmw2]
print("CTM", ctm)
if args.schedule.lower() == 'equal':
    if args.sssc == 0:
        lambdas = [i/(args.num_windows-1) for i in range(args.num_windows)]
    else:
        assert(args.sssc == 2 or args.ssc == 1)
        lambdas = [(i+1)/(args.num_windows+1) for i in range(args.num_windows)]
elif args.schedule.lower() == 'gaussian':
    if args.num_windows not in gaussian_windows:
        raise ValueError('Gaussian window not available for this number of windows')
    lambdas = gaussian_windows[args.num_windows]
elif args.schedule.lower() == 'custom':
    if args.custom_windows is None:
        raise ValueError('Custom schedule requires custom windows')
    lambdas = [float(i) for i in args.custom_windows.split(',')]
else:
    raise ValueError('schedule must be equal, gaussian, or custom')

if args.target_lam != -1:
    # Check if target_lam exists in lambdas
    if args.target_lam not in lambdas:
        raise ValueError(f'Target lambda {args.target_lam} not found in the lambda schedule')

    if args.reference_lam != -1:
        # Check if reference_lam exists in lambdas
        if args.reference_lam not in lambdas:
            raise ValueError(f'Reference lambda {args.reference_lam} not found in the lambda schedule')
        # Ensure reference_lam is in schedule
        print(f'Target lambda {args.target_lam} will be referenced with lambda {args.reference_lam}')
    else:
        # Find the closest lambda to target_lam in the lambdas list
        target_index = lambdas.index(args.target_lam)
        target=lambdas.pop(target_index)
        closest_lam = min(lambdas, key=lambda x: abs(x - args.target_lam))
        args.reference_lam = closest_lam
        print(f'Target lambda {args.target_lam} will be referenced with the closest lambda {closest_lam}')

    # Reorder the lambdas list: reference first, target last, others in between
    remaining_lambdas = [lam for lam in lambdas if lam not in [args.reference_lam, args.target_lam]]
    ordered_lambdas = [args.reference_lam] + remaining_lambdas + [args.target_lam]
    lambdas=ordered_lambdas
    print(f'New lambda schedule: {ordered_lambdas}')
##Throw exception if args.special != site or water

if args.type == 'site': 
    for l in lambdas:
        rbfe.site_rbfe(l, args.directory_path, args.convergence_cutoff, args.in_loc, args.initial_time, args.additional_time, args.first_max, args.second_max, sssc=args.sssc, add_restr=args.equil_restr, target_lam=args.target_lam, reference_lam=args.reference_lam,special=args.special, fpn=args.fpn, ctm=ctm)
elif args.type == 'water':
    for l in lambdas:
        rbfe.water_rbfe(l, args.directory_path, args.convergence_cutoff, args.in_loc, args.initial_time, args.additional_time, args.first_max, args.second_max, sssc=args.sssc, target_lam=args.target_lam, reference_lam=args.reference_lam, fpn=args.fpn, special=args.special,ctmw=ctmw)
elif args.type == 'all':
    for l in lambdas:
        if args.special == 'site' and args.target_lam != -1:
            print('site and target_lam', args.target_lam)
            rbfe.site_rbfe(l, args.directory_path, args.convergence_cutoff, args.in_loc, args.initial_time, args.additional_time, args.first_max, args.second_max, sssc=args.sssc,add_restr=args.equil_restr, target_lam=args.target_lam, reference_lam=args.reference_lam, fpn=args.fpn, special=args.special,ctm=ctm)
            rbfe.water_rbfe(l, args.directory_path, args.convergence_cutoff, args.in_loc, args.initial_time, args.additional_time, args.first_max, args.second_max, sssc=args.sssc, target_lam=-1, reference_lam=-1, fpn=args.fpn,ctmw=ctmw)
        elif args.special == 'water' and args.target_lam != -1:
            rbfe.site_rbfe(l, args.directory_path, args.convergence_cutoff, args.in_loc, args.initial_time, args.additional_time, args.first_max, args.second_max, sssc=args.sssc,add_restr=args.equil_restr, target_lam=-1, reference_lam=-1, fpn=args.fpn,ctm=ctm)
            rbfe.water_rbfe(l, args.directory_path, args.convergence_cutoff, args.in_loc, args.initial_time, args.additional_time, args.first_max, args.second_max, sssc=args.sssc, target_lam=args.target_lam, reference_lam=args.reference_lam, fpn=args.fpn, special=args.special,ctmw=ctmw)
        else:
            rbfe.site_rbfe(l, args.directory_path, args.convergence_cutoff, args.in_loc, args.initial_time, args.additional_time, args.first_max, args.second_max, sssc=args.sssc,add_restr=args.equil_restr, target_lam=-1, reference_lam=-1, fpn=args.fpn,ctm=ctm)
            rbfe.water_rbfe(l, args.directory_path, args.convergence_cutoff, args.in_loc, args.initial_time, args.additional_time, args.first_max, args.second_max, sssc=args.sssc, target_lam=args.target_lam, reference_lam=args.reference_lam, fpn=args.fpn,ctmw=ctmw)
else:
    raise ValueError('type must be site, water, or all')

