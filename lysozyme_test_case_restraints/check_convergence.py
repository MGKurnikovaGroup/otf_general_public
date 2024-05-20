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
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
import convergence_test as ct

# constants
temp=300.0
k_b = 1.9872041e-3
t_eq = 250 # equilibration time in frames (each frame = 2 ps)
K = 8.314472*0.001  # Gas constant in kJ/mol/K
V = 1.66            # standard volume in nm^3


conv_file=open('converge_check2.txt', 'w')

#COMPLEX STEP
dcrglist0 = glob.glob('./dcrg+vdw/la*/prod/*.out*')
dcrglist0.sort()
dHdl0=[extract_dHdl(j, temp) for j in dcrglist0]
    #Compile List of Output files into processed data by lambda
lam_set = []
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
#dHdl_eq0=[j[t_eq:] for j in dHdl]
auto_list = [timeseries.detect_equilibration(j) for j in dHdl]
dHdl_eq0 = [dHdl[j][auto_list[j][0]:] for j in range(len(dHdl))]
dHdl_ssmp_indices0=[timeseries.subsample_correlated_data(j, conservative=True) for j in dHdl_eq0]
dHdl_ssmp0 = [dHdl_eq0[j][dHdl_ssmp_indices0[j]] for j in range(len(dHdl_eq0))]
for i in range(len(dHdl_ssmp0)):
    if not ct.check_convergence(dHdl_ssmp0[i], .1)[0]:
        #if len(dHdl_ssmp0[i]) < 50:
        conv_file.write('dcrg+vdw: ' + str(i)+' '+str(ct.check_convergence(dHdl_ssmp0[i],.1)[1])+'\n')

watlist0 = glob.glob('./water-dcrg+vdw/la*/prod/*.out*')
watlist0.sort()
wdHdl0=[extract_dHdl(j, temp) for j in watlist0]
    #Compile List of Output files into processed data by lambda
wlam_set = []
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
#wdHdl_eq0=[j[t_eq:] for j in wdHdl]
wauto_list = [timeseries.detect_equilibration(j) for j in wdHdl]
wdHdl_eq0 = [wdHdl[j][wauto_list[j][0]:] for j in range(len(wdHdl))]
wdHdl_ssmp_indices0=[timeseries.subsample_correlated_data(j, conservative=True) for j in wdHdl_eq0]
wdHdl_ssmp0 = [wdHdl_eq0[j][wdHdl_ssmp_indices0[j]] for j in range(len(wdHdl_eq0))]
for i in range(len(wdHdl_ssmp0)):
    if not ct.check_convergence(wdHdl_ssmp0[i], .1)[0]:
        #if len(wdHdl_ssmp0[i]) < 50:
        conv_file.write('water-dcrg+vdw: ' + str(i)+' '+str(ct.check_convergence(wdHdl_ssmp0[i],.1)[1])+'\n')

## RTR STEP

rtrlist0 = glob.glob('./rtr/la*/prod/*.out')
rtrlist0.sort()
    #Compile List of Output files into processed data by lambda
rlam_set = []
last_lam = 0
for j in range(len(rtrlist0)):
    rlam_set.append(float(rtrlist0[j].split('/')[2].split('-')[1]))
    if last_lam != rlam_set[-1]:
        last_lam = rlam_set[-1]
rlam_set = list(set(rlam_set))
rlam_set = sorted(rlam_set)
rdHdl_ssmp0=[]
print("rlam set: ", rlam_set)
for j in rlam_set:
    if float(j) == 0:
        sets = ct.analyze_rtr(j, from_rtr=True)
        for i in sets:
            rdHdl_ssmp0.append(i)
    else:
        rdHdl_ssmp0.append(ct.analyze_rtr(j, from_rtr=True))
for i in range(len(rdHdl_ssmp0)):
    if not ct.check_convergence(rdHdl_ssmp0[i], .1)[0] and i not in [0,1,2]:
        #if len(rdHdl_ssmp0[i]) < 50:
        conv_file.write('rtr: ' + str(i)+' '+str(ct.check_convergence(rdHdl_ssmp0[i],.1)[1])+'\n')
conv_file.close()
