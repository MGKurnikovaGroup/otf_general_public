import sys
import pandas as pd
import numpy as np


for item in sys.argv[1:]:
    with open(item+'/vbla.txt','r') as vbla:
        for line in vbla:
            line = line.split(' ')
            vbla_list = line
    vbla.close()
    with open(item+'/complex-repres.pdb', 'r') as cpx:
        vbla_number = [0,0,0]
        for line in cpx:
            if 0 not in vbla_number:
                break
            line = line.split(' ')
            while '' in line:
                line.remove('')
            if vbla_list[0] == line[2]:
                vbla_number[0]=int(line[1])
            elif vbla_list[1] == line[2]:
                vbla_number[1]=int(line[1])
            elif vbla_list[2] == line[2]:
                vbla_number[2]=int(line[1])
    cpx.close()
    rmsf = pd.read_csv(item+'/md-complex/rmsf', engine='python', sep=r'\s{2,}', names=['Atom', 'rmsf'])
    rmsf_r = rmsf.reset_index()
    rmsf_c = rmsf_r.loc[vbla_number]
    rmsf_c.to_csv(item+'/rmsf_analysis.dat', sep = '\t')
