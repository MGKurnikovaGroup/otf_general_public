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
'''
#Model Displacement
disp=[] #displacement^2 from calculated values
sigma_a=[] #alleotoric variance calculated by linear interpolation
sigma_e=[] #epistemic variance (displacent^2-sigma_a)
sigma_eu=[] #unit epistemic variance
calcs_range=np.arange(lam_set[0], lam_set[-1]+.00001, .00001)
for i in range(len(lam_set)-2):
    disp.append((dmean0[i+1]-linear_int(lam_set[i],lam_set[i+2],dmean0[i],dmean0[i+2],lam_set[i+1]))**2)
    #sigma_e.append(disp[i]-dvar0[i+1])
    sigma_a.append(linear_int(lam_set[i],lam_set[i+2],dvar0[i],dvar0[i+2],lam_set[i+1]))
    if disp[i] >= sigma_a[i]:
        sigma_e.append(disp[i]-sigma_a[i])
    else:
        sigma_e.append(0)
    sigma_eu.append(sigma_e[i]*(lam_set[i+2]-lam_set[i])/((lam_set[i+2]-lam_set[i+1])*(lam_set[i+1]-lam_set[i])))
    if i == 0 or i == len(lam_set)-3:
        #sigma_eu.append(sigma_e[i]*(lam_set[i+2]-lam_set[i])/((lam_set[i+2]-lam_set[i+1])*(lam_set[i+1]-lam_set[i])))
        sigma_eu.append(sigma_e[i]*(lam_set[i+2]-lam_set[i])/((lam_set[i+2]-lam_set[i+1])*(lam_set[i+1]-lam_set[i])))
sigma_eu0=[] #unit epistemic variance on nonsimulated points
sigma_e0=[] #epistemic variance on nonsimulated points
sigma_a0=[] #alleotoric variance of nonsimulated points calculated by interpolation
interpolated_means=[]
for i in calcs_range:
    endpoints=lambda_ends_index(i,lam_set)
    sigma_a0.append(linear_int(lam_set[endpoints[0]],lam_set[endpoints[1]],dvar0[endpoints[0]],dvar0[endpoints[1]],i))
    interpolated_means.append(linear_int(lam_set[endpoints[0]],lam_set[endpoints[1]],dmean0[endpoints[0]],dmean0[endpoints[1]],i)) 
    sigma_eu0.append(linear_int(lam_set[endpoints[0]],lam_set[endpoints[1]],sigma_eu[endpoints[0]], sigma_eu[endpoints[1]],i))
    sigma_e0.append(sigma_eu0[-1]*(lam_set[endpoints[1]]-i)*(i-lam_set[endpoints[0]])/(lam_set[endpoints[1]]-lam_set[endpoints[0]]))

sigma_e0=np.array(sigma_e0)
sigma_a0=np.array(sigma_a0)
sigma0=sigma_e0+sigma_a0

#Extrapolation
#We're going to estimate the uncertainty as uncertainty of the corresponding point from the opposite side
#of the endpoint
high_extrap=np.arange(lam_set[-1]+.00001, 1.00001, .00001)
low_extrap=np.arange(0,lam_set[0],.00001)
high_means=np.flip(dmean0[-1]+(dmean0[-1]-dmean0[-2])/(lam_set[-1]-lam_set[-2])*(1-high_extrap))
low_means=dmean0[0]-(dmean0[1]-dmean0[0])/(lam_set[1]-lam_set[0])*(lam_set[0]-low_extrap)
low_vars=sigma0[1:len(low_extrap)+1]
high_vars=np.flip(sigma0[-(len(high_extrap)+1):-1])
high_means *= k_b*temp
high_vars=high_vars**.5*k_b*temp
low_means *= k_b*temp
low_vars=low_vars**.5*k_b*temp
interpolated_means=np.array(interpolated_means)*k_b*temp
sigma0=sigma0**.5*k_b*temp
var0=sigma0**2
dmean0=np.array(dmean0)*k_b*temp

import matplotlib.pyplot as plt
plt.plot(high_extrap,high_means, color='g')
plt.plot(high_extrap,high_means+high_vars, color='b')
plt.plot(high_extrap,high_means-high_vars, color='b')
plt.plot(low_extrap,low_means, color='g')
plt.plot(low_extrap,low_means+low_vars, color='b')
plt.plot(low_extrap,low_means-low_vars, color='b')
plt.plot(calcs_range,interpolated_means)
plt.plot(calcs_range,interpolated_means+sigma0, color='r')
plt.plot(calcs_range,interpolated_means-sigma0, color='r')
plt.scatter(lam_set, dmean0, color='k')
plt.title('Overall Error (1 sigma)')
#plt.ylim(-150,-110)
plt.show()

plt.plot(calcs_range,sigma0)
plt.show()

#plt.plot(calcs_range,interpolated_means)
#plt.plot(calcs_range,interpolated_means+sigma_a0, color='r')
#plt.plot(calcs_range,interpolated_means-sigma_a0, color='r')
#plt.title('Alleotoric Error (1 sigma)')
#plt.scatter(lam_set, dmean0, color='k')
#plt.ylim(-150,-110)
#plt.show()

#plt.plot(calcs_range,interpolated_means)
#plt.plot(calcs_range,interpolated_means+sigma_e0, color='r')
#plt.plot(calcs_range,interpolated_means-sigma_e0, color='r')
#plt.title('Epistemic Error (1 sigma)')
#plt.scatter(lam_set, dmean0, color='k')
#plt.ylim(-150,-110)
#plt.show()
'''

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

#print(wvar0)
#Model Displacement
cdisp=[] #displacement^2 from calculated values
csigma_a=[] #alleotoric variance calculated by linear interpolation
csigma_e=[] #epistemic variance (displacent^2-sigma_a)
csigma_eu=[] #unit epistemic variance
ccalcs_range=np.arange(lam_set[0], lam_set[-1]+.00001, .00001)
for i in range(len(lam_set)-2):
    cdisp.append((cmean0[i+1]-linear_int(lam_set[i],lam_set[i+2],cmean0[i],cmean0[i+2],lam_set[i+1]))**2)
    #wsigma_e.append(wdisp[i]-wvar0[i+1])
    csigma_a.append(linear_int(wlam_set[i],wlam_set[i+2],cvar0[i],cvar0[i+2],wlam_set[i+1]))
    if cdisp[i] >= csigma_a[i]:
        csigma_e.append(cdisp[i]-csigma_a[i])
    else:
        csigma_e.append(0)
    csigma_eu.append(csigma_e[i]*(lam_set[i+2]-lam_set[i])/((lam_set[i+2]-wlam_set[i+1])*(wlam_set[i+1]-wlam_set[i])))
    if i == 0:
        csigma_eu.append(csigma_e[i]*(wlam_set[i+2]-wlam_set[i])/((wlam_set[i+2]-wlam_set[i+1])*(wlam_set[i+1]-wlam_set[i])))
    if i == len(wlam_set)-3:
        #wsigma_eu.append(wsigma_e[i]*(wlam_set[i+2]-wlam_set[i])/((wlam_set[i+2]-wlam_set[i+1])*(wlam_set[i+1]-wlam_set[i])))
        csigma_eu.append(csigma_e[i]*(wlam_set[i+2]-wlam_set[i])/((wlam_set[i+2]-wlam_set[i+1])*(wlam_set[i+1]-wlam_set[i])))
csigma_eu0=[] #unit epistemic variance on nonsimulated points
csigma_e0=[] #epistemic variance on nonsimulated points
csigma_a0=[] #alleotoric variance of nonsimulated points calculated by interpolation
cinterpolated_means=[]
#print(wdisp)
#print(wsigma_a)
#print(wsigma_eu)
#print(wsigma_a)
for i in ccalcs_range:
    endpoints=lambda_ends_index(i,wlam_set)
    a0 = linear_int(wlam_set[endpoints[0]],wlam_set[endpoints[1]],cvar0[endpoints[0]],cvar0[endpoints[1]],i)
    if a0 < 0:
        csigma_a0.append(0)
    else:
        csigma_a0.append(linear_int(wlam_set[endpoints[0]],wlam_set[endpoints[1]],cvar0[endpoints[0]],cvar0[endpoints[1]],i))
    cinterpolated_means.append(linear_int(wlam_set[endpoints[0]],wlam_set[endpoints[1]],cmean0[endpoints[0]],cmean0[endpoints[1]],i))
    csigma_eu0.append(linear_int(wlam_set[endpoints[0]],wlam_set[endpoints[1]],csigma_eu[endpoints[0]], csigma_eu[endpoints[1]],i))
    csigma_e0.append(csigma_eu0[-1]*(wlam_set[endpoints[1]]-i)*(i-wlam_set[endpoints[0]])/(wlam_set[endpoints[1]]-wlam_set[endpoints[0]]))

csigma_e0=np.array(csigma_e0)
csigma_a0=np.array(csigma_a0)
csigma0=csigma_e0+csigma_a0
csigma0=csigma0**.5*k_b*temp
cmean0=np.array(cmean0)*k_b*temp

'''
plt.plot(chigh_extrap,chigh_means, color='g')
plt.plot(chigh_extrap,chigh_means+chigh_vars, color='b')
plt.plot(chigh_extrap,chigh_means-chigh_vars, color='b')
plt.plot(clow_extrap,clow_means, color='g')
plt.plot(clow_extrap,clow_means+clow_vars, color='b')
plt.plot(clow_extrap,clow_means-clow_vars, color='b')
plt.plot(ccalcs_range,cinterpolated_means)
plt.plot(ccalcs_range,cinterpolated_means+csigma0, color='r')
plt.plot(ccalcs_range,cinterpolated_means-csigma0, color='r')
plt.scatter(wlam_set, cmean0, color='k')
plt.title('Overall Error (1 sigma)')
#plt.ylim(-150,-110)
plt.show()

#plt.plot(calcs_range,winterpolated_means)
#plt.plot(calcs_range,winterpolated_means+wsigma_a0, color='r')
#plt.plot(calcs_range,winterpolated_means-wsigma_a0, color='r')
#plt.title('Alleotoric Error (1 sigma)')
#plt.scatter(wlam_set, wmean0, color='k')
#plt.ylim(-150,-110)
#plt.show()

#plt.plot(calcs_range,winterpolated_means)
#plt.plot(calcs_range,winterpolated_means+wsigma_e0, color='r')
#plt.plot(calcs_range,winterpolated_means-wsigma_e0, color='r')
#plt.title('Epistemic Error (1 sigma)')
#plt.scatter(wlam_set, wmean0, color='k')
#plt.ylim(-150,-110)
#plt.show()

'''
print('Overall Error')
overall_error=sum(csigma0**2)*.00001
print(overall_error**.5)

#df_array = np.around([ddG_site-ddG_wat, (dg_varw_gp+dg_var_gp)**.5,
#                 ddG_site, dg_var_gp**.5,
#                 ddG_wat, dg_varw_gp],decimals=2)

#df=pd.DataFrame(df_array).transpose()
#df.columns=['ddG', 'ddG_sd', 'Site', 'Site_sd',
#            'Water', 'Water_sd']

#df.to_csv('summary_brown.dat', sep='\t', index=False)
df=pd.DataFrame([np.trapz(cmean0, lam_set), overall_error**.5]).transpose()
df.columns=["ddG","error"]
df.to_csv('lam_seed.csv', index=False)
