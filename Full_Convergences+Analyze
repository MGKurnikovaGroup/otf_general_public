from alchemlyb.parsing.amber import extract_dHdl
import os
import glob
import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np
from pymbar import timeseries
from sklearn.utils import resample
from scipy.spatial.distance import jensenshannon as js #A function to compute the Jensen-Shannon divergence

# Constants
temp = 300.0  # Temp in Kelvin
k_b = 1.9872041e-3  # Boltzmann constant 
t_eq = 0.5  # Equilibration time in ns

# Function to parse constants from MD output files:untouched 

def parse_constants(lam, from_rtr=False):
    istep1, ntpr, dt, nstlim = 0, 0, 0, 0
    if from_rtr:#ooks for files in specific directories
        if os.path.exists(f'./rtr/la-{lam}/prod/complex_prod_00.out'):
            file = f'./rtr/la-{lam}/prod/complex_prod_00.out'
        else:
            file = f'./rtr/la-{lam}/prod/complex_prod_0a.out'
    else:
        if os.path.exists(f'./la-{lam}/prod/complex_prod_00.out'):
            file = f'./la-{lam}/prod/complex_prod_00.out'
        elif os.path.exists(f'./la-{lam}/prod/ligwat_prod_00.out'):
            file = f'./la-{lam}/prod/ligwat_prod_00.out'
        elif os.path.exists(f'./la-{lam}/prod/complex_prod_0a.out'):
            file = f'./la-{lam}/prod/complex_prod_0a.out'
        else:
            file = f'./la-{lam}/prod/ligwat_prod_0a.out'
    
    with open(file, 'r') as f:
        for line in f:
            if istep1 != 0 and dt != 0 and ntpr != 0 and nstlim != 0:
                break
            for s in line.split(", "):
                if "dt" in s and dt == 0:
                    #dt = float(s[5:])  # Time step in picoseconds
                    dt = float(s[5:].strip())  # Time step in picoseconds

                elif "istep1" in s and istep1 == 0:
                    istep1 = int(s[9:])  # Restraints step
                elif "ntpr" in s and ntpr == 0:
                    ntpr = int(s[7:])  # Frequency of output
                elif 'nstlim' in s and nstlim == 0:
                    nstlim = int(s[9:])  # Number of timesteps
    
    return istep1, ntpr, dt, nstlim


def parse_lists(from_rtr=False): 
    # Used for ABFE simulations, not important for RBFE
    
    # Initialize empty lists to store reference values and k values
    ref_list = []
    k_list = []
    
    # Determine the file path based on the from_rtr flag
    if from_rtr:
        file = 'k.RST'
    else:
        file = '../k.RST'
    
    # Open the specified file for reading
    with open(file, 'r') as f:
        # Read each line in the file
        for line in f:
            # Split the line by ", " and iterate through the segments
            for s in line.split(", "):
                # If the segment contains "r2", extract and store the reference value
                if "r2" in s:
                    ref_list.append(float(s[3:]))
                # If the segment contains "rk2", extract and store the k value
                elif "rk2" in s:
                    k_list.append(float(s[4:]))
    
    # Return the lists of reference values and k values
    return ref_list, k_list

def calculate_acf_manual(data, max_lag): #calculates the autocorrelation function (ACF) of a time series data up to a specified maximum lag
    acf = np.correlate(data - np.mean(data), data - np.mean(data), mode='full') / np.var(data) / len(data)
    return acf[len(acf)//2:len(acf)//2 + max_lag] # an array of autocorrelation values from lag 0 up to max_lag,  how the values of a time series are related to their own past values.

def integrated_autocorrelation_time_manual(acf):
    tau_int = 0.5 + np.sum(acf)
    return tau_int

def estimate_neff_manual(acf):
    tau_int = integrated_autocorrelation_time_manual(acf)
    return len(acf) / (1 + 2 * tau_int)

def standard_error(data):
    return np.std(data) / np.sqrt(len(data)) #finds the standard error for block size 

def block_averaging(data, block_size):
    # Calculate the number of full blocks that can be created from the data with the given block size
    n_blocks = len(data) // block_size
    if n_blocks == 0:
        return data  # If block size is too large (i.e., fewer than one full block), return the original data
    
    # Compute the mean of each block and store in an array
    block_averaged_data = np.array([np.mean(data[i * block_size:(i + 1) * block_size]) for i in range(n_blocks)])
    return block_averaged_data  # Return the block-averaged data

def calculate_tau_int_block(data, block_size):
    # Perform block averaging on the data
    block_averaged_data = block_averaging(data, block_size)
    
    # Calculate the standard error of the original data
    sem_original = standard_error(data)
    
    # Calculate the standard error of the block-averaged data
    sem_blocked = standard_error(block_averaged_data)
    
    if sem_blocked == 0:
        return 1  # Default to 1 if sem_blocked is zero to avoid division by zero
    
    # Calculate the ratio of the squared standard errors multiplied by the number of data points
    ratio_squared_n = (sem_original / sem_blocked) ** 2 * len(data)
    
    # Calculate the integrated autocorrelation time using the ratio
    tau_int_block = math.ceil(len(data) / ratio_squared_n)
    return tau_int_block  # Return the integrated autocorrelation time

def calculate_optimal_block_size(data):
    # Estimate the initial block size using twice the integrated autocorrelation time from pymbar
    tau_int = integrated_autocorrelation_time_pymbar(data)
    block_size = int(2 * tau_int)
    
    while block_size < len(data) // 2:
        # Perform block averaging with the current block size
        block_averaged_data = block_averaging(data, block_size)
        
        # Calculate the standard error of the block-averaged data
        sem_blocked = standard_error(block_averaged_data)
        
        # Calculate the next block size by doubling the current block size
        next_block_size = block_size * 2
        
        # Perform block averaging with the next block size
        next_block_averaged_data = block_averaging(data, next_block_size)
        
        # Calculate the standard error of the next block-averaged data
        next_sem_blocked = standard_error(next_block_averaged_data)
        
        # Check if the change in standard error between the current and next block size is less than 1%
        if np.abs(next_sem_blocked - sem_blocked) < 0.01 * sem_blocked:
            break  # If true, break the loop as the standard error has stabilized
        
        # Update the block size to the next block size for the next iteration
        block_size = next_block_size
    
    return block_size  # Return the optimal block size


def integrated_autocorrelation_time_pymbar(data):
    tau_int = pymbar_timeseries.integrated_autocorrelation_time(data, fast=False, mintime=3)
    return tau_int #regular pymbr 

def average_tau(tau_manual, tau_pymbar):
    return (tau_manual + tau_pymbar) / 2 #average tau between pymbar and manual as a fourth method 

def calculate_errors(data, true_tau_int=None, method="pymbar", max_lag=100): #calculating the errors for each method
    acf_manual = calculate_acf_manual(data, max_lag)
    tau_int_manual = integrated_autocorrelation_time_manual(acf_manual)
    tau_int_pymbar = integrated_autocorrelation_time_pymbar(data)
    tau_int_avg = average_tau(tau_int_manual, tau_int_pymbar)
    
    if true_tau_int is None:
        block_size = calculate_optimal_block_size(data)
    else:
        block_size = int(true_tau_int)
        
    tau_int_block = calculate_tau_int_block(data, block_size)

    #mean absolute erorrs 
    
    errors = {
        "block_averaging": {"MAE_g": np.mean(np.abs(tau_int_block - true_tau_int))} if true_tau_int else None,
        "manual": {"MAE_g": np.mean(np.abs(tau_int_manual - true_tau_int))} if true_tau_int else None,
        "pymbar": {"MAE_g": np.mean(np.abs(tau_int_pymbar - true_tau_int))} if true_tau_int else None,
        "average": {"MAE_g": np.mean(np.abs(tau_int_avg - true_tau_int))} if true_tau_int else None
    }

    if method == "manual": #all the tau_int, acf 
        tau_int = tau_int_manual
    elif method == "block_averaging":
        tau_int = tau_int_block
    elif method == "average":
        tau_int = tau_int_avg
    else:
        tau_int = tau_int_pymbar

    return tau_int_manual, tau_int_block, tau_int_pymbar, tau_int_avg, errors

def analyze(lam, decorrelate=False, method="pymbar"):
     if 'la' in lam:
        lam = lam.split('-')[1]
    datalist = glob.glob('./la-' + lam + '/prod/*.out*')
    if not datalist:
        raise ValueError("No data files found matching the pattern './la-{}'/prod/*.out*".format(lam))
    datalist.sort()
    dHdl0 = [extract_dHdl(i, temp) for i in datalist]
    if not dHdl0:
        raise ValueError("No dHdl data extracted from the files.")
    if len(dHdl0) > 1:
        dHdl = np.array(dHdl0[0]['dHdl'])
        for i in range(len(dHdl0[1:])):
            dHdl = np.concatenate((dHdl, np.array(dHdl0[i + 1]['dHdl'])))
    else:
        dHdl = np.array(dHdl0[0]['dHdl'])
    auto_list = pymbar_timeseries.detect_equilibration(dHdl)
    dHdl_eq = dHdl[auto_list[0]:]
    if decorrelate:
        # Use the specified method to calculate the autocorrelation time
        if method == "manual":
        acf = calculate_acf_manual(dHdl_ssmp, max_lag=100)
        tau_int = integrated_autocorrelation_time_manual(acf)
        dHdl_ssmp = subsample_data(dHdl_ssmp, tau_int) #This function subsamples the data based on the given autocorrelation time. It takes every tau_int-th element from the data
        elif method == "block_averaging":
            block_size = calculate_optimal_block_size(dHdl_ssmp)
            tau_int = calculate_tau_int_block(dHdl_ssmp, block_size)
            dHdl_ssmp = subsample_data(dHdl_ssmp, tau_int) #calls the subsample function for the indices 
        elif method == "average":
            acf = calculate_acf_manual(dHdl_ssmp, max_lag=100)
            tau_int_manual = integrated_autocorrelation_time_manual(acf)
            tau_int_pymbar = integrated_autocorrelation_time_pymbar(dHdl_ssmp)
            tau_int = average_tau(tau_int_manual, tau_int_pymbar)
            dHdl_ssmp = subsample_data(dHdl_ssmp, tau_int) #calls the subsample method for the indices 
        else:  # default to pymbar   
            dHdl_ssmp_indices = pymbar_timeseries.subsample_correlated_data(dHdl_eq, conservative=True) #uses pymbar to get split indices
            dHdl_ssmp = dHdl_eq[dHdl_ssmp_indices]
    else:
        dHdl_ssmp = dHdl_eq

 
    
    return dHdl_ssmp, tau_int

def subsample_data(data, tau_int):#takes it as an np array and autocorrelation time and subsamples based off of that and the autocorrelation time should be rounded up
    subsample_indices = np.arange(0, len(data), int(np.ceil(tau_int))) ## Generate indices for subsampling the data, starting at 0 and taking every ceil(tau_int)-th element

    return data[subsample_indices]

def check_convergence(sample, cutoff, n_bins):
    # Calculate the range of the sample data
    print(n_bins)
    s_range = np.max(sample) - np.min(sample)
    
    # Generate quantile bins
    qs = [np.min(sample) + (i + 1) / (n_bins + 1) * s_range for i in range(n_bins)]
    
    # Split the sample data into two halves
    data_1 = sample[:len(sample) // 2]
    data_2 = sample[len(sample) // 2:]
    
    # Initialize bins for data_1 and data_2
    data_1_bins = []
    data_2_bins = []
    
    # Populate the bins based on quantiles
    for j in range(len(qs) - 1):
        num_1 = num_2 = 0
        if j == 0:
            for k in data_1:
                if k < qs[0]:
                    num_1 += 1
            for k in data_2:
                if k < qs[0]:
                    num_2 += 1
            data_1_bins.append(num_1 / len(data_1))
            data_2_bins.append(num_2 / len(data_2))
        num_1 = num_2 = 0
        for k in data_1:
            if qs[j] <= k < qs[j + 1]:
                num_1 += 1
        for k in data_2:
            if qs[j] <= k < qs[j + 1]:
                num_2 += 1
        data_1_bins.append(num_1 / len(data_1))
        data_2_bins.append(num_2 / len(data_2))
        
    # Handle the last bin separately
    num_1 = num_2 = 0
    for k in data_1:
        if k >= qs[-1]:
            num_1 += 1
    for k in data_2:
        if k >= qs[-1]:
            num_2 += 1
    data_1_bins.append(num_1 / len(data_1))
    data_2_bins.append(num_2 / len(data_2))
    
    # Compute Jensen-Shannon distance between the two distributions
    js_distance = js(data_1_bins, data_2_bins)
    
    # Check if the JS distance is below the cutoff
    converged = bool(js_distance <= cutoff)
    return converged, js_distance
