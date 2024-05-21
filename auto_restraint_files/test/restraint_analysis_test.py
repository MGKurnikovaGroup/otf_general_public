import sys
import os
import pytest
from pathlib import Path

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from restraint_analysis import *

###################Helpers########################
root_dir = Path(__file__).resolve().parent.parent.parent

def almost_equal(a, b, places=3):
    return round(abs(a - b), places) == 0

###################Tests########################

#find_neighbors
def test_find_neighbors():
    assert(find_neighbors('C4',str(root_dir)+'/lysozyme_test_case_restraints/setup/lig_tleap.mol2') == ['8', '9', '5'])
    assert(find_neighbors('C1',str(root_dir)+'/lysozyme_test_case_restraints/setup/lig_tleap.mol2') == ['2', '3', '11'])
    assert(find_neighbors('N2',str(root_dir)+'/lysozyme_test_case_restraints/setup/lig_tleap.mol2') == ['17'])
    assert(find_neighbors('H8',str(root_dir)+'/lysozyme_test_case_restraints/setup/lig_tleap.mol2') == ['14'])
    assert(find_neighbors('C8',str(root_dir)+'/lysozyme_test_case_restraints/setup/lig_tleap.mol2') == ['18', '14'])
    print('find_neighbors passed')

#check_terminal
def test_check_terminal():
    assert(check_terminal(['8', '9', '5'],'C4',str(root_dir)+'/lysozyme_test_case_restraints/setup/lig_tleap.mol2')=='C4')
    assert(check_terminal(['12', '14', '17', '18'],'N2',str(root_dir)+'/lysozyme_test_case_restraints/setup/lig_tleap.mol2')=='N2')
    assert(check_terminal(['16','14','15','17'],'H8',str(root_dir)+'/lysozyme_test_case_restraints/setup/lig_tleap.mol2')=='C7')
    assert(check_terminal(['13','12','14'],'H6',str(root_dir)+'/lysozyme_test_case_restraints/setup/lig_tleap.mol2')=='N1')
    assert(check_terminal(['18','14'],'C8',str(root_dir)+'/lysozyme_test_case_restraints/setup/lig_tleap.mol2')=='C8')
    print('check_terminal passed')
#get_angle
def test_get_angle():
    assert(almost_equal(get_angle(1,1,1), 1.047))
    assert(almost_equal(get_angle(1,1,1), 1.047))
    assert(almost_equal(get_angle(3,4,5), 0.927))
    assert(almost_equal(get_angle(0.5,0.7,0.3), 2.094))
    with pytest.raises(ValueError, match="Invalid triangle sides"):
        get_angle(1, 2, 3)
    with pytest.raises(ValueError, match="Side lengths cannot be zero"):
        get_angle(0, 3, 4)
    print('get_angle passed')
    

###################Run########################
test_find_neighbors()
test_check_terminal()
test_get_angle()
