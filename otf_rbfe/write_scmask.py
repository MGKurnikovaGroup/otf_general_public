#!/usr/bin/env python3
# coding: utf-8

import math
import sys

lig1=[]
lig2=[]
scmask_temp1=[]
scmask_temp2=[]

# input files
ifilename='water/ligwat.pdb'
scfilename = 'scmask.txt'

###############
ifile = open(ifilename, "r")

# create a list for each ligand
for l in ifile:
    if "L0" in l:
        lig1.append(l.strip().split())
    elif "L1" in l:
        lig2.append(l.strip().split())

#print(lig1[0])
#print(lig2[2][7])
#min(len(lig1), len(lig2))

def abs_diff_xyz(atom0, atom1):
    abs_diff_x = abs(float(atom0[5])-float(atom1[5])) 
    abs_diff_y = abs(float(atom0[6])-float(atom1[6])) 
    abs_diff_z = abs(float(atom0[7])-float(atom1[7]))
    return math.sqrt(abs_diff_x**2+abs_diff_y**2+abs_diff_z**2)

def write_mask(filename, scmask1, scmask2):
    # Safely read the input filename using 'with'
    with open(filename, 'w') as f:
        f.write('scmask1='+scmask1+'\n')
        f.write('scmask2='+scmask2)
    f.close()
#abs_diff_xyz(lig1[10],lig2[10])

# iterate over atoms
for i in range(min(len(lig1), len(lig2))):
    #print(abs_diff_xyz(lig1[i],lig2[i]))
    # add atoms which differ in XYZ to scmask_temp
    if (lig1[i][0] == 'TER') or (lig2[i][0] == 'TER'):
        if (lig1[i][0] == 'TER') and (lig2[i][0] != 'TER'):
            scmask_temp2.append(lig2[i][2])
        elif (lig1[i][0] != 'TER') and (lig2[i][0] == 'TER'):
            scmask_temp1.append(lig1[i][2])
        continue
    if abs_diff_xyz(lig1[i],lig2[i]) >= 0.1:
        scmask_temp1.append(lig1[i][2])
        scmask_temp2.append(lig2[i][2])
    
    #add atoms to scmask_temp if one is hydrogen and another is heavy
    elif "H" in lig1[i][2] and "H" not in lig2[i][2]:
        scmask_temp1.append(lig1[i][2])
        scmask_temp2.append(lig2[i][2])
    elif "H" in lig2[i][2] and "H" not in lig1[i][2]:
        scmask_temp1.append(lig1[i][2])
        scmask_temp2.append(lig2[i][2])
    

# add last atoms of the largest ligand to scmask
if len(lig1)-len(lig2) < 0:
    for i in range(len(lig1),len(lig2)):
        if not (lig2[i][0] == 'TER'):
            scmask_temp2.append(lig2[i][2])
               
if len(lig1)-len(lig2) > 0:
    for i in range(len(lig2),len(lig1)):
        if not (lig1[i][0] == 'TER'):
            scmask_temp1.append(lig1[i][2])    

#print(scmask_temp1, "\n", scmask_temp2)

# remove duplicates from lists  
scmask_clean1 = []
scmask_clean2 = []

for x in scmask_temp1: 
    if x not in scmask_clean1: 
        scmask_clean1.append(x)

for y in scmask_temp2: 
    if y not in scmask_clean2: 
        scmask_clean2.append(y)

#print(scmask_clean1, "\n", scmask_clean2)
#print(scmask_clean1)
remove_mask1=[]
remove_mask2=[]
for i in range(len(scmask_clean1)):
    for j in lig1:
        if j[2] == scmask_clean1[i]:
            coord1=(float(j[5]),float(j[6]),float(j[7]))
            break
    for j in range(len(scmask_clean2)):
        for k in lig2:
            if k[2] == scmask_clean2[j]:
                #print(k)
                coord2=(float(k[5]),float(k[6]),float(k[7]))
                break
        if math.sqrt((coord1[0]-coord2[0])**2+(coord1[1]-coord2[1])**2+(coord1[2]-coord1[2])**2)==0 and (('H' not in scmask_clean1[i] and 'H' not in scmask_clean2[j]) or ('H' in scmask_clean1[i] and 'H' in scmask_clean2[j])):
            print(scmask_clean1[i], scmask_clean2[j])
            remove_mask1.append(i)
            remove_mask2.append(j)
            break
scmask_true1=[]
scmask_true2=[]
for i in range(len(scmask_clean1)):
    if i not in remove_mask1:
        scmask_true1.append(scmask_clean1[i])
for i in range(len(scmask_clean2)):
    if i not in remove_mask2:
        scmask_true2.append(scmask_clean2[i])
#generate final AMBER masks
if len(scmask_true1)>0:
    scmask1 = ":1@"+",".join(scmask_true1)
else:
    scmask1 = ''
    
if len(scmask_true2)>0:
    scmask2 = ":2@"+",".join(scmask_true2)
else:
    scmask2 = ''

print("scmask1=",scmask1)
print("scmask2=",scmask2)
# write scmask in script
write_mask(scfilename, scmask1, scmask2)

