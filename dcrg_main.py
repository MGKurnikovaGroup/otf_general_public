import abfe_simulate as abfe
import argparse

#Global Variables
parser = argparse.ArgumentParser()
parser.add_argument('directory_path', type=str, help='absolute path to protocol directory')
parser.add_argument('--convergence_cutoff', type=float, default = .1, help='convergence criteria')
parser.add_argument('--initial_time', type=float, default=2.5, help='initial simulation time in ns')
parser.add_argument('--additional_time', type=float, default=0.5, help='simulation time of additional runs in ns')
parser.add_argument('--first_max', type=float, default=6.5, help='first maximum amount of simulation time')
parser.add_argument('--sec_max', type=float, default=10.5, help='second maximum amount of simulation time')
args=parser.parse_args()

# constants
temp=300.0
k_b = 1.9872041e-3
t_eq = 250 # equilibration time in frames (each frame = 2 ps)



#Initial Simulations at lambda = [.3, .5, .7]
for l in [.025,.05,0.1,.15, 0.2,.25, 0.3, 0.4, 0.5, 0.6, 0.7,.75, 0.8,.85, 0.9,.95, .975]:
    abfe.dcrg_abfe(l, args.directory_path, args.convergence_cutoff, args.initial_time, args.additional_time, args.first_max, args.sec_max)


