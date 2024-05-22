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

#find_hydrogen_neighbor
def test_find_hydrogen_neighbor():
    #input list should be only neighbor indices
    assert(find_hydrogen_neighbor(['14'],'H8',str(root_dir)+'/lysozyme_test_case_restraints/setup/lig_tleap.mol2') == 'C7')
    assert(find_hydrogen_neighbor(['3'],'H2',str(root_dir)+'/lysozyme_test_case_restraints/setup/lig_tleap.mol2') == 'C2')
    assert(find_hydrogen_neighbor(['12'],'H6',str(root_dir)+'/lysozyme_test_case_restraints/setup/lig_tleap.mol2') == 'N1')

    #non terminal hydrogen
    assert(find_hydrogen_neighbor(['12','1'],'H6',str(root_dir)+'/lysozyme_test_case_restraints/setup/lig_tleap.mol2') == 'H6')
    assert(find_hydrogen_neighbor(['14','1'],'H8',str(root_dir)+'/lysozyme_test_case_restraints/setup/lig_tleap.mol2') == 'H8')
    print('find_hydrogen_neighbor passed')

#neighbor_names
def test_neighbor_names():
    assert(neighbor_names(['8', '9', '5'],str(root_dir)+'/lysozyme_test_case_restraints/setup/lig_tleap.mol2') == ['C5', 'C3'])
    assert(neighbor_names(['2', '3', '11'],str(root_dir)+'/lysozyme_test_case_restraints/setup/lig_tleap.mol2') == ['C2', 'C6'])
    assert(neighbor_names(['17'],str(root_dir)+'/lysozyme_test_case_restraints/setup/lig_tleap.mol2') == ['C8'])
    assert(neighbor_names(['18', '14'],str(root_dir)+'/lysozyme_test_case_restraints/setup/lig_tleap.mol2') == ['N2', 'C7'])
    assert(neighbor_names(['10', '11', '7'],str(root_dir)+'/lysozyme_test_case_restraints/setup/lig_tleap.mol2') == ['C6', 'C4'])
    print('neighbor_names passed')

#find_location 
def test_find_location():
    assert(find_location('C4',str(root_dir)+'/lysozyme_test_case_restraints/complex-repres.pdb') == (33.466, 29.156, 39.458))
    assert(find_location('H5',str(root_dir)+'/lysozyme_test_case_restraints/complex-repres.pdb') == (33.055, 29.805, 37.463))
    assert(find_location('N2',str(root_dir)+'/lysozyme_test_case_restraints/complex-repres.pdb') == (31.915, 34.831, 36.163))

    #residue not 1, should throw exception
    with pytest.raises(Exception, match="location not found"):
        find_location('N',str(root_dir)+'/lysozyme_test_case_restraints/complex-repres.pdb')
    with pytest.raises(Exception, match="location not found"):
        find_location('HD3',str(root_dir)+'/lysozyme_test_case_restraints/complex-repres.pdb')
    
    print('find_location passed')

#find_residue_loc
def test_find_residue_loc():
    assert(find_residue_loc('GLN_103@OE1',str(root_dir)+'/lysozyme_test_case_restraints/complex-repres.pdb')==(((39.307, 35.579, 41.28), (38.205, 36.478, 41.686), (37.618, 36.185, 43.064)), ((37.618, 36.185, 43.064), (38.205, 36.478, 41.686), (39.307, 35.579, 41.28))))
    assert(find_residue_loc('GLN_103',str(root_dir)+'/lysozyme_test_case_restraints/complex-repres.pdb')==(((39.307, 35.579, 41.28), (38.205, 36.478, 41.686), (37.618, 36.185, 43.064)), ((37.618, 36.185, 43.064), (38.205, 36.478, 41.686), (39.307, 35.579, 41.28))))
    assert(find_residue_loc('LEU_119@HD22',str(root_dir)+'/lysozyme_test_case_restraints/complex-repres.pdb')==(((28.480, 32.989, 35.591), (28.480, 31.690, 36.196), (27.778, 30.632, 35.349)), ((27.778, 30.632, 35.349), (28.480, 31.690, 36.196), (28.480, 32.989, 35.591))))
    assert(find_residue_loc('LEU_119',str(root_dir)+'/lysozyme_test_case_restraints/complex-repres.pdb')==(((28.480, 32.989, 35.591), (28.480, 31.690, 36.196), (27.778, 30.632, 35.349)), ((27.778, 30.632, 35.349), (28.480, 31.690, 36.196), (28.480, 32.989, 35.591))))

    #using a bad file, should return None if either N, C, CA not found
    assert(find_residue_loc('MET_2', str(root_dir)+'/lysozyme_test_case_restraints/complex-repres_test.pdb')==None)
    print('find_residue_loc passed')

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
test_find_hydrogen_neighbor()
test_neighbor_names()
test_find_location()
test_find_residue_loc()
test_get_angle()
