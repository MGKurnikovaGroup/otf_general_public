#Provides methods for the simulation of lambda windows
#Selected from main steps
#Assumes starting from molecule directory

import os
import shutil
import convergence_test as ct
import subprocess
import shlex
import glob
import math

def update_input(lam, loc, dest, prod=False, nstlim=0):
    #moves input file from dest to loc with
    #updated lambda value lam
    lam=process_lam(lam)
    with open(loc, 'r') as file:
        data = file.read()
        if prod:
            data = data.replace('nstlim = z', 'nstlim = '+ str(int(math.floor(nstlim/0.000002))))
        data = data.replace('clambda = x', 'clambda = '+ lam)
    file.close()
    with open(dest, 'w') as file:
        file.write(data)

def update_input_rtr(lam, loc, dest, counter, nstlim):
    #moves input file from dest to loc with
    #updated lambda value lam
    lam=process_lam(lam)
    with open(loc, 'r') as file:
        data = file.read()
        data = data.replace('nstlim = z', 'nstlim = '+ str(int(math.floor(nstlim/0.000002))))
        if float(lam) == 1:
           data = data.replace('DISANG=../y', 'DISANG=../k.RST')
           data = data.replace('DUMPAVE = x', 'DUMPAVE = rstr_1.0'+str(counter))
        else:
            data = data.replace('DISANG=../y', 'DISANG=../k-la-' + lam +'.RST')
            data = data.replace('DUMPAVE = x', 'DUMPAVE = rstr_'+lam+str(counter))
    file.close()
    with open(dest, 'w') as file:
        file.write(data)

def gen_k(lam):
    kfile = 'k.RST'
    k_list = []
    lambdas=process_lam(lam)
    f = open(kfile)
    cfile = open("rtr/k-la-"+lambdas+".RST", "w")
    for line in f:
        for s in line.split(", "):
            if "rk2" in s:
                new_k = str(float(s[4:])*float(lambdas))
                line = line.replace("rk2="+s[4:], "rk2="+new_k)
                line = line.replace("rk3="+s[4:], "rk3="+new_k)
        cfile.write(line)
    cfile.close()

def process_lam(lam):
    #this is a helper function for processing the input of update_lam and others
    lam = str(lam)
    if '-' in lam:
        lam=lam.split('-')[1]
    return lam

def dcrg_abfe(lam, directory_path, convergence_cutoff,  initial_time, additional_time, max_time_1, max_time_2):
    #Create Directory Architecture
    lam=process_lam(lam)
    print(lam)
    if not os.path.exists("./dcrg+vdw/la-"+lam):
        os.mkdir("./dcrg+vdw/la-"+lam)
        os.mkdir("./dcrg+vdw/la-"+lam+'/1_min')
        os.mkdir("./dcrg+vdw/la-"+lam+'/2_nvt')
        os.mkdir("./dcrg+vdw/la-"+lam+'/3_npt')
        os.mkdir("./dcrg+vdw/la-"+lam+'/prod')
    
    #Create Input Files
    update_input(lam, directory_path+'/dcrg+vdw/1_min/1min.in', "./dcrg+vdw/la-"+lam+'/1_min/1min.in')
    update_input(lam, directory_path+'/dcrg+vdw/1_min/2min.in', "./dcrg+vdw/la-"+lam+'/1_min/2min.in')
    update_input(lam, directory_path+'/dcrg+vdw/2_nvt/nvt.in', "./dcrg+vdw/la-"+lam+'/2_nvt/nvt.in')
    update_input(lam, directory_path+'/dcrg+vdw/3_npt/1_npt.in', "./dcrg+vdw/la-"+lam+'/3_npt/1_npt.in')
    update_input(lam, directory_path+'/dcrg+vdw/3_npt/2_npt.in', "./dcrg+vdw/la-"+lam+'/3_npt/2_npt.in')
    update_input(lam, directory_path+'/dcrg+vdw/3_npt/3_npt.in', "./dcrg+vdw/la-"+lam+'/3_npt/3_npt.in')
    update_input(lam, directory_path+'/dcrg+vdw/prod/prod.in', "./dcrg+vdw/la-"+lam+'/prod/prod.in', prod=True, nstlim=initial_time)
    
    #Run TI
    #If out file already exists, don't mess with it for now
    #Probably should remove or edit this functionality in the future
    os.chdir('dcrg+vdw')
    if not os.path.exists("./la-"+lam+'/prod/complex_prod_00.out'):
        subprocess.call(shlex.split('./md-lambda.sh la-'+lam+' > la-'+lam+'/std.md.txt')) #Script needs to be updated
    print('h')
    #Analyze data, restart simulation if necessary
    counter = 0
    if len(glob.glob('./la-'+lam+'/prod/*.out')) > 1:
        counter = len(glob.glob('./la-'+lam+'/prod/*.out')) - 1
    dcrg_data = ct.analyze(lam,decorrelate=True)
    while (not ct.check_convergence(dcrg_data, convergence_cutoff)[0] and counter <= math.floor((max_time_1-initial_time)/additional_time)) or len(dcrg_data) <= 50:
        #Currently allows 8 restarts (4ns extra)
        #Requires 50 samples to continue
        #restart_lam.sh first argument: lamdba window
        #2nd argument: Suffix of new .out file
        #3rd: sufficx of restart file to use
        print('Beginning restart '+str(counter+1))
        if not os.path.exists('./la-'+lam+'/prod/restart.in'):
            update_input(lam, directory_path+'/dcrg+vdw/prod/restart.in', './la-'+lam+'/prod/restart.in', prod=True, nstlim=additional_time)
        counter_remainder = counter % 10
        counter_quotient = counter // 10
        if counter_remainder == 9:
            subprocess.call(shlex.split('./restart.sh la-'+lam+' '+str(counter+1) + ' ' + str(counter_quotient)+str(counter_remainder)))
        else:
            subprocess.call(shlex.split('./restart.sh la-'+lam+' '+str(counter_quotient)+str(counter_remainder+1) + ' ' + str(counter_quotient)+str(counter_remainder)))
        counter += 1
        dcrg_data=ct.analyze(lam,decorrelate=True)
        if counter >= math.floor((max_time_2-initial_time)/additional_time):
            break
    os.chdir('..')

def water_abfe(lam, directory_path, convergence_cutoff,initial_time, additional_time, max_time_1, max_time_2):
    #Create Directory Architecture
    lam =process_lam(lam)
    if not os.path.exists("./water-dcrg+vdw/la-"+lam):
        os.mkdir("./water-dcrg+vdw/la-"+lam)
        os.mkdir("./water-dcrg+vdw/la-"+lam+'/1_min')
        os.mkdir("./water-dcrg+vdw/la-"+lam+'/2_nvt')
        os.mkdir("./water-dcrg+vdw/la-"+lam+'/3_npt')
        os.mkdir("./water-dcrg+vdw/la-"+lam+'/prod')

    #Create Input Files
    update_input(lam, directory_path+'/water-dcrg+vdw/1_min/1min.in', "./water-dcrg+vdw/la-"+lam+'/1_min/1min.in')
    update_input(lam, directory_path+'/water-dcrg+vdw/1_min/2min.in', "./water-dcrg+vdw/la-"+lam+'/1_min/2min.in')
    update_input(lam, directory_path+'/water-dcrg+vdw/2_nvt/nvt.in', "./water-dcrg+vdw/la-"+lam+'/2_nvt/nvt.in')
    update_input(lam, directory_path+'/water-dcrg+vdw/3_npt/1_npt.in', "./water-dcrg+vdw/la-"+lam+'/3_npt/1_npt.in')
    update_input(lam, directory_path+'/water-dcrg+vdw/3_npt/2_npt.in', "./water-dcrg+vdw/la-"+lam+'/3_npt/2_npt.in')
    update_input(lam, directory_path+'/water-dcrg+vdw/3_npt/3_npt.in', "./water-dcrg+vdw/la-"+lam+'/3_npt/3_npt.in')
    update_input(lam, directory_path+'/water-dcrg+vdw/prod/prod.in', "./water-dcrg+vdw/la-"+lam+'/prod/prod.in', prod=True, nstlim=initial_time)

    #Run TI
    os.chdir('water-dcrg+vdw')
    if not os.path.exists("./la-"+lam+'/prod/ligwat_prod_00.out'):
        subprocess.call(shlex.split('./md-equil.sh la-'+lam+' > la-'+lam+'/std.md.txt')) 
    #Script needs to be updated
    #Analyze data, restart simulation if necessary
    counter = 0
    if len(glob.glob('./la-'+lam+'/prod/*.out')) > 1:
        counter = len(glob.glob('./la-'+lam+'/prod/*.out')) - 1
    wat_data = ct.analyze(lam, decorrelate=True)
    while (not ct.check_convergence(wat_data, convergence_cutoff)[0] and counter <= math.floor((max_time_1-initial_time)/additional_time)) or len(wat_data) <= 50:
        #restart_lam.sh first argument: lamdba window
        #2nd argument: Suffix of new .out file
        #3rd: sufficx of restart file to use
        print('Beginning restart '+str(counter+1))
        if not os.path.exists('./la-'+lam+'/prod/restart.in'):
            update_input(lam, directory_path+'/water-dcrg+vdw/prod/restart.in', './la-'+lam+'/prod/restart.in', prod=True, nstlim=additional_time)
        counter_quotient = counter // 10
        counter_remainder = counter % 10
        if counter_remainder == 9:
            subprocess.call(shlex.split('./restart.sh la-'+lam+' '+str(counter+1) + ' ' + str(counter_quotient)+str(counter_remainder)))
        else:
            subprocess.call(shlex.split('./restart.sh la-'+lam+' '+str(counter_quotient)+str(counter_remainder+1) + ' ' + str(counter_quotient)+str(counter_remainder)))
        counter += 1
        wat_data=ct.analyze(lam, decorrelate=True)
        if counter >= math.floor((max_time_2-initial_time)/additional_time):
            break
    os.chdir('..')

def rtr_abfe(lam, directory_path, convergence_cutoff, initial_time, additional_time, max_time_1, max_time_2):
    #prepare input files
    lam=process_lam(lam)
    print(lam)
    if float(lam) != 1:
        gen_k(lam)
    if not os.path.exists("./rtr/la-"+lam):
        os.mkdir("./rtr/la-"+lam)
        os.mkdir("./rtr/la-"+lam+'/prod')

    update_input_rtr(lam, directory_path+'/rtr/prod/prod.in', './rtr/la-'+lam+'/prod/prod.in', '00', initial_time)
    
    #Run TI
    os.chdir('rtr')

    if not os.path.exists("./la-"+lam+'/prod/complex_prod_00.out'):
        subprocess.call(shlex.split('./md-lambda.sh la-'+lam+' > la-'+lam+'/std.md.txt')) #Script needs to be updated

    #Analyze data, restart simulation if necessary
    counter = 0
    if len(glob.glob('./la-'+lam+'/prod/*.out')) > 1:
        counter = len(glob.glob('./la-'+lam+'/prod/*.out')) - 1
    rtr_data =ct.analyze_rtr(lam, decorrelate=True)
    while (not ct.check_convergence(rtr_data, convergence_cutoff)[0] and counter <= math.floor((max_time_1-initial_time)/additional_time)) or len(rtr_data) <= 50:
        #Currently allows 8 restarts (4ns extra)
        #Requires 50 samples to continue
        #restart_lam.sh first argument: lamdba window
        #2nd argument: Suffix of new .out file
        #3rd: sufficx of restart file to use
        print('Beginning restart '+str(counter+1))
        counter_remainder = counter % 10
        counter_quotient = counter // 10
        if counter_remainder == 9:
            update_input_rtr(lam, directory_path+'/rtr/prod/restart.in', './la-'+lam+'/prod/restart.in',
                    str(counter + 1), nstlim=additional_time)
            subprocess.call(shlex.split('./restart.sh la-'+lam+' '+str(counter+1) + ' ' + str(counter_quotient)+str(counter_remainder)))
        else:
            update_input_rtr(lam, directory_path+'/rtr/prod/restart.in', './la-'+lam+'/prod/restart.in',
                    str(counter_quotient)+str(counter_remainder+1), nstlim=additional_time)
            subprocess.call(shlex.split('./restart.sh la-'+lam+' '+str(counter_quotient)+str(counter_remainder+1) + ' ' + str(counter_quotient)+str(counter_remainder)))
        counter += 1
        rtr_data=ct.analyze_rtr(lam, decorrelate=True)
        if counter >= math.floor((max_time_2-initial_time)/additional_time):
            break
    os.chdir('..')

