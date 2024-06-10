import sys
import pandas as pd
import numpy as np
import math

from restraint_analysis_functions import *



df1 = pd.read_csv('md-complex/BB.avg.dat', engine='python', sep=r'\s{2,}', header=0, names=['Acceptor', 'DonorH', 'Donor', 'Frames', 'Frac', 'AvgDist', 'AvgAng'])
df2 = pd.read_csv('md-complex/BB2.avg.dat', engine='python', sep=r'\s{2,}', header=0, names=['Acceptor', 'DonorH', 'Donor', 'Frames', 'Frac', 'AvgDist', 'AvgAng'])
df1_rel=df1[df1['Frac'] >= .5]
df2_rel=df2[df2['Frac'] >= .5]

ligand=open('setup/lig_tleap.mol2', 'r')

#check if multiple options, calculate centroid
if len(df1_rel) + len(df2_rel) > 1:
    ligand=open('setup/lig_tleap.mol2', 'r')
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
            ligand=open('setup/lig_tleap.mol2', 'r')
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
            ligand=open('setup/lig_tleap.mol2', 'r')
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
                    
elif len(df1_rel)+len(df2_rel) > 0:
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
