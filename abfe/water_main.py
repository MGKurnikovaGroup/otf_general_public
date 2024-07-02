import abfe_simulate as abfe
import argparse
import numpy as np

# constants
temp=300.0
k_b = 1.9872041e-3
t_eq = 250 # equilibration time in frames (each frame = 2 ps)


#Global Variables
parser = argparse.ArgumentParser()
parser.add_argument('directory_path', type=str, help='absolute path to protocol directory')
parser.add_argument('--convergence_cutoff', type=float, default = .1, help='convergence criteria')
parser.add_argument('--initial_time', type=float, default=2.5, help='initial simulation time in ns')
parser.add_argument('--additional_time', type=float, default=0.5, help='simulation time of additional runs in ns')
parser.add_argument('--first_max', type=float, default=6.5, help='first maximum amount of simulation time')
parser.add_argument('--sec_max', type=float, default=10.5, help='second maximum amount of simulation time')

parser.add_argument('--schedule', type=str, default='equal', help='schedule for lambda windows')
parser.add_argument('--num_windows', type=int, default=10, help='number of lambda windows')
parser.add_argument('--custom_windows', type=str, default=None, help='list of lambda windows')

args=parser.parse_args()

#schedule: equal, gaussian, custom, throw error otherwise
if args.schedule.lower() == 'equal':
    lambdas = [i/args.num_windows for i in range(args.num_windows)]
elif args.schedule.lower() == 'gaussian':
    lambdas = [0.5 * (1 - np.cos(np.pi * i / args.num_windows)) for i in range(args.num_windows)]
elif args.schedule.lower() == 'custom':
    lambdas = [float(i) for i in args.custom_windows.split(',')]
else:
    raise ValueError('schedule must be equal, gaussian, or custom')

print(lambdas)

#rtr can only be custom


#Initial Simulations at lambda = [.3, .5, .7]
# for l in lambdas:
#     abfe.water_abfe(l, args.directory_path, args.convergence_cutoff, args.initial_time, args.additional_time, args.first_max, args.sec_max)


