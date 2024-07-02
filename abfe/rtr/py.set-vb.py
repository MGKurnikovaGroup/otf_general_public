#!/usr/bin/env python3

import sys

kfile = sys.argv[1]
k_list = []
lambdas=["0.00", "0.05", "0.10", "0.20", "0.30", "0.50"]
for clambda in lambdas: 
    print("lambda = "+clambda)
    f = open(kfile)
    cfile = open("k-la-"+clambda+".RST", "w")
    for line in f:
        for s in line.split(", "):
            if "rk2" in s:
                new_k = str(float(s[4:])*float(clambda))
                line = line.replace("rk2="+s[4:], "rk2="+new_k)
                line = line.replace("rk3="+s[4:], "rk3="+new_k)
        cfile.write(line)
        #print(line.strip())
    cfile.close()

