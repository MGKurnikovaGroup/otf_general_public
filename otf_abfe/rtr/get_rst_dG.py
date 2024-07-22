#!/usr/bin/env python

#from __future__ import print_function
import sys
#import statistics as stat
import re
import numpy as np
from scipy import interpolate
from scipy.integrate import simps
from numpy import trapz
#import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline

## 1. GET DV/DL VALUES

# get force constants and reference values
ref_list = []
k_list = []
with open(sys.argv[1]) as f:
    for line in f:
        for s in line.split(", "):
            if "r2" in s:
                ref_list.append(float(s[3:]))
            elif "rk2" in s:
                k_list.append(float(s[4:]))
                
if len(ref_list) != 6: #del ref_list[-1]
    print("there should be 6 reference values but we have "+str(len(ref_list)))
    
if len(k_list) != 6: #del ref_list[-1]
    print("there should be 6 force constants but we have "+str(len(ref_list)))

print("reference values: ", ref_list)
print("force constants: ", k_list)

for n in range (1,6):
    k_list[n] = k_list[n]/(57.2958**2)
print("converted force constants: ", k_list)

# equilibration period
n = 50

# this function calculates dvdl for the current frame
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

# import data
# llambda = [0.00922, 0.04794, 0.11505, 0.20634, 0.31608, 0.43738, 0.56262, 0.68392, 0.79366, 0.88495, 0.95206, 0.99078]
files = sys.argv[2:]
print(files)
print('filename    la    dvdl, kcal/mol')
out_file = open('lambdas.dvdl', 'w+')
check_file = open('check_dih.txt', 'w')

x=[] # lambda values
y=[] # dv/dl values
for filename in files:
    cfile = open(filename, 'r') # current file
    lines = cfile.readlines()
    dvdl_file = open('dvdl.'+filename,'w')
    del lines[:n] # remove equilibration period
    dvdl_sum = 0

    for line in lines:
        cdof = line.split() # current degrees of freedom
        del cdof[0]
        if len(cdof) > 6: del cdof[-1]
        cdof, check_dih = check_dihedrals(cdof, ref_list)
        dvdl = calc_dvdl(cdof, ref_list, k_list)
        print(dvdl, end="", file=dvdl_file)
        print(check_dih, end="", file=check_file)

        dvdl_sum = dvdl_sum + dvdl

    dvdl_file.close()
    dvdl_ave = dvdl_sum/len(lines)
    la = float(re.findall('\d+\.\d+', filename )[0])
    
    x.append(la)
    y.append(dvdl_ave)
    
    out = out_file.write(str(la)+' '+str(dvdl_ave)+'\n')
    print(filename, ' ', la, ' ', dvdl_ave, ' ', len(lines))
    #print >> out_file, filename, ' ', dvdl_ave

#out_file.close()
check_file.close()

## 2. INTEGRATION
# import

#data = np.loadtxt(out_file)
#x = data[:,0]
#y = data[:,1]
print('x: ',x)
print('y: ',y)
print('Integrals from x = ',x[0],' to x = ',x[-1])
out_file.close()

outfile=open('total.txt', "w+")
#yint = integ(x, tck)
# using Trapezoidal rule:
integral = trapz(y,x)
print('Trapezoidal rule: ',integral)
out = outfile.write('RESTR_ADD    '+str(integral)+'\n')

# using Simpson's rule:
#integral = simps(y,x)
#print "Simpsons rule: ",integral

# using k-spline
#ks = 2 # degree of smoothing spline
#spl = UnivariateSpline(x, y, s=0.1, k=ks)
#integral = spl.integral(x[0], x[-1])
#print "Spline k=",ks," : ",integral

outfile.close()

#plt.plot(x, y, marker='o', ms=5)
#plt.xticks(np.arange(0.0, 1.1, 0.1))
#plt.xlabel('lambda')
#plt.ylabel('dV/dl')
##xs = np.linspace(0, 1, 1000)
##plt.plot(xs, spl(xs), 'g', lw=3)
##plt.show()
#plt.savefig("rtr_dvdl.png")

# integration of spline
def integ(x, tck, constant=0):
    x = np.atleast_1d(x)
    out = np.zeros(x.shape, dtype=x.dtype)
    for n in range(len(out)):
        out[n] = interpolate.splint(0, x[n], tck)
    out += constant
    return out
