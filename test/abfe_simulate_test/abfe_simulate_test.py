import sys
import os
import pytest
from pathlib import Path

# parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# sys.path.insert(0, parent_dir)


root_dir = str(Path(__file__).resolve().parent.parent.parent)

sys.path.insert(0, str(root_dir))

from abfe_simulate import *

###################Helper Functions####################

def clear_file(file):
    with open(file, 'w') as file:
        pass

def read_file(file):
    with open(file, 'r') as file:
        return file.read()
    
###################Tests########################

#update_input
def test_update_input():
    input_file = root_dir + '/test/abfe_simulate_test/1min.in'
    input_file_2 = root_dir + '/test/abfe_simulate_test/prod.in'
    updated_file = root_dir + '/test/abfe_simulate_test/updated_1min.in'
    updated_file_2 = root_dir + '/test/abfe_simulate_test/updated_prod.in'
    clear_file(updated_file)
    
    assert('clambda = x' in read_file(input_file))
    update_input('0.1', input_file, updated_file)
    assert('clambda = 0.1' in read_file(updated_file))

    update_input('0.75', input_file_2, updated_file_2, True)
    assert('clambda = 0.75' in read_file(updated_file_2))
    assert('nstlim = 0' in read_file(updated_file_2))

    update_input('0.5', input_file_2, updated_file_2, True, 1000)
    assert('clambda = 0.5' in read_file(updated_file_2))
    assert('nstlim = 500000' in read_file(updated_file_2))

    print('update_input passed')

#update_input_rtr
def test_update_input_rtr():
    input_file = root_dir + '/test/abfe_simulate_test/rtr_prod.in'
    updated_file = root_dir + '/test/abfe_simulate_test/updated_rtr_prod.in'
    
    clear_file(updated_file)
    
    assert('nstlim = z' in read_file(input_file))
    assert('DISANG=../y' in read_file(input_file))
    assert('DUMPAVE = x' in read_file(input_file))
    
    update_input_rtr('1', input_file, updated_file, 1, 1000)
    updated_content = read_file(updated_file)
    assert('nstlim = 500000' in updated_content)
    assert('DISANG=../k.RST' in updated_content)
    assert('DUMPAVE = rstr_1.01' in updated_content)
    
    update_input_rtr('0.75', input_file, updated_file, 3, 1500)
    updated_content = read_file(updated_file)
    assert('nstlim = 750000' in updated_content)
    assert('DISANG=../k-la-0.75.RST' in updated_content)
    assert('DUMPAVE = rstr_0.753' in updated_content)
    
    print('update_input_rtr passed')

#gen_k
def test_gen_k():

    rst = open('k.RST')
    rst_rk2 = []
    for line in rst:
        for s in line.split(", "):
            if "rk2" in s:
                rst_rk2.append(s)

    gen_k(0.5)

    test1 = open('rtr/k-la-0.5.RST')
    test1_rk2 = []
    for line in test1:
        for s in line.split(", "):
            if "rk2" in s:
                test1_rk2.append(s)

    for i in range(len(rst_rk2)):
        assert(float(test1_rk2[i][4:]) == 0.5 * float(rst_rk2[i][4:]))
    
    gen_k(0.25)
    test2 = open('rtr/k-la-0.25.RST')
    test_rk2 = []
    for line in test2:
        for s in line.split(", "):
            if "rk2" in s:
                test_rk2.append(s)

    for i in range(len(rst_rk2)):
        assert(float(test_rk2[i][4:]) == 0.25 * float(rst_rk2[i][4:]))
    print('gen_k passed')

#process_lam 
def test_process_lam():

    assert process_lam("1.5") == "1.5"
    assert process_lam(1.5) == "1.5"  # Testing with float input
    assert process_lam("prefix-1.5") == "1.5"
    assert process_lam("123-456") == "456"
    print('process_lam passed')

###################Run####################
test_update_input()
test_update_input_rtr()
test_gen_k()
test_process_lam()
