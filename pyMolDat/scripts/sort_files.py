import os
from pathlib import Path
import pandas as pd
import glob
import numpy as np
import json
import atom_database

home = str(Path.home())

file_directory = os.path.join(home, 'Desktop/project/example_molecules')

file_dict = {}

coordinate_files = []

moment_files = []

energy_files = []

# get all files in file hierarchy and sort into each file type
for root, dirs, files in os.walk(file_directory):
    for i in files:
        if os.path.splitext(os.path.basename(root + '/' + i))[1] == '.clt':
            coordinate_files.append(root + '/' + i)

        if os.path.splitext(os.path.basename(root + '/' + i))[1] == '.xyz':
            coordinate_files.append(root + '/' + i)

        if os.path.splitext(os.path.basename(root + '/' + i))[1] == '.pdb':
            coordinate_files.append(root + '/' + i)

        if os.path.splitext(os.path.basename(root + '/' + i))[1] == '.mom':
            moment_files.append(root + '/' + i)

file_dict['coordinates'] = coordinate_files
file_dict['moments'] = moment_files

