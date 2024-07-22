from alchemlyb.parsing.amber import extract_dHdl
import os
import glob
import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np
from pymbar import timeseries
from sklearn.utils import resample
from scipy.spatial.distance import jensenshannon as js

temp=300.0
k_b = 1.9872041e-3
t_eq = .5 #ns

def calc_dvdl(current_values, ref_values, force_constants):
    if len(current_values) == len(ref_values) and len(ref_values) == len(force_constants):
        dvdl = 0
        for i in range(len(current_values)):
            dvdl += force_constants[i]*((float(current_values[i])-ref_values[i])**2)
        return dvdl

    else:
        print('Number of current values, reference values and/or constants is not the same:')
        print(len(current_values),' ',len(ref_values),' ',len(force_constants))

# this function check values of dihedral angles and converts them to a correct range if needed.
# I.e., if reference value is 179 but a raw value at some frame is -175,
# this value should be converted to 185 to obtain a correct dv/dl.
def check_dihedrals(current_values, ref_values):
    checkout = []
    for i in [2,4,5]:
        absdelta = abs(float(current_values[i])-ref_values[i])
        #checkout.append(absdelta)
        if absdelta > 240:
            initial = current_values[i]
            current_values[i] = ref_values[i] - abs(360.0 - absdelta)
            checkout.append(str(i)+' diheral value is changed:  '+str(initial)+'  '+str(current_values[i]))
    return [current_values, checkout]

def parse_constants(lam, from_rtr=False):
    istep1, ntpr, dt, nstlim = 0,0,0,0
    if from_rtr:
        if os.path.exists('./rtr/la-'+lam+'/prod/complex_prod_00.out'):
            file = './rtr/la-'+lam+'/prod/complex_prod_00.out'
        else:
            file = './rtr/la-'+lam+'/prod/complex_prod_0a.out'
    else:
        if os.path.exists('./la-'+lam+'/prod/complex_prod_00.out'):
            file = './la-'+lam+'/prod/complex_prod_00.out'
        elif os.path.exists('./la-'+lam+'/prod/ligwat_prod_00.out'):
            file = './la-'+lam+'/prod/ligwat_prod_00.out'
        elif os.path.exists('./la-'+lam+'/prod/complex_prod_0a.out'):
            file = './la-'+lam+'/prod/complex_prod_0a.out'
        else:
            file = './la-'+lam+'/prod/ligwat_prod_0a.out'
    with open(file, 'r') as f:
        for line in f:
            if istep1 != 0 and dt != 0 and ntpr != 0 and nstlim != 0:
                break
            for s in line.split(", "):
                if "dt" in s and dt == 0:
                    dt = float(s[5:])
                elif "istep1" in s and istep1 == 0:
                    istep1 = int(s[9:])
                elif "ntpr" in s and ntpr == 0:
                    ntpr = int(s[7:])
                elif 'nstlim' in s and nstlim == 0:
                    nstlim = int(s[9:])
    return istep1, ntpr, dt, nstlim

def parse_lists(from_rtr=False):
    ref_list = []
    k_list = []
    if from_rtr:
        file='k.RST'
    else:
        file='../k.RST'
    with open(file, 'r') as f:
        for line in f:
            for s in line.split(", "):
                if "r2" in s:
                    ref_list.append(float(s[3:]))
                elif "rk2" in s:
                    k_list.append(float(s[4:]))
    return ref_list, k_list


def analyze(lam, decorrelate=False):
    #Compile all outputs from lambda window
    #Returns equilibrated and decorrelated timeseries data
    lam = str(lam)
    if 'la' in lam:
        lam = lam.split('-')[1]
    datalist = glob.glob('./la-'+lam+'/prod/*.out*')
    #datalist=['./la-'+lam+'/prod/complex_prod.out']
    datalist.sort()
    dHdl0=[extract_dHdl(i, temp) for i in datalist]
    if len(dHdl0) > 1:
        dHdl=np.array(dHdl0[0]['dHdl'])
        for i in range(len(dHdl0[1:])):
            dHdl=np.concatenate((dHdl,np.array(dHdl0[i+1]['dHdl'])))
    else:
        dHdl=np.array(dHdl0[0]['dHdl'])
    #step1, ntpr, dt, nstlim = parse_constants(lam)
    #dHdl_eq=dHdl[int(float(t_eq)*1000/ntpr/dt+1):]
    auto_list = timeseries.detect_equilibration(dHdl)
    dHdl_eq = dHdl[auto_list[0]:]
    if decorrelate:
        dHdl_ssmp_indices=timeseries.subsample_correlated_data(dHdl_eq, conservative=True)
        dHdl_ssmp = dHdl_eq[dHdl_ssmp_indices]
    else:
        dHdl_ssmp = dHdl_eq
    return dHdl_ssmp



def analyze_rtr(lam, from_rtr = False, decorrelate=False):
    #Compile all outputs from lambda window
    #Returns equilibrated and decorrelated timeseries data
    lam = str(lam)
    if 'la' in lam:
        lam = lam.split('-')[1]
    print(lam)
    if from_rtr:
        datalist=glob.glob('./rtr/la-'+lam+"/rstr*")
    else:
        datalist = glob.glob('./la-'+lam+'/rstr*')
    #datalist=['./la-'+lam+'/prod/complex_prod.out']
    datalist.sort()
    print(datalist)
    ref_list,k_list = parse_lists(from_rtr=from_rtr) 
    print("Ref List: ", ref_list)
    print("K_list: ", k_list)
    dvdl=np.array([])
    rtr_lambda=[]
    new_k = k_list.copy()
    for n in range (1,6):
        new_k[n] = new_k[n]/(57.2958**2)
    if True:
        for filename in datalist:
            dvdls=[]
            cfile = open(filename, 'r') # current file
            lines = cfile.readlines()
            for line in lines:
                cdof = line.split() # current degrees of freedom
                del cdof[0]
                if len(cdof) > 6: del cdof[-1]
                cdof, check_dih = check_dihedrals(cdof, ref_list)
                dvdl_val = calc_dvdl(cdof, ref_list, new_k)
                dvdls.append(dvdl_val)
            dvdl=np.concatenate((dvdl, np.array(dvdls)))
        istep1, ntpr, dt, nstlim = parse_constants(lam, from_rtr=from_rtr)
        #dvdl_eq=dvdl[math.floor(.2*len(dvdl)):]
        #dvdl_eq=dvdl[int(float(t_eq)*1000/istep1/dt+1):]
        auto_list = timeseries.detect_equilibration(dvdl)
        dvdl_eq = dvdl[auto_list[0]:]
        if decorrelate:
            dvdl_ssmp_indices=timeseries.subsample_correlated_data(dvdl_eq, conservative=True)
            dvdl_ssmp = dvdl_eq[dvdl_ssmp_indices]
        else:
            dvdl_ssmp=dvdl_eq
        return dvdl_ssmp




def check_convergence(sample, cutoff):
    #Takes equilibrated and decorrelated np.array
    #Divides set in two and performs jehnsen shannon distance
    #to check for convergence below an arbitrary value
    #returns True if converged, else False
    s_range = np.max(sample) - np.min(sample)
    qs = []
    for i in range(6):
        qs.append(np.min(sample)+(i+1)/7*s_range)
    print(qs,np.median(sample))
    data_1 = sample[:math.floor(len(sample)/2)]
    data_2 = sample[math.floor(len(sample)/2):]
    data_1_bins=[]
    data_2_bins=[]
    for j in range(len(qs)-1):
        num_1 = 0
        num_2 = 0
        if j == 0:
            for k in data_1:
                if k < qs[0]:
                    num_1 += 1
            for k in data_2:
                if k < qs[0]:
                    num_2 += 1
            data_1_bins.append(num_1/len(data_1))
            data_2_bins.append(num_2/len(data_2))
            num_1=0
            num_2=0
        for k in data_1:
            if k < qs[j+1] and k >= qs[j]:
                num_1 += 1
        for k in data_2:
            if k < qs[j+1] and k >= qs[j]:
                num_2 += 1
        data_1_bins.append(num_1/len(data_1))
        data_2_bins.append(num_2/len(data_2))
        if j + 2 == len(qs):
            num_1 = 0
            num_2 = 0
            for k in data_1:
                if k >= qs[j+1]:
                    num_1 += 1
            for k in data_2:
                if k >= qs[j+1]:
                    num_2 += 1
            data_1_bins.append(num_1/len(data_1))
            data_2_bins.append(num_2/len(data_2))
    print('KL Divergence', js(data_1_bins, data_2_bins))
    if js(data_1_bins, data_2_bins) <= cutoff:
        return True, js(data_1_bins, data_2_bins)
    else:
        return False, js(data_1_bins, data_2_bins)
