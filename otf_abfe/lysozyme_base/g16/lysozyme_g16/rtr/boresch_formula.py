#!/usr/bin/env python

import math
import sys

#===================================================================================================
# INPUTS
#===================================================================================================

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
    print "there should be 6 reference values but we have "+str(len(ref_list))
    
if len(k_list) != 6: #del ref_list[-1]
    print "there should be 6 force constants but we have "+str(len(ref_list))

print "reference values: ", ref_list
print "force constants: ", k_list


K = 8.314472*0.001  # Gas constant in kJ/mol/K
V = 1.66            # standard volume in nm^3

T      = 300.0      # Temperature in Kelvin
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
        ( (K_r * K_thA * K_thB * K_phiA * K_phiB * K_phiC)**0.5 ) / ( (2.0 * math.pi * K * T)**(3.0) )
    )
)

dG = - K * T * math.log(arg)

print "dG_off = %8.3f kcal/mol" %(dG/4.184)
print "dG_on  = %8.3f kcal/mol" %(-dG/4.184)

outfile = open("total.txt", "w+")
out = outfile.write('RESTR_RMV    '+str(dG/4.184)+'\n')
outfile.close()

