import sys
import pandas as pd
import numpy as np
import math

#########Execution#########
def execute(frac, bb='md-complex/BB.avg.dat', bb2='md-complex/BB2.avg.dat', ligand='setup/lig_tleap.mol2', pdb='complex-repres.pdb'):
    
    #establish global file paths
    global bb_file
    bb_file = bb
    global bb2_file
    bb2_file = bb2
    global ligand_file
    ligand_file = ligand
    global pdb_file
    pdb_file = pdb

    df1 = pd.read_csv(bb_file, engine='python', sep=r'\s{2,}', header=0, names=['Acceptor', 'DonorH', 'Donor', 'Frames', 'Frac', 'AvgDist', 'AvgAng'])
    df2 = pd.read_csv(bb2_file, engine='python', sep=r'\s{2,}', header=0, names=['Acceptor', 'DonorH', 'Donor', 'Frames', 'Frac', 'AvgDist', 'AvgAng'])
    df1_rel=df1[df1['Frac'] >= float(frac)]
    df2_rel=df2[df2['Frac'] >= float(frac)]

    #check for multiple options. Only one is executed.
    if len(df1_rel) + len(df2_rel) > 1:
        exec1(df1_rel, df2_rel, ligand_file, pdb_file)
    elif len(df1_rel)+len(df2_rel) > 0:
        exec2(df1_rel, df2_rel, pdb_file)
    #centroid search
    else:
        exec3(pdb_file)

def exec1(df1_rel, df2_rel, ligand_file, pdb_file):
    ligand=open(ligand_file, 'r')
    start = False
    xs=[]
    ys=[]
    zs=[]
    for line in ligand:
        if '@<TRIPOS>BOND' in line:
            start = False
        if start:
            lines=line.split(' ')
            while '' in lines:
                lines.remove('')
            xs.append(float(lines[2]))
            ys.append(float(lines[3]))
            zs.append(float(lines[4]))
        if '@<TRIPOS>ATOM' in line:
            start = True
    centroid=(sum(xs)/len(xs),sum(ys)/len(ys),sum(zs)/len(zs))
    distances = []
    atoms = []
    residues = []
    ligand.close()
    if len(df1_rel) > 0:
        for i in range(len(df1_rel)):
            item = df1_rel['Donor'][i]
            counter_item=df1_rel['Acceptor'][i].split('@')[0]
            atom = item.split('@')[1]
            ligand=open(ligand_file, 'r')
            for line in ligand:
                if atom in line:
                    lines=line.split(' ')
                    while '' in lines:
                        lines.remove('')
                    distances.append(((centroid[0]-float(lines[2]))**2+
                        (centroid[1]-float(lines[3]))**2 + (centroid[2]-float(lines[3]))**2)**.5)
                    atoms.append(atom)
            residues.append(counter_item)
    if len(df2_rel) > 0:
        for i in range(len(df2_rel)):
            item = df2_rel['Acceptor'][i]
            counter_item = df2_rel['Donor'][i].split('@')[0]
            atom = item.split('@')[1]
            ligand=open(ligand_file, 'r')
            for line in ligand:
                if atom in line:
                    lines=line.split(' ')
                    while '' in lines:
                        lines.remove('')
                    distances.append(((centroid[0]-float(lines[2]))**2+
                        (centroid[1]-float(lines[3]))**2 + (centroid[2]-float(lines[3]))**2)**.5)
                    atoms.append(atom)
            residues.append(counter_item)
    
    for i in range(len(atoms)):
        mol_atom_a = atoms[np.argmin(distances)]
        residue = residues[np.argmin(distances)]
        mol_atom_a_loc = find_location(mol_atom_a)
        res_loc, res_loc_2 = find_residue_loc(residue)
        n_names, neighbors_neighbors_names = process_mol_atom_a(mol_atom_a)
        n_locations = []
        for atom in n_names:
            n_locations.append(find_location(atom))
        nn_locations = []
        for atom_list in neighbors_neighbors_names:
            atomsn = []
            for atom in atom_list:
                atomsn.append(find_location(atom))
            nn_locations.append(atomsn)

        selected_mol_loc, selected_mol_names, res_id = choose_neighbors(res_loc, res_loc_2, mol_atom_a, n_names, neighbors_neighbors_names, mol_atom_a_loc, n_locations, nn_locations)
        if res_id == 0:
            res_true = res_loc
            res_names = find_residue_names(residue)[0]
        else:
            res_true = res_loc_2
            res_names = find_residue_names(residue)[1]
        if valid(res_true, selected_mol_loc):
            vbla = open('vbla.txt', 'w')
            vbla_string = ''
            for item in selected_mol_names:
                vbla_string += item
                vbla_string += ' '
            vbla.write(vbla_string)
            vbla2 = open('vbla2.txt', 'w')
            vbla2_string = ''
            for item in res_names:
                vbla2_string += item
                vbla2_string += ' '
            vbla2.write(vbla2_string)
            break
        atoms.pop(np.argmin(distances))
        residues.pop(np.argmin(distances))
        distances.pop(np.argmin(distances))
        if len(atoms) == 0:
            atom_names, atom_distances = centroid_search()
            ca_names, ca_locs = find_ca_atoms()
            for j in range(len(atom_names)):
                atom_n = atom_names[np.argmin(atom_distances)]
                atom_d = atom_distances[np.argmin(atom_distances)]
                valid_ca_names = []
                valid_ca_locs = []
                valid_mol_names = []
                valid_mol_locs = []
                atom_l = find_location(atom_n)
                n_names, neighbors_neighbors_names = process_mol_atom_a(atom_n)
                n_locations = []
                for atom in n_names:
                    n_locations.append(find_location(atom))
                nn_locations = []
                for atom_list in neighbors_neighbors_names:
                    atomsn = []
                    for atom in atom_list:
                        atomsn.append(find_location(atom))
                    nn_locations.append(atomsn)
                for k in range(len(ca_names)-2):
                    res_loc = (ca_locs[k], ca_locs[k+1], ca_locs[k+2])
                    res_loc_2 = tuple(reversed(res_loc))
                    selected_mol_loc, selected_mol_names, res_id = choose_neighbors(res_loc, res_loc_2, atom_n, n_names, neighbors_neighbors_names, atom_l, n_locations, nn_locations)
                    if res_id == 0:
                        res_true = res_loc
                        res_names = (ca_names[k], ca_names[k+1], ca_names[k+2])
                    else:
                        res_true = res_loc_2
                        res_names = (ca_names[k+2], ca_names[k+1], ca_names[k])
                    if valid(res_true, selected_mol_loc):
                        valid_ca_names.append(res_names)
                        valid_ca_locs.append(res_true)
                        valid_mol_names.append(selected_mol_names)
                        valid_mol_locs.append(selected_mol_loc)
                distance_a_A = []
                for k in range(len(valid_mol_locs)):
                    distance_a_A.append(get_distance(valid_mol_locs[k][0], valid_ca_locs[k][0]))
                if distance_a_A[np.argmin(distance_a_A)] < 10:
                    selected_mol_names = valid_mol_names[np.argmin(distance_a_A)]
                    res_names = valid_ca_names[np.argmin(distance_a_A)]
                    vbla = open('vbla.txt', 'w')
                    vbla_string = ''
                    for item in selected_mol_names:
                        vbla_string += item
                        vbla_string += ' '
                    vbla.write(vbla_string)
                    vbla2 = open('vbla2.txt', 'w')
                    vbla2_string = ''
                    for item in res_names:
                        vbla2_string += item
                        vbla2_string += ' '
                    vbla2.write(vbla2_string)
                    break
                else:
                    atom_names.pop(np.argmin(atom_distances))
                    atom_distances.pop(np.argmin(atom_distances))

def exec2(df1_rel, df2_rel, pdb_file):
    if len(df1_rel) > 0:
        mol_atom_a = df1_rel['Donor'][0].split('@')[1]
        residue = df1_rel['Acceptor'][0].split('@')[0]
    else:
        mol_atom_a = df2_rel['Acceptor'][0].split('@')[1]
        residue = df2_rel['Donor'][0].split('@')[0]
    mol_atom_a_loc = find_location(mol_atom_a)
    res_loc, res_loc_2 = find_residue_loc(residue)
    n_names, neighbors_neighbors_names = process_mol_atom_a(mol_atom_a)
    n_locations = []
    for atom in n_names:
        n_locations.append(find_location(atom))
    nn_locations = []
    for atom_list in neighbors_neighbors_names:
        atoms = []
        for atom in atom_list:
            atoms.append(find_location(atom))
        nn_locations.append(atoms)

    selected_mol_loc, selected_mol_names, res_id  = choose_neighbors(res_loc, res_loc_2, mol_atom_a, n_names, neighbors_neighbors_names, mol_atom_a_loc, n_locations, nn_locations)
    if res_id == 0:
        res_true = res_loc
        res_names = find_residue_names(residue)[0]
    else:
        res_true = res_loc_2
        res_names = find_residue_names(residue)[1]
    if valid(res_true, selected_mol_loc):

        vbla = open('vbla.txt', 'w')
        vbla_string = ''
        for item in selected_mol_names:
            vbla_string += item
            vbla_string += ' '
        vbla.write(vbla_string)
        vbla2 = open('vbla2.txt', 'w')
        vbla2_string = ''
        for item in res_names:
            vbla2_string += item
            vbla2_string += ' '
        vbla2.write(vbla2_string)
    else:
        atom_names, atom_distances = centroid_search()
        ca_names, ca_locs = find_ca_atoms()
        for j in range(len(atom_names)):
            atom_n = atom_names[np.argmin(atom_distances)]
            atom_d = atom_distances[np.argmin(atom_distances)]
            valid_ca_names = []
            valid_ca_locs = []
            valid_mol_names = []
            valid_mol_locs = []
            atom_l = find_location(atom_n)
            n_names, neighbors_neighbors_names = process_mol_atom_a(atom_n)

            n_locations = []
            for atom in n_names:
                n_locations.append(find_location(atom))
            nn_locations = []
            for atom_list in neighbors_neighbors_names:
                atomsn = []
                for atom in atom_list:
                    atomsn.append(find_location(atom))
                nn_locations.append(atomsn)
            distance_test = []
            distance_locs = []
            for k in range(len(ca_names)-2):
                res_loc = (ca_locs[k], ca_locs[k+1], ca_locs[k+2])
                res_loc_2 = tuple(reversed(res_loc))
                selected_mol_loc, selected_mol_names, res_id = choose_neighbors(res_loc, res_loc_2, atom_n, n_names, neighbors_neighbors_names, atom_l, n_locations, nn_locations)
                if res_id == 0:
                    res_true = res_loc
                    res_names = (ca_names[k], ca_names[k+1], ca_names[k+2])
                else:
                    res_true = res_loc_2
                    res_names = (ca_names[k+2], ca_names[k+1], ca_names[k])
                if valid(res_true, selected_mol_loc):
                    valid_ca_names.append(res_names)
                    valid_ca_locs.append(res_true)
                    valid_mol_names.append(selected_mol_names)
                    valid_mol_locs.append(selected_mol_loc)
                distance_test.append(get_distance(atom_l, ca_locs[k]))
                distance_locs.append((atom_l, ca_locs[k]))
            distance_a_A = []
            locs_a_A = []
            for k in range(len(valid_mol_locs)):
                locs_a_A.append((valid_mol_locs[k][0], valid_ca_locs[k][0]))
                distance_a_A.append(get_distance(valid_mol_locs[k][0], valid_ca_locs[k][0]))
            if len(distance_a_A) > 0:

                if distance_a_A[np.argmin(distance_a_A)] < 10:
                    selected_mol_names = valid_mol_names[np.argmin(distance_a_A)]
                    res_names = valid_ca_names[np.argmin(distance_a_A)]
                    vbla = open('vbla.txt', 'w')
                    vbla_string = ''
                    for item in selected_mol_names:
                        vbla_string += item
                        vbla_string += ' '
                    vbla.write(vbla_string)
                    vbla2 = open('vbla2.txt', 'w')
                    vbla2_string = ''
                    for item in res_names:
                        vbla2_string += item
                        vbla2_string += ' '
                    vbla2.write(vbla2_string)
                    break
                else:
                    atom_names.pop(np.argmin(atom_distances))
                    atom_distances.pop(np.argmin(atom_distances))
            else:
                atom_names.pop(np.argmin(atom_distances))
                atom_distances.pop(np.argmin(atom_distances))

#centroid search
def exec3(pdb_file):
    atom_names, atom_distances = centroid_search()
    ca_names, ca_locs = find_ca_atoms()
    for j in range(len(atom_names)):
        atom_n = atom_names[np.argmin(atom_distances)]
        atom_d = atom_distances[np.argmin(atom_distances)]
        valid_ca_names = []
        valid_ca_locs = []
        valid_mol_names = []
        valid_mol_locs = []
        atom_l = find_location(atom_n)
        n_names, neighbors_neighbors_names = process_mol_atom_a(atom_n)

        n_locations = []
        for atom in n_names:
            n_locations.append(find_location(atom))
        nn_locations = []
        for atom_list in neighbors_neighbors_names:
            atomsn = []
            for atom in atom_list:
                atomsn.append(find_location(atom))
            nn_locations.append(atomsn)
        distance_test = []
        distance_locs = []
        for k in range(len(ca_names)-2):
            res_loc = (ca_locs[k], ca_locs[k+1], ca_locs[k+2])
            res_loc_2 = tuple(reversed(res_loc))
            selected_mol_loc, selected_mol_names, res_id = choose_neighbors(res_loc, res_loc_2, atom_n, n_names, neighbors_neighbors_names, atom_l, n_locations, nn_locations)
            if res_id == 0:
                res_true = res_loc
                res_names = (ca_names[k], ca_names[k+1], ca_names[k+2])
            else:
                res_true = res_loc_2
                res_names = (ca_names[k+2], ca_names[k+1], ca_names[k])
            if valid(res_true, selected_mol_loc):
                valid_ca_names.append(res_names)
                valid_ca_locs.append(res_true)
                valid_mol_names.append(selected_mol_names)
                valid_mol_locs.append(selected_mol_loc)
            distance_test.append(get_distance(atom_l, ca_locs[k]))
            distance_locs.append((atom_l, ca_locs[k]))
        distance_a_A = []
        locs_a_A = []
        for k in range(len(valid_mol_locs)):
            locs_a_A.append((valid_mol_locs[k][0], valid_ca_locs[k][0]))
            distance_a_A.append(get_distance(valid_mol_locs[k][0], valid_ca_locs[k][0]))
        if len(distance_a_A) > 0:

            if distance_a_A[np.argmin(distance_a_A)] < 10:
                selected_mol_names = valid_mol_names[np.argmin(distance_a_A)]
                res_names = valid_ca_names[np.argmin(distance_a_A)]
                vbla = open('vbla.txt', 'w')
                vbla_string = ''
                for item in selected_mol_names:
                    vbla_string += item
                    vbla_string += ' '
                vbla.write(vbla_string)
                vbla2 = open('vbla2.txt', 'w')
                vbla2_string = ''
                for item in res_names:
                    vbla2_string += item
                    vbla2_string += ' '
                vbla2.write(vbla2_string)
                break
            else:
                atom_names.pop(np.argmin(atom_distances))
                atom_distances.pop(np.argmin(atom_distances))
        else:
            atom_names.pop(np.argmin(atom_distances))
            atom_distances.pop(np.argmin(atom_distances))

#########Functions#########

def find_neighbors(mol, test_loc=''):
    #Return atom numbers via connectivity of mol2 file
    #input: string mol ('C4'), string test_loc (path to file)
    #returns: string list containing indices of neighbors
    global ligand_file
    if test_loc != '':
        ligand_file = test_loc

    atom_num_found = False
    atomn_neighbors = []
    with open(ligand_file, 'r') as ligand:
        for line in ligand:
            if '@<TRIPOS>SUBSTRUCTURE' in line:
                break
            if mol in line:
                line = line.split(' ')
                while '' in line:
                    line.remove('')
                if mol == line[1]:
                    atom_num = line[0]
            if atom_num_found:
                line = line.split(' ')
                while '' in line:
                    line.remove('')
                if atom_num in line[1:3]:
                    if atom_num in line[1]:
                        atomn_neighbors.append(line[2])
                    elif atom_num in line[2]:
                        atomn_neighbors.append(line[1])
            if '@<TRIPOS>BOND' in line:
                atom_num_found = True
    ligand.close()
    return atomn_neighbors

def find_hydrogen_neighbor(moln_list, mol, test_loc=''):
    #If terminal, returns bound heavy atom. Else returns self
    #input: String List moln_list, contains indices of hydrogen neighbors;
    #       String mol, molecule name ('H8')
    #returns: String, name of bound heavy atom ('C7') OR self ('H8')
    #requires: mol is hydrogen
    #          moln_list contains neighbors to mol

    #bug: if mol not in moln_list, still returns mol
    global ligand_file
    if test_loc != '':
        ligand_file = test_loc
    atom_neighbors=[]
    for item in moln_list:
        with open(ligand_file, 'r') as ligand:
            start_checking = False
            for line in ligand:
                if '@<TRIPOS>BOND' in line:
                    start_checking=False
                if start_checking:
                    line = line.split(' ')
                    while '' in line:
                        line.remove('')
                    if item in line:
                        atom_neighbors.append(line[1])
                if '@<TRIPOS>ATOM' in line:
                    start_checking = True
        ligand.close()
    if len(atom_neighbors)==1:
        return atom_neighbors[0]
    else:
        heavy_sum = 0
        for atom in atom_neighbors:
            if not 'H' in atom:
                heavy_sum += 1
        if heavy_sum >= 2:
            return mol
        else:
            for atom in atom_neighbors:
                if not 'H' in atom:
                    return atom

def neighbor_names(moln_list, test_loc=''):
    #Return atom names of heavy atom neighbors
    #input: String moln_list, contains indices of neighbors
    #returns: String List, names of neighbors
    global ligand_file
    if test_loc != '':
        ligand_file = test_loc
    
    atom_neighbors=[]
    for item in moln_list:
        with open(ligand_file, 'r') as ligand:
            start_checking = False
            for line in ligand:
                if '@<TRIPOS>BOND' in line:
                    start_checking=False
                if start_checking:
                    line = line.split(' ')
                    while '' in line:
                        line.remove('')
                    if item == line[0]:
                        atom_neighbors.append(line[1])
                if '@<TRIPOS>ATOM' in line:
                    start_checking = True
        ligand.close()
    heavy_list = []
    for atom in atom_neighbors:
        if not 'H' in atom:
            heavy_list.append(atom)
    return heavy_list

def process_mol_atom_a(atom):
    if 'H' in atom:
        neighbors=find_neighbors(atom)
        atom = find_hydrogen_neighbor(neighbors, atom)
    neighbors=find_neighbors(atom)
    n_names=neighbor_names(neighbors)
    neighbors_neighbors_number = []
    neighbors_neighbors_names = []
    for neighbor in n_names:
        neighbor_neighbor_num = find_neighbors(neighbor)
        neighbor_neighbor_name = neighbor_names(neighbor_neighbor_num)
        nnn_num = []
        nnn_name = []
        for i in range(len(neighbor_neighbor_name)):
            if not (neighbor_neighbor_name[i] == atom or 'H' in neighbor_neighbor_name[i]):
                nnn_num.append(neighbor_neighbor_num[i])
                nnn_name.append(neighbor_neighbor_name[i])
        neighbors_neighbors_names.append(nnn_name)
        neighbors_neighbors_number.append(nnn_num)
    return n_names, neighbors_neighbors_names 

def find_location(atom, test_loc=''):
    #input: String atom ('C4')
    #returns: Tuple (float, float, float) xyz location of atom
    #Assumes that the ligand is the first residue.
    #Should fail if gets to second residue without finding name
    global pdb_file
    if test_loc != '':
        pdb_file = test_loc

    with open(pdb_file, 'r') as ligand:
        for line in ligand:
            line = line.split(' ')
            while '' in line:
                line.remove('')
            if (len(line) >= 5 and line[4] == '1') and atom == line[2]:
                return (float(line[5]), float(line[6]), float(line[7]))
    raise Exception("location not found")

def find_residue_loc(residue, test_loc=''):
    #input: String residue, acceptor from BB.avg.data or BB2.avg.data (GLN_103@OE1)
    #returns: Tuple (Tuple (float, float, float), Tuple (float, float, float)) xyz location of residue
    #         OR None if N, C, CA molecules not found in the group
    global pdb_file
    if test_loc != '':
        pdb_file = test_loc
        
    #dispose of the molecule name (@ and to the right)
    if residue.find('@') != -1:
        residue = residue[:residue.find('@')]
    
    res_name, res_number = residue.split('_')
    with open(pdb_file, 'r') as protein:
        has_N = False
        has_C = False
        has_CA = False
        for line in protein:
            line=line.split(' ')
            while '' in line:
                line.remove('')
            if len(line) == 12:
                if res_name == line[3] and res_number == line[4]:
                    if 'N' == line[2]:
                        N_loc = (float(line[5]), float(line[6]), float(line[7]))
                        has_N = True
                    elif 'C' == line[2]:
                        C_loc = (float(line[5]), float(line[6]), float(line[7]))
                        has_C = True
                    elif 'CA' == line[2]:
                        CA_loc = (float(line[5]), float(line[6]), float(line[7]))
                        has_CA = True
            if has_N and has_C and has_CA:
                return (N_loc, CA_loc, C_loc), (C_loc, CA_loc, N_loc)

def find_residue_names(residue):
    #input: String residue, Donor from BB2.avg.data limited up to the @ (SER_118)
    #returns: Tuple (String, String) names of atoms with residue number (('118@N', '118@CA', '118@C'), ('118@C', '118@CA', '118@N'))
    residue = residue.split('_')[1]
    return (residue+"@N", residue+"@CA", residue+"@C"), (residue+"@C", residue+"@CA", residue+"@N")

def get_distance(atom_a, atom_b):
    #calculates the Euclidean distance between two points represented as atoms in three-dimensional space.
    #input: Tuple (float, float, float) atom_a, Tuple (float, float, float) atom_b. These are atom coordinates.
    #returns: float distance between atom_a and atom_b
    return ((atom_a[0] - atom_b[0])**2 + (atom_a[1] - atom_b[1])**2 + (atom_a[2] - atom_b[2])**2)**.5

def get_angle(a_b, a_c, b_c):
    #returns the angle between sides a_b and b_c given integer lengths
    #input: int a_b, int a_c, int b_c
    #returns: float angle between sides a_b and b_c

    # Check for zero length sides
    if a_b == 0 or a_c == 0 or b_c == 0:
        raise ValueError("Side lengths cannot be zero")
    
    # Check for invalid triangle
    if a_b + b_c <= a_c or a_b + a_c <= b_c or b_c + a_c <= a_b:
        raise ValueError("Invalid triangle sides")
    
    return  np.arccos((b_c**2 + a_b**2 - a_c**2)/(2*b_c*a_b))


def valid(res_loc, mol_loc):
    #returns True if valid residue location and molecule location configuration, otherwise False
    #input: res_loc: tuple of 3 tuples of 3 floats, mol_loc: List of 3 tuples of 3 floats
    A_B_C=get_angle(get_distance(res_loc[0], res_loc[1]), get_distance(res_loc[0], res_loc[2]),
            get_distance(res_loc[1], res_loc[2]))
    if math.pi/4 >= A_B_C or 3*math.pi/4 <= A_B_C:
        return False
    else:
        
        a_A_B = get_angle(get_distance(mol_loc[0], res_loc[0]), get_distance(mol_loc[0], res_loc[1]),
                get_distance(res_loc[0], res_loc[1]))
        if math.pi/4 >= a_A_B or 3*math.pi/4 <= a_A_B:
            return False
        else:
            A_a_b = get_angle(get_distance(mol_loc[0], res_loc[0]), get_distance(mol_loc[1], res_loc[0]),
                get_distance(mol_loc[0], mol_loc[1]))
            if  math.pi/4 >= A_a_b or 3*math.pi/4 <= A_a_b:
                return False
            else:
                a_b_c = get_angle(get_distance(mol_loc[0], mol_loc[1]), get_distance(mol_loc[0], mol_loc[2]),
                    get_distance(mol_loc[1], mol_loc[2]))
                if math.pi/4 >= a_b_c or 3*math.pi/4 <= a_b_c:
                    return False
                else:
                    return True

def calc_angles(res_loc, mol_loc):
    #returns angles in order ABC, aAB, Aab, abc
    #input: res_loc: tuple of 3 tuples of 3 floats, mol_loc: List of 3 tuples of 3 floats
    #returns: tuple of four angles
    A_B_C=get_angle(get_distance(res_loc[0], res_loc[1]), get_distance(res_loc[0], res_loc[2]),
            get_distance(res_loc[1], res_loc[2]))
    a_A_B = get_angle(get_distance(mol_loc[0], res_loc[0]), get_distance(mol_loc[0], res_loc[1]),
            get_distance(res_loc[0], res_loc[1]))
    A_a_b = get_angle(get_distance(mol_loc[0], res_loc[0]), get_distance(mol_loc[1], res_loc[0]),
            get_distance(mol_loc[0], mol_loc[1]))
    a_b_c = get_angle(get_distance(mol_loc[0], mol_loc[1]), get_distance(mol_loc[0], mol_loc[2]),
            get_distance(mol_loc[1], mol_loc[2]))
    return (A_B_C, a_A_B, A_a_b, a_b_c)

def angle_deviation(vec):
    #input: vec: tuple of four floats
    #returns: float mean absolute error of the angles from 90 degrees
    vec = np.array(vec)
    return float(abs((vec-math.pi/2)).mean())

def choose_neighbors(res_loc, res_loc_2, mol_atom_a, n_names, neighbors_neighbors_names, mol_atom_a_loc, n_locations, nn_locations):
    #res_loc res_loc_2 tuple xyz
    #resloc: (ABC)resloc2: (C,B,A), mol: (a, b, c), angles we care about (C,B,A), (B, A, a), (Aab), (abc)
    #r<10

    #scoring: deviation of angles from 90 degress (MAE)
    valid_atoms = []
    valid_locs = []
    valid_res = []
    valid_res_id = []
    for i in range(len(n_names)):
        for j in range(len(neighbors_neighbors_names[i])):
            if len({mol_atom_a_loc, n_locations[i], nn_locations[i][j]}) == 3:
                if valid(res_loc, [mol_atom_a_loc, n_locations[i], nn_locations[i][j]]):
                    valid_locs.append([mol_atom_a_loc, n_locations[i], nn_locations[i][j]])
                    valid_atoms.append([mol_atom_a, n_names[i], neighbors_neighbors_names[i][j]])
                    valid_res.append(res_loc)
                    valid_res_id.append(0)
                elif valid(res_loc_2, [mol_atom_a_loc, n_locations[i], nn_locations[i][j]]):
                    valid_locs.append([mol_atom_a_loc, n_locations[i], nn_locations[i][j]])
                    valid_atoms.append([mol_atom_a, n_names[i], neighbors_neighbors_names[i][j]])
                    valid_res.append(res_loc_2)
                    valid_res_id.append(1)
            for k in range(len(neighbors_neighbors_names[i])):
                if k != j:
                    if len({mol_atom_a_loc, nn_locations[i][j], nn_locations[i][k]}) == 3:
                        if valid(res_loc, [mol_atom_a_loc, nn_locations[i][j], nn_locations[i][k]]):
                            valid_locs.append([mol_atom_a_loc, nn_locations[i][j], nn_locations[i][k]])
                            valid_atoms.append([mol_atom_a, neighbors_neighbors_names[i][j], neighbors_neighbors_names[i][k]])
                            valid_res.append(res_loc)
                            valid_res_id.append(0)
                        elif valid(res_loc_2, [mol_atom_a_loc, nn_locations[i][j], nn_locations[i][k]]):
                            valid_locs.append([mol_atom_a_loc, nn_locations[i][j], nn_locations[i][k]])
                            valid_atoms.append([mol_atom_a, neighbors_neighbors_names[i][j], neighbors_neighbors_names[i][k]])
                            valid_res.append(res_loc_2)
                            valid_res_id.append(1)
            for k in range(len(neighbors_neighbors_names[i])):
                for l in range(len(neighbors_neighbors_names[i])):
                    if k != l:
                        if len({nn_locations[i][k], nn_locations[i][l], mol_atom_a_loc}) == 3:
                            if valid(res_loc, [nn_locations[i][k], nn_locations[i][l], mol_atom_a_loc]):
                                valid_locs.append([nn_locations[i][k], nn_locations[i][l], mol_atom_a_loc])
                                valid_atoms.append([neighbors_neighbors_names[i][k], neighbors_neighbors_names[i][l], mol_atom_a])
                                valid_res.append(res_loc)
                                valid_res_id.append(0)
                            elif valid(res_loc_2, [nn_locations[i][k], nn_locations[i][l], mol_atom_a_loc]):
                                valid_locs.append([nn_locations[i][k], nn_locations[i][l], mol_atom_a_loc])
                                valid_atoms.append([neighbors_neighbors_names[i][k], neighbors_neighbors_names[i][l], mol_atom_a])
                                valid_res.append(res_loc_2)
                                valid_res_id.append(1)
    if len(valid_locs) == 0:
        return [(0,0,0), (1,1,1), (2,2,2)], [mol_atom_a, n_names[0], neighbors_neighbors_names[0][0]], 0
    else:
        scores = []
        for i in range(len(valid_locs)):
            scores.append(angle_deviation(calc_angles(valid_res[i], valid_locs[i])))
        index = np.argmin(scores)
        return valid_locs[index], valid_atoms[index], valid_res_id[index]



def centroid_search(test_loc=''):
    #returns: Tuple, tuple[0] is list of atom names excluding hydrogen, 
    #                tuple[1] is list of respective atom distances from centroid
    global pdb_file
    if test_loc != '':
        pdb_file = test_loc
    ligand=open(pdb_file, 'r')
    start = False
    xs=[]
    ys=[]
    zs=[]
    for line in ligand:
        if 'TER' in line and start == True:
            ligand.close()
            break
        if start:
            lines=line.split(' ')
            while '' in lines:
                lines.remove('')
            xs.append(float(lines[5]))
            ys.append(float(lines[6]))
            zs.append(float(lines[7]))
        if 'CRYST1' in line:
            start = True
    centroid=(sum(xs)/len(xs),sum(ys)/len(ys),sum(zs)/len(zs))
    atom_names = []
    distances = []
    with open(pdb_file, 'r') as l:
        start_finding = False
        for line in l:
            if 'TER' in line and start_finding:
                l.close()
                break
            if start_finding:
                line = line.split(' ')
                while '' in line:
                    line.remove('')
                loc = (float(line[5]), float(line[6]), float(line[7]))
                name = line[2]
                if not 'H' in name:
                    distances.append(get_distance(loc, centroid))
                    atom_names.append(name)
            if 'CRYST1' in line:
                start_finding = True
    return atom_names, distances
    
def find_ca_atoms(test_loc=''):
    #returns: Tuple, tuple[0] is list of atom names (CA only),
    #                tuple[1] is list of respective atom locations
    global pdb_file
    if test_loc != '':
        pdb_file = test_loc

    ca_names = []
    ca_locs = []
    with open(pdb_file, 'r') as f:
        first_ter = False
        for line in f:
            if 'TER' in line and first_ter:
                break
            if first_ter:
                line = line.split(' ')
                while ''  in line:
                    line.remove('')
                if 'CA' == line[2]:
                    ca_names.append(line[4]+'@CA')
                    ca_locs.append((float(line[5]), float(line[6]), float(line[7])))
            if 'TER' in line and not first_ter:
                first_ter = True
    return ca_names, ca_locs

def find_backbone_atoms(test_loc=''):
    #returns: Tuple, tuple[0] is list of atom names (N, C, or CA),
    #                tuple[1] is list of respective atom locations
    global pdb_file
    if test_loc != '':
        pdb_file = test_loc

    backbone_names = []
    backbone_locs = []
    with open(pdb_file, 'r') as f:
        first_ter = False
        for line in f:
            if 'TER' in line and first_ter:
                break
            if first_ter:
                line = line.split(' ')
                while ''  in line:
                    line.remove('')
                if 'CA' == line[2] or 'C' == line[2] or 'N' == line[2] :
                    backbone_names.append(line[4]+'@'+line[2])
                    backbone_locs.append((float(line[5]), float(line[6]), float(line[7])))
            if 'TER' in line and not first_ter:
                first_ter = True
    return backbone_names, backbone_locs