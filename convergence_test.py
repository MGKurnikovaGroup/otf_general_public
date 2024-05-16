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


def parse_constants(lam, from_rtr=False): #used to update MD input constants
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
                if "dt" in s and dt == 0: #time step in picoseconds, typically 0.001 or 0.002
                    dt = float(s[5:])
                elif "istep1" in s and istep1 == 0: #used for restraints, not super important for RBFE
                    istep1 = int(s[9:])
                elif "ntpr" in s and ntpr == 0: #frequency in timestep for outputing to the .out file
                    ntpr = int(s[7:])
                elif 'nstlim' in s and nstlim == 0: #number of timesteps for the simulation
                    nstlim = int(s[9:])
    return istep1, ntpr, dt, nstlim

def parse_lists(from_rtr=False): #used for ABFE simulations, not important for RBFE
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
    print('DL Divergence', js(data_1_bins, data_2_bins))
    if js(data_1_bins, data_2_bins) <= cutoff:
        return True, js(data_1_bins, data_2_bins)
    else:
        return False, js(data_1_bins, data_2_bins)
