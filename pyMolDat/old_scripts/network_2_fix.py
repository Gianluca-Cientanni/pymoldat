import os
from pathlib import Path
home = str(Path.home())
import pandas as pd
import numpy as np
import functions
import atom_database
import json

# directory where molecule files are stored
file_dir = os.path.join(home, 'Desktop/project/example_molecules/')

# function extracts atomic coordinates
information = functions.extract_info(file_dir)

# load bond details from database
database = atom_database.database

# add covalent radius to each atom (here we'll need to figure out how to use Tkinter to select drop down bar to choose molecule)
molecule = information['pyridine']
array = []

for i in range(len(molecule)):
    atom_number = molecule.get_value(i, col='atomic_number')
    radii = database.get_value(index=int(atom_number - 1), col='cov_rad')
    array.append(radii)
molecule.insert(2, 'cov_rad', array)

# empty dataframe to append atomic pairs that are bonded
atomic_pairs = pd.DataFrame(data={'index': [], 'pair': [], 'bond_length': [], 'probability': []})

# fills an array with atomic pairs and removes the self duplicate, ([3,3]) for example
index = []
for i in range(len(molecule)):
    for j in range(len(molecule)):
        if i != j:
            index.append([i,j])
        else:
            continue

# removes a reversed duplicate (will remove [0,1] and leave [1,0], for example)
for k, val in enumerate(index):
    for m in index:
        if [val[0], val[1]] == [m[1], m[0]]:
            index.remove(m)

# distinguish between bonded atoms and non-bonded atoms, fill df with bonded pairs
for i in index:
    first_atom_coord = np.array([molecule.iloc[i[0]][3], molecule.iloc[i[0]][4], molecule.iloc[i[0]][5]])
    second_atom_coord = np.array([molecule.iloc[i[1]][3], molecule.iloc[i[1]][4], molecule.iloc[i[1]][5]])

    # this works out spatial distance between index atoms and also their covalent distance
    # assumes that distances are given in angstrom, code previous to this should be converted to angstrom
    dist = np.linalg.norm((first_atom_coord - second_atom_coord))
    cov_rad_dist = molecule.iloc[i[0]][2] + molecule.iloc[i[1]][2]

    # if the distance between two atoms is less than the sum of their covalent radii, they are considered bonded.
    if dist < cov_rad_dist:
            atomic_pairs = atomic_pairs.append(
                {'index': i, 'pair': molecule.iloc[i[0]][1] + '-' + molecule.iloc[i[1]][1],
                 'bond_length': dist, 'probability': 'work this out'}, ignore_index=True)

    # apply gaussian spread to bond length
    adjustable_sigma = 0.1
    normal_curve = np.random.normal(loc=cov_rad_dist, scale=adjustable_sigma)

