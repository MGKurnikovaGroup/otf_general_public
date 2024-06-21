import sys
import os
import pytest
from pathlib import Path

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from abfe_simulate import *

root_dir = str(Path(__file__).resolve().parent.parent)

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
    input_file = root_dir + '/test/abfe_simulate_test_files/1min.in'
    input_file_2 = root_dir + '/test/abfe_simulate_test_files/prod.in'
    updated_file = root_dir + '/test/abfe_simulate_test_files/updated_1min.in'
    updated_file_2 = root_dir + '/test/abfe_simulate_test_files/updated_prod.in'
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
    input_file = root_dir + '/test/abfe_simulate_test_files/rtr_prod.in'
    updated_file = root_dir + '/test/abfe_simulate_test_files/updated_rtr_prod.in'
    
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

def test_gen_k():
    #add write location as a generalizable parameter to gen_k for testing purposes
    pass

###################Run####################
test_update_input()
test_update_input_rtr()
