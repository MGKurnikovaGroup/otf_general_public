import abfe_simulate
import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('directory_path', type=str, help='absolute path to protocol directory')
parser.add_argument('type', type=str, help='type of execution: dcrg, water, rtr')
parser.add_argument('--convergence_cutoff', type=float, default = .1, help='convergence criteria')
parser.add_argument('--initial_time', type=float, default=2.5, help='initial simulation time in ns')
parser.add_argument('--additional_time', type=float, default=0.5, help='simulation time of additional runs in ns')
parser.add_argument('--first_max', type=float, default=6.5, help='first maximum amount of simulation time')
parser.add_argument('--second_max', type=float, default=10.5, help='second maximum amount of simulation time')

parser.add_argument('--schedule', type=str, default='equal', help='schedule for lambda windows')
parser.add_argument('--num_windows', type=int, default=10, help='number of lambda windows')
parser.add_argument('--custom_windows', type=str, default=None, help='list of lambda windows')

args=parser.parse_args()

gaussian_windows = {1:[0.5],
                    2:[0.21132,0.78867],
                    3:[0.11270,0.5,0.88729],
                    5:[0.04691,0.23076,0.5,0.76923,0.95308],
                    7:[0.02544,0.12923,0.29707,0.5,0.70292,0.87076,0.97455],
                    9:[0.01592,0.08198,0.19331,0.33787,0.5,0.66213,0.80669,0.91802,0.98408],
                    12:[0.00922,0.04794,0.11505,0.20634,0.31608,0.43738,0.56262,0.68392,0.79366,0.88495,0.95206,0.99078]}

#Creating lambda windows
if args.schedule.lower() == 'equal':
    lambdas = [i/args.num_windows for i in range(args.num_windows)]
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


#Executions (dcrg, water, rtr)
if args.type == 'dcrg':
    for l in lambdas:
        abfe_simulate.dcrg_abfe(l, args.directory_path, args.convergence_cutoff, args.initial_time, args.additional_time, args.first_max, args.second_max)

elif args.type == 'water':
    for l in lambdas:
        abfe_simulate.water_abfe(l, args.directory_path, args.convergence_cutoff, args.initial_time, args.additional_time, args.first_max, args.second_max)

elif args.type == 'rtr':
    for l in lambdas:
        abfe_simulate.rtr_abfe(l, args.directory_path, args.convergence_cutoff,  args.initial_time, args.additional_time, args.first_max, args.second_max)

else:
    raise ValueError('type must be dcrg, water, or rtr')