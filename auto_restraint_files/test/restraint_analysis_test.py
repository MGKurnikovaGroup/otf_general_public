import sys
import os
import pytest
from pathlib import Path

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from restraint_analysis import *

###################Helpers########################
root_dir = Path(__file__).resolve().parent.parent.parent



def truncate_to_three_decimals(number):
    str_num = str(number)
    if '.' in str_num:
        integer_part, decimal_part = str_num.split('.')
        truncated_decimal_part = decimal_part[:3]  # Take only the first three digits of the fractional part
        return f"{integer_part}.{truncated_decimal_part}"
    else:
        return str_num
#make the above functino generalizable to any number of decimals
def truncate_to_n_decimals(number, n):
    str_num = str(number)
    if '.' in str_num:
        integer_part, decimal_part = str_num.split('.')
        truncated_decimal_part = decimal_part[:n]  # Take only the first three digits of the fractional part
        return f"{integer_part}.{truncated_decimal_part}"
    else:
        return str_num

#considered equal if the first three decimals match
def almost_equal(num1, num2, places=3):
    return truncate_to_n_decimals(num1, places) == truncate_to_n_decimals(num2, places)

def list_almost_equal(list1, list2):
    if len(list1) != len(list2):
        print('asdf')
        return False
    for i in range(len(list1)):
        if not almost_equal(list1[i], list2[i]):
            return False
    return True
###################Tests########################

#find_neighbors()
def test_find_neighbors():
    path = str(root_dir)+'/lysozyme_test_case_restraints/setup/lig_tleap.mol2'
    assert(find_neighbors('C4', path) == ['8', '9', '5'])
    assert(find_neighbors('C1', path) == ['2', '3', '11'])
    assert(find_neighbors('N2', path) == ['17'])
    assert(find_neighbors('H8', path) == ['14'])
    assert(find_neighbors('C8', path) == ['18', '14'])
    print('find_neighbors passed')

#find_hydrogen_neighbor()
def test_find_hydrogen_neighbor():
    #input list should be only neighbor indices
    path = str(root_dir)+'/lysozyme_test_case_restraints/setup/lig_tleap.mol2'

    assert(find_hydrogen_neighbor(['14'],'H8',path) == 'C7')
    assert(find_hydrogen_neighbor(['3'],'H2',path) == 'C2')
    assert(find_hydrogen_neighbor(['12'],'H6',path) == 'N1')

    #non terminal hydrogen
    assert(find_hydrogen_neighbor(['12','1'],'H6', path) == 'H6')
    assert(find_hydrogen_neighbor(['14','1'],'H8', path) == 'H8')
    
    print('find_hydrogen_neighbor passed')

#neighbor_names()
def test_neighbor_names():

    path = str(root_dir)+'/lysozyme_test_case_restraints/setup/lig_tleap.mol2'

    assert(neighbor_names(['8', '9', '5'],path) == ['C5', 'C3'])
    assert(neighbor_names(['2', '3', '11'],path) == ['C2', 'C6'])
    assert(neighbor_names(['17'],path) == ['C8'])
    assert(neighbor_names(['18', '14'],path) == ['N2', 'C7'])
    assert(neighbor_names(['10', '11', '7'],path) == ['C6', 'C4'])
    
    print('neighbor_names passed')

#find_location()
def test_find_location():

    path = str(root_dir)+'/lysozyme_test_case_restraints/complex-repres.pdb'

    assert(find_location('C4',path) == (33.466, 29.156, 39.458))
    assert(find_location('H5',path) == (33.055, 29.805, 37.463))
    assert(find_location('N2',path) == (31.915, 34.831, 36.163))

    #residue not 1, should throw exception
    with pytest.raises(Exception, match="location not found"):
        find_location('N', path)
    with pytest.raises(Exception, match="location not found"):
        find_location('HD3', path)

    print('find_location passed')

#find_residue_loc()
def test_find_residue_loc():

    path = str(root_dir)+'/lysozyme_test_case_restraints/complex-repres.pdb'

    assert(find_residue_loc('GLN_103@OE1', path)==(((39.307, 35.579, 41.28), (38.205, 36.478, 41.686), (37.618, 36.185, 43.064)), ((37.618, 36.185, 43.064), (38.205, 36.478, 41.686), (39.307, 35.579, 41.28))))
    assert(find_residue_loc('GLN_103', path)==(((39.307, 35.579, 41.28), (38.205, 36.478, 41.686), (37.618, 36.185, 43.064)), ((37.618, 36.185, 43.064), (38.205, 36.478, 41.686), (39.307, 35.579, 41.28))))
    assert(find_residue_loc('LEU_119@HD22', path)==(((28.480, 32.989, 35.591), (28.480, 31.690, 36.196), (27.778, 30.632, 35.349)), ((27.778, 30.632, 35.349), (28.480, 31.690, 36.196), (28.480, 32.989, 35.591))))
    assert(find_residue_loc('LEU_119', path)==(((28.480, 32.989, 35.591), (28.480, 31.690, 36.196), (27.778, 30.632, 35.349)), ((27.778, 30.632, 35.349), (28.480, 31.690, 36.196), (28.480, 32.989, 35.591))))

    #using a bad file, should return None if either N, C, CA not found
    assert(find_residue_loc('MET_2', str(root_dir)+'/lysozyme_test_case_restraints/complex-repres_test.pdb')==None)
    print('find_residue_loc passed')

#find_residue_names()
def test_find_residue_names():
    assert(find_residue_names('SER_118')==(('118@N', '118@CA', '118@C'), ('118@C', '118@CA', '118@N')))
    assert(find_residue_names('LEU_122')==(('122@N', '122@CA', '122@C'), ('122@C', '122@CA', '122@N')))
    assert(find_residue_names('VAL_112')==(('112@N', '112@CA', '112@C'), ('112@C', '112@CA', '112@N')))
    print('find_residue_names passed')

#get_distance()
def test_get_distance():
    assert almost_equal(get_distance((1.0, 2.0, 3.0), (4.0, 5.0, 6.0)), 5.196)
    assert almost_equal(get_distance((-1.0, -2.0, -3.0), (-4.0, -5.0, -6.0)), 5.196)
    assert almost_equal(get_distance((1.0, -2.0, 3.0), (-4.0, 5.0, -6.0)), 12.449)
    assert almost_equal(get_distance((0.0, 0.0, 0.0), (0.0, 0.0, 0.0)), 0.0)
    assert almost_equal(get_distance((1000.0, 2000.0, 3000.0), (4000.0, 5000.0, 6000.0)), 5196.152)
    print('get_distance passed')

#get_angle()
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

#valid()
def test_valid():
    assert(valid(((48.082, 36.606, 29.121), (50.558, 35.805, 32.021), (53.561, 35.533, 29.583)),[(33.985, 31.377, 38.696), (33.85, 32.334, 37.722), (33.149, 33.616, 38.163)])==True)
    assert(valid(((0, 0, 0), (1, 0, 0), (0, 1, 0)), [(0, 0, 1), (1, 0, 1), (0, 1, 1)]) == True)
    assert(valid(((1, 0, 0), (0, 1, 0), (0, 0, 1)),[(1, 1, 1), (2, 2, 2), (3, 3, 3)]) == False)
    # assert(valid(((0, 0, 0), (1, 1, 1), (2, 2, 2)),[(3, 3, 3), (4, 4, 4), (5, 5, 5)]) == False)
    # assert(valid(((1.5, 1.5, 1.5),(2.5, 2.5, 2.5),(3.5, 3.5, 3.5)),[(4.5, 4.5, 4.5),(5.5, 5.5, 5.5),(6.5, 6.5, 6.5)]) == True)
    assert(valid(((100000.0, 200000.0, 300000.0), (400000.0, 500000.0, 600000.0), (700000.0, 800000.0, 900000.0)),[(1000000.0, 1100000.0, 1200000.0), (1300000.0, 1400000.0, 1500000.0), (1600000.0, 1700000.0, 1800000.0)]) == True)

def test_calc_angles():


    res_loc1 = [(0,0,0), (1,1,0), (0,1,1)]
    mol_loc1 = [(2,2,2), (2,3,3), (4,4,3)]
    expected1 = (np.pi/3, 0.61548, 2.52611, 1.89254)
    assert(list_almost_equal(calc_angles(res_loc1, mol_loc1), expected1))
    
    res_loc2 = [(47.231,35.897,28.944),(49.753,35.065,31.777),(52.627,35.298,29.108)]
    mol_loc2 = [(33.678,30.991,38.216),(34.125,32.107,37.418),(32.933,33.467,38.775)]
    expected2 = (1.5375, 1.62839, 0.69886, 1.54076)
    assert(list_almost_equal(calc_angles(res_loc2, mol_loc2), expected2))

    print('calc_angles passed')

#angle_deviation()
def test_angle_deviation():
    assert angle_deviation((math.pi/2, math.pi/2, math.pi/2, math.pi/2)) == 0.0
    assert angle_deviation((math.pi/4, math.pi/4, math.pi/4, math.pi/4)) == 0.7853981633974483
    assert angle_deviation((0, 0, 0, 0)) == math.pi/2
    assert almost_equal(angle_deviation((math.pi/2 - 0.1, math.pi/2 + 0.1, math.pi/2 - 0.05, math.pi/2)), 0.0625)
    print('angle_deviation passed')

def test_centroid_search():

    #using shortened version of complex-repres as test file
    path = str(root_dir)+'/lysozyme_test_case_restraints/complex-repres_test2.pdb'
    atoms = centroid_search(path)[0]
    dists_from_centroid = centroid_search(path)[1]
    
    #check that hydrogen is not taken into account
    assert 'H' not in atoms

    #check that the distances to centroid are correct
    #centroid should be (33.937, 32.49125, 39.313)
    assert atoms[0] == 'C1'
    assert almost_equal(dists_from_centroid[0], 1.1926, 2)

    assert atoms[2] == 'N2'
    assert almost_equal(dists_from_centroid[2], 4.41407)

    print('centroid_search passed')

###################Run########################
test_find_neighbors()
test_find_hydrogen_neighbor()
test_neighbor_names()
test_find_location()
test_find_residue_loc()
test_find_residue_names()
test_get_distance()
test_get_angle()
test_angle_deviation()
test_calc_angles()
# test_valid()
test_centroid_search()