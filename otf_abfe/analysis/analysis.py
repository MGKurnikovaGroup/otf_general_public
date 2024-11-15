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

# constants
temp=300.0
k_b = 1.9872041e-3
t_eq = 250 # equilibration time in frames (each frame = 2 ps)
K = 8.314472*0.001  # Gas constant in kJ/mol/K
V = 1.66            # standard volume in nm^3




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
    
#Bootstrap 10000 samples
dmean0=[0]
dvar0=[0]
complex_lams = [0]+lam_set
for j in range(len(dHdl_ssmp0)):
    data1=dHdl_ssmp0[j]
    boot_samples1 = [resample(data1, n_samples=len(data1)) for k in range(10000)]
    boot_mean1=np.array([k.mean() for k in boot_samples1])
    dmean0.append(boot_mean1.mean())
    dvar0.append(boot_mean1.std()**2)
complex_lams.append(1)
dmean0.append(0)
dvar0.append(0)

with open("dcrg_hist.txt", 'w') as f:
    f.write(str(dHdl_ssmp_indices0)+'\n'+str(dvar0))
f.close()

print("dcrg+vdw: ", np.trapz(dmean0, complex_lams)*k_b*temp)
dg_var = 0
for i in range(len(dvar0)-1):
    dg_var += ((complex_lams[i+1]-complex_lams[i])/2)**2 * (dvar0[i]+dvar0[i+1])
dg_var *= (k_b*temp)**2
print("dcrg+vdw SE: ", dg_var**.5)

#WATER STEP
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

#Bootstrap 10000 samples
wmean0=[0]
wvar0=[0]
wat_lams = [0]+wlam_set
for j in range(len(wdHdl_ssmp0)):
    data1=wdHdl_ssmp0[j]
    boot_samples1 = [resample(data1, n_samples=len(data1)) for k in range(10000)]
    boot_mean1=np.array([k.mean() for k in boot_samples1])
    wmean0.append(boot_mean1.mean())
    wvar0.append(boot_mean1.std()**2)
wat_lams.append(1)
wmean0.append(0)
wvar0.append(0)

print("water-dcrg+vdw: ", np.trapz(wmean0, wat_lams)*k_b*temp)
dg_varw = 0
for i in range(len(wvar0)-1):
    dg_varw += ((wat_lams[i+1]-wat_lams[i])/2)**2 * (wvar0[i]+wvar0[i+1])
dg_varw *= (k_b*temp)**2
print("water-dcrg+vdw SE: ", dg_varw**.5)

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
    rdHdl_ssmp0.append(ct.analyze_rtr(j, from_rtr=True))

#Bootstrap 10000 samples
rmean0=[]
rvar0=[]
rtr_lams = rlam_set
for j in range(len(rdHdl_ssmp0)):
    data1=rdHdl_ssmp0[j]
    boot_samples1 = [resample(data1, n_samples=len(data1)) for k in range(10000)]
    boot_mean1=np.array([k.mean() for k in boot_samples1])
    rmean0.append(boot_mean1.mean())
    rvar0.append(boot_mean1.std()**2)

print("rtr: ", np.trapz(rmean0, rtr_lams))
dg_varr = 0
for i in range(len(rvar0)-1):
    dg_varr += ((rtr_lams[i+1]-rtr_lams[i])/2)**2 * (rvar0[i]+rvar0[i+1])
print("rtr SE: ", dg_varr**.5)
ref_list, k_list = ct.parse_lists(True)

#Apply Boresch Formula
r0     = float(ref_list[0])/10      # Distance in nm
thA    = float(ref_list[1])      # Angle in degrees
thB    = float(ref_list[3])     # Angle in degrees

# 1 kcal/(mol*A^2) = 418.4 kJ/(mol*nm^2)
# 1 kcal/(mol*rad^2) = 4.184 kJ/(mol*rad^2)
K_r    = 2*418.4*k_list[0]    # force constant for distance (kJ/mol/nm^2)
K_thA  = 2*4.184*k_list[1]      # force constant for angle (kJ/mol/rad^2)
K_thB  = 2*4.184*k_list[3]      # force constant for angle (kJ/mol/rad^2)
K_phiA = 2*4.184*k_list[2]       # force constant for dihedral (kJ/mol/rad^2)
K_phiB = 2*4.184*k_list[4]     # force constant for dihedral (kJ/mol/rad^2)
K_phiC = 2*4.184*k_list[5]      # force constant for dihedral (kJ/mol/rad^2)

#===================================================================================================
# BORESCH FORMULA
#===================================================================================================

thA = math.radians(thA)  # convert angle from degrees to radians --> math.sin() wants radians
thB = math.radians(thB)  # convert angle from degrees to radians --> math.sin() wants radians
arg =(
    (8.0 * math.pi**2.0 * V) / (r0**2.0 * math.sin(thA) * math.sin(thB))
    *
    (
        ( (K_r * K_thA * K_thB * K_phiA * K_phiB * K_phiC)**0.5 ) / ( (2.0 * math.pi * K * temp)**(3.0) )
    )
)

boresch = - K * temp * math.log(arg)/4.184

print('dG: ', np.trapz(wmean0, wat_lams)*k_b*temp - boresch - np.trapz(rmean0, rtr_lams)*k_b*temp - np.trapz(dmean0, complex_lams)*k_b*temp)

dG_mean_n = np.trapz(wmean0, wat_lams)*k_b*temp - boresch - np.trapz(rmean0, rtr_lams) - np.trapz(dmean0, complex_lams)*k_b*temp
dcrg_n = np.trapz(dmean0, complex_lams)*k_b*temp
rtr_n = np.trapz(rmean0, rtr_lams)
wat_n = np.trapz(wmean0, wat_lams)*k_b*temp

df_array = np.around([dG_mean_n,
                 dcrg_n,
                 rtr_n,
                 wat_n,
                 boresch],decimals=2)

df=pd.DataFrame(df_array).transpose()
df.columns=['dG_n', 'dcrg_n',
            'rtr_n', 'water_n', 'Boresch']

df.to_csv('summary.dat', sep='\t', index=False)

