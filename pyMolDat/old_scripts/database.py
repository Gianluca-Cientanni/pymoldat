import os
from pathlib import Path
home = str(Path.home())
import pandas as pd
import mpl_toolkits.mplot3d as plt3d
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import tkinter
import sys
import vpython
from pyparsing import *
import functions
import json
import glob as glob

# directory where molecule files are stored
file_dir = os.path.join(home, 'Desktop/project/example_molecules/')

# list molecule files: below is an example for arg:
clt_files = glob.glob(file_dir + '*.clt')
xyz_files = glob.glob(file_dir + '*.xyz')

# empty dict to host df's
molecules_from_files = {}

# extract information from .clt files
for elem in clt_files:

    # empty dataframe to host data
    df = pd.DataFrame(data={'label': [], 'atomic_number': [], 'x': [], 'y': [], 'z': []})

    # open file
    file_object = open(elem, 'r')
    lines = file_object.readlines()

    molecule_name = os.path.basename(elem)
    molecule_name = os.path.splitext(molecule_name)[-2]

    # parse lines for data extraction
    for line in lines:
        clt_parser = Word(alphanums) + Word(nums + '.' + nums) + Word(printables + '.' + printables) + \
                     Word(printables + '.' + printables) + Word(printables + '.' + printables)
        try:
            parsed_lines = clt_parser.parseString(line)
            list_conversion = list(parsed_lines)
            df = df.append(
                {'label': list_conversion[0], 'atomic_number': float(list_conversion[1]),
                 'x': float(list_conversion[2]), 'y': float(list_conversion[3]),
                 'z': float(list_conversion[4])}, ignore_index=True)

        except Exception:
            print('not valid data line')
    molecules_from_files[str(molecule_name)] = df

# extract information from .xyz files
for elem in xyz_files:

    # empty dataframe to host data
    df = pd.DataFrame(data={'label': [], 'atomic_number': [], 'x': [], 'y': [], 'z': []})

    # open file
    file_object = open(elem, 'r')
    lines = file_object.readlines()

    molecule_name = os.path.basename(elem)
    molecule_name = os.path.splitext(molecule_name)[-2]

    # parse lines for data extraction
    for line in lines:
        clt_parser = Word(alphanums) + Word(printables + '.' + printables) + Word(printables + '.' + printables) + \
                     Word(printables + '.' + printables)
        try:
            parsed_lines = clt_parser.parseString(line)
            list_conversion = list(parsed_lines)
            df = df.append(
                {'label': list_conversion[0], 'atomic_number': functions.periodic_table[list_conversion[0]],
                 'x': float(list_conversion[1]), 'y': float(list_conversion[2]),
                 'z': float(list_conversion[3])}, ignore_index=True)

        except Exception:
            print('not valid data line')
    molecules_from_files[str(molecule_name)] = df

with open('result.json', 'w') as fp:
    json.dump(molecules_from_files, fp, cls=JSONEncoder)

open = json.load(open('result.json'))
