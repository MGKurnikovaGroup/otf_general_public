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

def update_input(lam, loc, dest, in_loc, sssc, prod=False, nstlim=0, add_restr='', frames_per_ns = 0, ctm=['','']):
    #moves input file from dest to loc with
    #updated lambda value lam
    lam=process_lam(lam)
    with open(in_loc, 'r') as file:
        for line in file:
            line=line.strip('\n')
            if 'scmask1' in line:
                scmask1=line.split('=')[1]
            if 'scmask2'in line:
                scmask2=line.split('=')[1]
    with open(loc, 'r') as file:
        data = file.read()
        if prod:
            data = data.replace('nstlim = z', 'nstlim = '+ str(int(math.floor(nstlim/0.000002))))#this assumes dt = .002, not always the case though. A good place for adding functionality
            if frames_per_ns > 0:
                data = data.replace('ntwx = 0', 'ntwx = '+ str(int(math.floor(500000/frames_per_ns))))
        data = data.replace('clambda = x', 'clambda = '+ lam)
        data = data.replace("scmask1 = 'SCM1'", "scmask1 = '"+scmask1+"'")
        data = data.replace("scmask2 = 'SCM2'", "scmask2 = '"+scmask2+"'")
        if ctm[0] != '':
            print(ctm)
            data = data.replace("timask1 = ':L0'", "timask1 = '"+str(ctm[0])+"'")
        if ctm[1] != '':
            data = data.replace("timask2 = ':L1'", "timask2 = '"+str(ctm[1])+"'")
        if sssc == 1:
            data = data.replace("scalpha = 0.2, scbeta = 50.0", "scalpha = 0.5, scbeta = 12.0")
        if sssc == 0:
            data = data.replace("gti_lam_sch = 1, scalpha = 0.2, scbeta = 50.0","scalpha = 0.5, scbeta = 12.0") 
        if add_restr != '':
            data = data.replace("restraintmask='", "restraintmask='"+add_restr+"|")
    file.close()
    with open(dest, 'w') as file:
        file.write(data)

def process_lam(lam):
    #this is a helper function for processing the input of update_lam and others
    lam = str(lam)
    if '-' in lam:
        lam=lam.split('-')[1]
    return lam

def site_rbfe(lam, directory_path, convergence_cutoff, in_loc, initial_time, additional_time, max_time_1, max_time_2, reference_lam = -1, sssc = 2, add_restr='', fpn=0, target_lam=-1, special='site', decorrelate = True, ctm = ['','']):
    #Create Directory Architecture
    lam=process_lam(lam)
    if not reference_lam == -1:
        reference_lam = process_lam(reference_lam)
    print(lam)
    if not os.path.exists("./site/la-"+lam):
        os.mkdir("./site/la-"+lam)
        os.mkdir("./site/la-"+lam+'/1_min')
        os.mkdir("./site/la-"+lam+'/2_nvt')
        os.mkdir("./site/la-"+lam+'/3_npt')
        os.mkdir("./site/la-"+lam+'/prod')
    
    #Create Input Files
    update_input(lam, directory_path+'/site/1_min/1min.in', "./site/la-"+lam+'/1_min/1min.in', in_loc, sssc, add_restr=add_restr, ctm=ctm)
    update_input(lam, directory_path+'/site/1_min/2min.in', "./site/la-"+lam+'/1_min/2min.in', in_loc, sssc, add_restr=add_restr, ctm=ctm)
    update_input(lam, directory_path+'/site/2_nvt/nvt.in', "./site/la-"+lam+'/2_nvt/nvt.in', in_loc, sssc, add_restr=add_restr, ctm=ctm)
    update_input(lam, directory_path+'/site/3_npt/1_npt.in', "./site/la-"+lam+'/3_npt/1_npt.in', in_loc, sssc, add_restr=add_restr, ctm=ctm)
    update_input(lam, directory_path+'/site/3_npt/2_npt.in', "./site/la-"+lam+'/3_npt/2_npt.in', in_loc, sssc, add_restr=add_restr, ctm=ctm)
    update_input(lam, directory_path+'/site/3_npt/3_npt.in', "./site/la-"+lam+'/3_npt/3_npt.in', in_loc, sssc, ctm=ctm)
    update_input(lam, directory_path+'/site/prod/prod.in', "./site/la-"+lam+'/prod/prod.in', in_loc, sssc, prod=True, nstlim = initial_time, frames_per_ns = fpn, ctm = ctm)
    
    #Run TI
    os.chdir('site')
    if not os.path.exists("./la-"+lam+'/prod/complex_prod_00.out'):
        if lam==str(target_lam) and reference_lam != -1 and special=='site':
            print('Special treatment of site la-'+str(target_lam)+' by la-'+str(reference_lam)+'!')
            subprocess.call(shlex.split('./md-lambda_special.sh la-'+str(target_lam)+' la-'+str(reference_lam)+' > la-'+lam+'/std.md.txt'))
        else:
            print('Running nomally site la-'+lam)
            subprocess.call(shlex.split('./md-lambda.sh la-'+lam+' > la-'+lam+'/std.md.txt'))
        
    #Analyze data, restart simulation if necessary
    counter = 0
    if len(glob.glob('./la-'+lam+'/prod/*.out')) > 1: #counts number of output files
        counter = len(glob.glob('./la-'+lam+'/prod/*.out')) - 1
    site_data = ct.analyze(lam, decorrelate=decorrelate)
    while (not ct.check_convergence(site_data, convergence_cutoff)[0] and counter < math.floor((max_time_1-initial_time)/additional_time)) or len(site_data) <= 50: #Checks convergence criteria
        print('Beginning restart '+str(counter+1))
        if not os.path.exists('./la-'+lam+'/prod/restart.in'):
            update_input(lam, directory_path+'/site/prod/restart.in', './la-'+lam+'/prod/restart.in', in_loc, sssc, prod=True, nstlim=additional_time, frames_per_ns = fpn, ctm=ctm)
        counter_remainder = counter % 10
        counter_quotient = counter // 10
        if counter_remainder == 9:
            subprocess.call(shlex.split('./restart.sh la-'+lam+' '+str(counter+1) + ' ' + str(counter_quotient)+str(counter_remainder)))
        else:
            subprocess.call(shlex.split('./restart.sh la-'+lam+' '+str(counter_quotient)+str(counter_remainder+1) + ' ' + str(counter_quotient)+str(counter_remainder)))
        if counter >= math.floor((max_time_2-initial_time)/additional_time):
            break
        counter += 1
        site_data=ct.analyze(lam, decorrelate = decorrelate)
    os.chdir('..')

def water_rbfe(lam, directory_path, convergence_cutoff, in_loc, initial_time, additional_time, max_time_1, max_time_2, reference_lam = -1, sssc=2, fpn=0, target_lam=-1, special='water', decorrelate = True, ctmw=['','']):
    #Create Directory Architecture
    lam =process_lam(lam)
    if not reference_lam == -1:
        reference_lam = process_lam(reference_lam)
    if not os.path.exists("./water/la-"+lam):
        os.mkdir("./water/la-"+lam)
        os.mkdir("./water/la-"+lam+'/1_min')
        os.mkdir("./water/la-"+lam+'/2_nvt')
        os.mkdir("./water/la-"+lam+'/3_npt')
        os.mkdir("./water/la-"+lam+'/prod')

    #Create Input Files
    update_input(lam, directory_path+'/water/1_min/1min.in', "./water/la-"+lam+'/1_min/1min.in', in_loc, sssc, ctm=ctmw)
    update_input(lam, directory_path+'/water/1_min/2min.in', "./water/la-"+lam+'/1_min/2min.in', in_loc, sssc, ctm=ctmw)
    update_input(lam, directory_path+'/water/2_nvt/nvt.in', "./water/la-"+lam+'/2_nvt/nvt.in', in_loc, sssc, ctm=ctmw)
    update_input(lam, directory_path+'/water/3_npt/1_npt.in', "./water/la-"+lam+'/3_npt/1_npt.in', in_loc, sssc, ctm=ctmw)
    update_input(lam, directory_path+'/water/3_npt/2_npt.in', "./water/la-"+lam+'/3_npt/2_npt.in', in_loc, sssc, ctm=ctmw)
    update_input(lam, directory_path+'/water/3_npt/3_npt.in', "./water/la-"+lam+'/3_npt/3_npt.in', in_loc, sssc, ctm=ctmw)
    update_input(lam, directory_path+'/water/prod/prod.in', "./water/la-"+lam+'/prod/prod.in', in_loc, sssc, prod=True, nstlim=initial_time, frames_per_ns=fpn, ctm=ctmw)

    #Run TI
    os.chdir('water')
    if not os.path.exists("./la-"+lam+'/prod/ligwat_prod_00.out'):
        if lam == str(target_lam) and reference_lam != -1 and special=='water':
            print('Special treatment of water la-'+str(target_lam)+' by la-'+str(reference_lam)+'!')
            subprocess.call(shlex.split('./md-equil_special.sh la-'+str(target_lam)+' la-'+str(reference_lam)+' > la-'+lam+'/std.md.txt'))
        else:
            print('Running nomally water la-'+lam)
            subprocess.call(shlex.split('./md-equil.sh la-'+lam+' > la-'+lam+'/std.md.txt'))
    #Analyze data, restart simulation if necessary
    counter = 0
    if len(glob.glob('./la-'+lam+'/prod/*.out')) > 1:
        counter = len(glob.glob('./la-'+lam+'/prod/*.out')) - 1
    wat_data = ct.analyze(lam, decorrelate = decorrelate)
    while (not ct.check_convergence(wat_data, convergence_cutoff)[0] and counter <= math.floor((max_time_1-initial_time)/additional_time)) or len(wat_data) <= 50:
        #restart_lam.sh first argument: lamdba window
        #2nd argument: Suffix of new .out file
        #3rd: sufficx of restart file to use
        print('Beginning ' +str(lam)+' restart '+str(counter+1))
        if not os.path.exists('./la-'+lam+'/prod/restart.in'):
            update_input(lam, directory_path+'/water/prod/restart.in', './la-'+lam+'/prod/restart.in', in_loc,sssc, prod=True, nstlim=additional_time, frames_per_ns = fpn, ctm=ctmw)
        counter_quotient = counter // 10
        counter_remainder = counter % 10
        if counter_remainder == 9:
            subprocess.call(shlex.split('./restart.sh la-'+lam+' '+str(counter+1) + ' ' + str(counter_quotient)+str(counter_remainder)))
        else:
            subprocess.call(shlex.split('./restart.sh la-'+lam+' '+str(counter_quotient)+str(counter_remainder+1) + ' ' + str(counter_quotient)+str(counter_remainder)))
        if counter >= math.floor((max_time_2-initial_time)/additional_time):
            break
        counter += 1
        wat_data=ct.analyze(lam, decorrelate = decorrelate)
    os.chdir('..')

