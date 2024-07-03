import abfe_simulate as abfe
import argparse

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
args=parser.parse_args()


#Initial Simulations at lambda = [0.0, .2, .5, 1]
for l in [0.0, 0.05, 0.1, 0.2, 0.3, 0.5, 1.0]:
    abfe.rtr_abfe(l, args.directory_path, args.convergence_cutoff,  args.initial_time, args.additional_time, args.first_max, args.sec_max)
