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
    
    clear_file(updated_file)
    
    assert('clambda = x' in read_file(input_file))
    update_input('0.1', input_file, updated_file)
    assert('clambda = 0.1' in read_file(updated_file))

    update_input('0.75', input_file_2, updated_file, True)
    assert('clambda = 0.75' in read_file(updated_file))
    assert('nstlim = 0' in read_file(updated_file))

    update_input('0.5', input_file_2, updated_file, True, 1000)
    assert('clambda = 0.5' in read_file(updated_file))
    assert('nstlim = 500000' in read_file(updated_file))

    print('update_input passed')

#update_input_rtr
def update_input_rtr():
    pass

###################Run####################
test_update_input()
update_input_rtr()
