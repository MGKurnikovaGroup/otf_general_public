from alchemlyb.parsing.amber import extract_dHdl
import os
import glob
import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np
from pymbar import timeseries
import sys
from sklearn.utils import resample
import convergence_test as ct
import argparse

# constants
temp=300.0
k_b = 1.9872041e-3
t_eq = 250 # equilibration time in frames (each frame = 2 ps)
K = 8.314472*0.001  # Gas constant in kJ/mol/K
V = 1.66            # standard volume in nm^3
weights=[0.04064,0.09032,0.13031,0.15617,0.16512] # for gaussian quadrature
w_i = [4-abs(x-4) for x in range(9)]
weights2 = [weights[i] for i in w_i] # all 9 weights corresponding to lambdas sorted in ascending order

def lambda_ends_index(i, lam_set):
    for j in range(len(lam_set)-1):
        if i <= lam_set[j+1]:
            return (j,j+1)
def linear_int(l,r,fl,fr,x):
    return ((fr-fl)/(r-l))*(x-l)+fl
#COMPLEX STEP
dcrglist0 = glob.glob('./site/la*/prod/*.out*')
dcrglist0.sort()
dHdl0=[extract_dHdl(j, temp) for j in dcrglist0]
    #Compile List of Output files into processed data by lambda
lam_set = [0]
dHdl=[]
last_lam = 0
for j in range(len(dcrglist0)):
    lam_set.append(float(dcrglist0[j].split('/')[2].split('-')[1]))
    if last_lam == lam_set[-1]:
        working_array=np.concatenate((working_array, np.array(dHdl0[j]['dHdl'])))
    else:
        if j == 0:
            working_array=np.array(dHdl0[j]['dHdl'])
        else:
            dHdl.append(working_array)
            working_array=np.array(dHdl0[j]['dHdl'])
        last_lam = lam_set[-1]
dHdl.append(working_array)
lam_set = list(set(lam_set))
lam_set = sorted(lam_set)
lam_set.append(1)
#dHdl_eq0=[j[t_eq:] for j in dHdl]
auto_list = [timeseries.detect_equilibration(j) for j in dHdl]
dHdl_ssmp0 = [dHdl[j][auto_list[j][0]:] for j in range(len(dHdl))]
    
#Bootstrap 10000 samples
dmean0=[0]
dvar0=[0]
for j in range(len(dHdl_ssmp0)):
    data1=dHdl_ssmp0[j]
    dmean0.append(data1.mean())
    dvar0.append(data1.std()**2/len(data1)*auto_list[j][1])
dmean0.append(0)
dvar0.append(0)

#WATER STEP
watlist0 = glob.glob('./water/la*/prod/*.out*')
watlist0.sort()
wdHdl0=[extract_dHdl(j, temp) for j in watlist0]
    #Compile List of Output files into processed data by lambda
wlam_set = [0]
wdHdl=[]
last_lam = 0
for j in range(len(watlist0)):
    wlam_set.append(float(watlist0[j].split('/')[2].split('-')[1]))
    if last_lam == wlam_set[-1]:
        working_array=np.concatenate((working_array, np.array(wdHdl0[j]['dHdl'])))
    else:
        if j == 0:
            working_array=np.array(wdHdl0[j]['dHdl'])
        else:
            wdHdl.append(working_array)
            working_array=np.array(wdHdl0[j]['dHdl'])
        last_lam = wlam_set[-1]
wdHdl.append(working_array)
wlam_set = list(set(wlam_set))
wlam_set = sorted(wlam_set)
wlam_set.append(1)
#wdHdl_eq0=[j[t_eq:] for j in wdHdl]
wauto_list = [timeseries.detect_equilibration(j) for j in wdHdl]
wdHdl_ssmp0 = [wdHdl[j][wauto_list[j][0]:] for j in range(len(wdHdl))]

#Bootstrap 10000 samples
wmean0=[0]
wvar0=[0]
for j in range(len(wdHdl_ssmp0)):
    data1=wdHdl_ssmp0[j]
    wmean0.append(data1.mean())
    wvar0.append(data1.std()**2/len(data1)*wauto_list[j][1])
wmean0.append(0)
wvar0.append(0)

cmean0=np.array(dmean0)-np.array(wmean0)
cvar0=np.array(wvar0)+np.array(dvar0)

parser = argparse.ArgumentParser()
parser.add_argument('-t', action='store_true')  # This defines a flag '-t'
parser.add_argument('-g', action='store_true')  # This defines a flag '-g'
args = parser.parse_args()

if args.t: # Trapezoid rule
    df=pd.DataFrame([np.trapz(cmean0, lam_set), np.trapz(cvar0, lam_set)**.5]).transpose()
    print(df)
else: # Gaussian quadrature (default; args.g)
    if len(cmean0[1:-1]) == 12:
        df=pd.DataFrame([np.dot(cmean0[1:-1],np.array([.02359, .05347, .08004, .10158, .11675, .12457, .12457, .11675, .10158, .08004, .05347, .02359])),
            np.dot(cvar0[1:-1],np.array([.02359, .05347, .08004, .10158, .11675, .12457, .12457, .11675, .10158, .08004, .05347, .02359]))**.5]).transpose()
    elif len(cmean0[1:-1])==9:
        df=pd.DataFrame([np.dot(cmean0[1:-1], np.array(weights2)), np.dot(cvar0[1:-1], np.array(weights2))**.5]).transpose()

df.columns=["ddG","standard error"]
df.to_csv('lam_seed.csv', index=False)
