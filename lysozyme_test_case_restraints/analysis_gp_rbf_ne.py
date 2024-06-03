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
from sklearn.gaussian_process.kernels import RBF, Matern, ConstantKernel as C
import convergence_test_gp as ct

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
dHdl_ssmp0 = [dHdl[j][auto_list[j][0]:] for j in range(len(dHdl))] #no decorrelation

#Bootstrap 10000 samples
dmean0=[0]
dvar0=[0]
complex_lams = [0]+lam_set
for j in range(len(dHdl_ssmp0)):
    data1=dHdl_ssmp0[j]
    boot_samples1 = [resample(data1, n_samples=len(data1)) for k in range(10000)]
    boot_mean1=np.array([k.mean() for k in boot_samples1])
    dmean0.append(boot_mean1.mean())
    dvar0.append(boot_mean1.std()**2*(2*auto_list[j][1])**.5)
complex_lams.append(1)
dmean0.append(0)
dvar0.append(0)


#Model Data
X=np.array(complex_lams)
y=np.array(dmean0)
dy=np.array(dvar0)/y.std()**2
comp_kernel = RBF(0.1, (.1, 1.0))#Matern(0.1, (1e-4, 1.0), nu=0.5)
x=np.atleast_2d(np.linspace(0,1,101)).T
comp_gp = GaussianProcessRegressor(kernel=comp_kernel, alpha=dy,
                            n_restarts_optimizer=10, normalize_y=True)
comp_gp.fit(X.reshape(-1, 1), y)
print("Complex Kernel")
print(comp_gp.kernel_)
y_pred, sigma = comp_gp.predict(x, return_std=True)

print("Numeric dcrg+vdw: ", np.trapz(dmean0, complex_lams)*k_b*temp)
dg_var = 0
for i in range(len(dvar0)-1):
    dg_var += ((complex_lams[i+1]-complex_lams[i])/2)**2 * (dvar0[i]+dvar0[i+1])
dg_var *= (k_b*temp)**2
print("Numeric dcrg+vdw SE: ", dg_var**.5)
print("GP dcrg+vdw: ", np.trapz(y_pred, x.squeeze())*k_b*temp)
dg_var_gp = 0
for i in range(len(sigma)-1):
    #dg_var_gp += sigma[i]**2*.01
    dg_var_gp += ((x.squeeze()[i+1]-x.squeeze()[i])/2) * (sigma[i]**2+sigma[i+1]**2)
dg_var_gp *= (k_b*temp)**2
print("GP dcrg+vdw SE: ", dg_var_gp**.5)


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
wdHdl_ssmp0 = [wdHdl[j][wauto_list[j][0]:] for j in range(len(wdHdl))]

#Bootstrap 10000 samples
wmean0=[0]
wvar0=[0]
wat_lams = [0]+wlam_set
for j in range(len(wdHdl_ssmp0)):
    data1=wdHdl_ssmp0[j]
    boot_samples1 = [resample(data1, n_samples=len(data1)) for k in range(10000)]
    boot_mean1=np.array([k.mean() for k in boot_samples1])
    wmean0.append(boot_mean1.mean())
    wvar0.append(boot_mean1.std()**2*(2*wauto_list[j][1])**.5)
wat_lams.append(1)
wmean0.append(0)
wvar0.append(0)

#Model Data
Xw=np.array(wat_lams)
yw=np.array(wmean0)
dyw=np.array(wvar0)/yw.std()**2
wcomp_kernel = RBF(0.1, (.1,1.0))#Matern(0.1, (1e-4, 1.0), nu=0.5)
xw=np.atleast_2d(np.linspace(0,1,1001)).T
wcomp_gp = GaussianProcessRegressor(kernel=wcomp_kernel, alpha=dyw,
                            n_restarts_optimizer=10, normalize_y=True)
wcomp_gp.fit(Xw.reshape(-1, 1), yw)
print('WCOMP_KERNEL: ')
print(wcomp_gp.kernel_)
yw_pred, wsigma = wcomp_gp.predict(xw, return_std=True)

print("Numeric water-dcrg+vdw: ", np.trapz(wmean0, wat_lams)*k_b*temp)
dg_varw = 0
for i in range(len(wvar0)-1):
    dg_varw += ((wat_lams[i+1]-wat_lams[i])/2)**2 * (wvar0[i]+wvar0[i+1])
dg_varw *= (k_b*temp)**2
print("Numeric water-dcrg+vdw SE: ", dg_varw**.5)
print("GP water-dcrg+vdw: ", np.trapz(yw_pred, xw.squeeze())*k_b*temp)
dg_varw_gp = 0
for i in range(len(wsigma)-1):
    #dg_varw_gp += wsigma[i]**2*0.001
    dg_varw_gp += ((xw.squeeze()[i+1]-xw.squeeze()[i])/2) * (wsigma[i]**2+wsigma[i+1]**2)
dg_varw_gp *= (k_b*temp)**2
print("GP water-dcrg+vdw SE: ", dg_varw_gp**.5)

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
auto_times=[]
print("rlam set: ", rlam_set)
for j in rlam_set:
    outputs, auto_time =ct.analyze_rtr(j, from_rtr=True)
    rdHdl_ssmp0.append(outputs)
    auto_times.append(auto_time)

#Bootstrap 10000 samples
rmean0=[]
rvar0=[]
rtr_lams = rlam_set
for j in range(len(rdHdl_ssmp0)):
    data1=rdHdl_ssmp0[j]
    boot_samples1 = [resample(data1, n_samples=len(data1)) for k in range(10000)]
    boot_mean1=np.array([k.mean() for k in boot_samples1])
    rmean0.append(boot_mean1.mean())
    rvar0.append(boot_mean1.std()**2*(2*auto_times[j])**.5)

#Model Data
Xr=np.array(rtr_lams)
yr=np.array(rmean0)
dry=np.array(rvar0)/yr.std()**2
rcomp_kernel = RBF(0.1,(.01,1))#Matern(0.1, (1e-4, 1.0), nu=0.5)
xr=np.atleast_2d(np.linspace(0,1,1001)).T
rcomp_gp = GaussianProcessRegressor(kernel=rcomp_kernel, alpha=dry,
                            n_restarts_optimizer=20, normalize_y=True)
rcomp_gp.fit(Xr.reshape(-1, 1), yr)
print('Rcomp Kernel')
print(rcomp_gp.kernel_)
yr_pred, rsigma = rcomp_gp.predict(xr, return_std=True)

print("Numeric rtr: ", np.trapz(rmean0, rtr_lams))
dg_varr = 0
for i in range(len(rvar0)-1):
    dg_varr += ((rtr_lams[i+1]-rtr_lams[i])/2)**2 * (rvar0[i]+rvar0[i+1])
print("Numeric RTR SE: ", dg_varr**.5)
print("GP RTR: ", np.trapz(yr_pred, xr.squeeze()))
dg_varr_gp = 0
for i in range(len(rsigma)-1):
    #dg_varr_gp+=rsigma[i]**2*0.001
    dg_varr_gp += ((xr.squeeze()[i+1]-xr.squeeze()[i])/2) * (rsigma[i]**2+rsigma[i+1]**2)
print("GP RTR SE: ", dg_varr_gp**.5)

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


dG_mean_g = np.trapz(yw_pred, xw.squeeze())*k_b*temp - boresch - np.trapz(yr_pred, xr.squeeze())-np.trapz(y_pred, x.squeeze())*k_b*temp
dG_var = (dg_var_gp+dg_varw_gp+dg_varr_gp)**.5
dcrg_g = np.trapz(y_pred, x.squeeze())*k_b*temp
rtr_g = np.trapz(yr_pred, xr.squeeze())
wat_g = np.trapz(yw_pred, xw.squeeze())*k_b*temp

df_array = np.around([dG_mean_g, dG_var,
                 dcrg_g, dg_var_gp**.5,
                 rtr_g, dg_varr_gp**.5,
                 wat_g, dg_varw_gp**.5,
                 boresch],decimals=2)

df=pd.DataFrame(df_array).transpose()
df.columns=['dG_g', 'dG_se','dcrg_g', 'dcrg_se',
            'rtr_g', 'rtr_se', 'water_g', 'water_se', 'Boresch']

df.to_csv('summary_gp1.dat', sep='\t', index=False)

import matplotlib.pyplot as plt

#plt.plot(xr,yr_pred, color='k')
#plt.plot(xr,yr_pred+rsigma, color='g')
#plt.plot(xr, yr_pred-rsigma, color='g')
#plt.scatter(rtr_lams, rmean0, color='r')
#plt.show()
