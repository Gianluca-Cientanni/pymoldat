import os
from pathlib import Path
import pandas as pd
import glob
import numpy as np
import json
from pyparsing import alphas, Word, Regex, printables, nums, Keyword, OneOrMore, Combine, Optional
import atom_database
import time
import tkinter
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from tkinter import filedialog

home = str(Path.home())

# extracted basic periodic table info from online source
periodic_table = {'Ac': 89,
 'Ag': 47,
 'Al': 13,
 'Am': 95,
 'Ar': 18,
 'As': 33,
 'At': 85,
 'Au': 79,
 'B': 5,
 'Ba': 56,
 'Be': 4,
 'Bh': 107,
 'Bi': 83,
 'Bk': 97,
 'Br': 35,
 'C': 6,
 'Ca': 20,
 'Cd': 48,
 'Ce': 58,
 'Cf': 98,
 'Cl': 17,
 'Cm': 96,
 'Cn': 112,
 'Co': 27,
 'Cr': 24,
 'Cs': 55,
 'Cu': 29,
 'Db': 105,
 'Ds': 110,
 'Dy': 66,
 'Er': 68,
 'Es': 99,
 'Eu': 63,
 'F': 9,
 'Fe': 26,
 'Fl': 114,
 'Fm': 100,
 'Fr': 87,
 'Ga': 31,
 'Gd': 64,
 'Ge': 32,
 'H': 1,
 'He': 2,
 'Hf': 72,
 'Hg': 80,
 'Ho': 67,
 'Hs': 108,
 'I': 53,
 'In': 49,
 'Ir': 77,
 'K': 19,
 'Kr': 36,
 'La': 57,
 'Li': 3,
 'Lr': 103,
 'Lu': 71,
 'Lv': 116,
 'Mc': 115,
 'Md': 101,
 'Mg': 12,
 'Mn': 25,
 'Mo': 42,
 'Mt': 109,
 'N': 7,
 'Na': 11,
 'Nb': 41,
 'Nd': 60,
 'Ne': 10,
 'Nh': 113,
 'Ni': 28,
 'No': 102,
 'Np': 93,
 'O': 8,
 'Og': 118,
 'Os': 76,
 'P': 15,
 'Pa': 91,
 'Pb': 82,
 'Pd': 46,
 'Pm': 61,
 'Po': 84,
 'Pr': 59,
 'Pt': 78,
 'Pu': 94,
 'Ra': 88,
 'Rb': 37,
 'Re': 75,
 'Rf': 104,
 'Rg': 111,
 'Rh': 45,
 'Rn': 86,
 'Ru': 44,
 'S': 16,
 'Sb': 51,
 'Sc': 21,
 'Se': 34,
 'Sg': 106,
 'Si': 14,
 'Sm': 62,
 'Sn': 50,
 'Sr': 38,
 'Ta': 73,
 'Tb': 65,
 'Tc': 43,
 'Te': 52,
 'Th': 90,
 'Ti': 22,
 'Tl': 81,
 'Tm': 69,
 'Ts': 117,
 'U': 92,
 'V': 23,
 'W': 74,
 'Xe': 54,
 'Y': 39,
 'Yb': 70,
 'Zn': 30,
 'Zr': 40}


# extend JSON encoder to be able to seralise Dataframes
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'to_json'):
            return obj.to_json(orient='records')
        return json.JSONEncoder.default(self, obj)


# Function that extracts molecular information from .clt/.xyz files.
# Takes a file directory and returns a dict of df's
# Will be able to add more file types easily in this way
# ORIGINAL
def extract_info(file_directory):
    # list molecule files: below is an example for arg:
    clt_files = glob.glob(file_directory + '*.clt')
    xyz_files = glob.glob(file_directory + '*.xyz')

    # empty dict to host df's
    molecules_from_files = {}

    # definitions of all the parsing tools used
    clt_parser = Word(alphas + nums) + Word(nums + '.' + nums) + Word(printables + '.' + printables) + \
                 Word(printables + '.' + printables) + Word(printables + '.' + printables)

    xyz_parser = Word(alphas) + Word(printables + '.' + printables) + Word(printables + '.' + printables) + \
                 Word(printables + '.' + printables)

    bohr = Keyword('Bohr')
    angstrom = Keyword('Angstrom')
    word = ~bohr + Word(alphas)
    sentence = OneOrMore(word)
    split_bohr = sentence('unit') + bohr + sentence('degree')
    split_angstrom = Keyword('Units') + angstrom
    unit_array = []
    error_array = []

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

            # find out units of distance in file
            try:
                res1 = split_bohr.parseString(line)
                if res1[1] == 'Bohr':
                    unit_array.append(res1[1])
            except Exception:
                print('invalid unit line')
            try:
                res2 = split_angstrom.parseString(line)
                if res2[1] == 'Angstrom':
                    unit_array.append(res2[1])

            except Exception:
                print('not valid data line')

            try:
                parsed_lines = clt_parser.parseString(line)
                list_conversion = list(parsed_lines)
                df = df.append(
                    {'label': list_conversion[0][0], 'atomic_number': float(list_conversion[1]),
                     'x': float(list_conversion[2]), 'y': float(list_conversion[3]),
                     'z': float(list_conversion[4])}, ignore_index=True)
                print('valid data line')
            except Exception:
                print('not valid data line')

        # perform necessary unit conversions
        if len(unit_array) == 1:
            if unit_array[0] == 'Angstrom':
                print('Units are Angstrom')
            elif unit_array[0] == 'Bohr':
                df['x'] = df['x'] / 1.89
                df['y'] = df['y'] / 1.89
                df['z'] = df['z'] / 1.89
        # ambiguous case, just have to assume it's bohr but add line in summary file explaining ambiguity
        elif len(unit_array) == 2:
            print('ambiguous units')
            unit_array.clear()
            unit_array.append('Unknown')
            error_array.append('Ambiguous unit in file.')

        molecules_from_files[str(molecule_name)] = df

        if len(clt_files) > 1:
            print('there are too many coordinate files, ambiguous')
            error_array.append('There are too many coordinate files, see file origin above for file used.')

    # extract information from .xyz files:
    for elem in xyz_files:

        # empty dataframe to host data
        df_2 = pd.DataFrame(data={'label': [], 'atomic_number': [], 'x': [], 'y': [], 'z': []})

        # open file
        file_object = open(elem, 'r')
        lines = file_object.readlines()

        molecule_name = os.path.basename(elem)
        molecule_name = os.path.splitext(molecule_name)[-2]

        # parse lines for data extraction
        for line in lines:

            try:
                parsed_lines = xyz_parser.parseString(line)
                list_conversion = list(parsed_lines)
                atomic_number_df = atom_database.database[atom_database.database['symbol'] == list_conversion[0]]
                atomic_number = atomic_number_df.iloc[0][0]
                df_2 = df_2.append(
                    {'label': list_conversion[0], 'atomic_number': atomic_number,
                     'x': float(list_conversion[1]), 'y': float(list_conversion[2]),
                     'z': float(list_conversion[3])}, ignore_index=True)
                print('valid data line')
            except Exception:
                print('not valid data line')
        molecules_from_files[str(molecule_name)] = df_2

    if len(error_array) == 0:
        error_array.append('No errors')

    # create a json object that will be saved to a summary file
    for key, value in molecules_from_files.items():
        coord_string = value.to_string().splitlines()

        coord_data = {

            'File origin': file_directory,
            'Error list': error_array,
            'Units': unit_array[0],
            'Coordinate Data': coord_string

        }

        with open("coord_test.json", "w") as coord_json:
            json.dump(coord_data, coord_json, indent=4)

    return(molecules_from_files)


# extracts atomic positions and saves them to a json file
def extract_coordinates(file_directory):
    # list molecule files: below is an example for arg:
    clt_files = glob.glob(file_directory + '*.clt')
    xyz_files = glob.glob(file_directory + '*.xyz')

    # empty dict to host df's
    molecules_from_files = {}

    # definitions of all the parsing tools used
    clt_parser = Word(alphas + nums) + Word(nums + '.' + nums) + Word(printables + '.' + printables) + \
                 Word(printables + '.' + printables) + Word(printables + '.' + printables)

    xyz_parser = Word(alphas) + Word(printables + '.' + printables) + Word(printables + '.' + printables) + \
                 Word(printables + '.' + printables)

    bohr = Keyword('Bohr')
    angstrom = Keyword('Angstrom')
    word = ~bohr + Word(alphas)
    sentence = OneOrMore(word)
    split_bohr = sentence('unit') + bohr + sentence('degree')
    split_angstrom = Keyword('Units') + angstrom
    unit_array = []
    error_array = []

    # empty dataframe to host data
    df = pd.DataFrame(data={'label': [], 'atomic_number': [], 'x': [], 'y': [], 'z': []})

    if len(clt_files) or len(xyz_files) or (len(clt_files) + len(xyz_files)) > 1:

        # extract information from .clt files
        for elem in clt_files:

            # open file
            file_object = open(elem, 'r')
            lines = file_object.readlines()

            molecule_name = os.path.basename(elem)
            molecule_name = os.path.splitext(molecule_name)[-2]

            # parse lines for data extraction
            for line in lines:

                # find out units of distance in file
                try:
                    res1 = split_bohr.parseString(line)
                    if res1[1] == 'Bohr':
                        unit_array.append(res1[1])
                except Exception:
                    print('invalid unit line')
                try:
                    res2 = split_angstrom.parseString(line)
                    if res2[1] == 'Angstrom':
                        unit_array.append(res2[1])

                except Exception:
                    print('not valid data line')

                try:
                    parsed_lines = clt_parser.parseString(line)
                    list_conversion = list(parsed_lines)
                    df = df.append(
                        {'label': list_conversion[0][0], 'atomic_number': float(list_conversion[1]),
                         'x': float(list_conversion[2]), 'y': float(list_conversion[3]),
                         'z': float(list_conversion[4])}, ignore_index=True)
                    print('valid data line')
                except Exception:
                    print('not valid data line')

            # perform necessary unit conversions
            if len(unit_array) == 1:
                if unit_array[0] == 'Angstrom':
                    print('Units are Angstrom')
                elif unit_array[0] == 'Bohr':
                    df['x'] = df['x'] / 1.89
                    df['y'] = df['y'] / 1.89
                    df['z'] = df['z'] / 1.89
            # ambiguous case, just have to assume it's bohr but add line in summary file explaining ambiguity
            elif len(unit_array) == 2:
                print('ambiguous units')
                unit_array.clear()
                unit_array.append('Unknown')
                error_array.append('Ambiguous unit in file.')

            molecules_from_files[str(molecule_name)] = df

            if len(clt_files) > 1:
                print('there are too many clt files, ambiguous')
                error_array.append('There are too many .clt files, see file origin above for file used.')

        # extract information from .xyz files:
        for elem in xyz_files:

            # empty dataframe to host data
            df_2 = pd.DataFrame(data={'label': [], 'atomic_number': [], 'x': [], 'y': [], 'z': []})

            # open file
            file_object = open(elem, 'r')
            lines = file_object.readlines()

            molecule_name = os.path.basename(elem)
            molecule_name = os.path.splitext(molecule_name)[-2]

            # parse lines for data extraction
            for line in lines:

                try:
                    parsed_lines = xyz_parser.parseString(line)
                    list_conversion = list(parsed_lines)
                    atomic_number_df = atom_database.database[atom_database.database['symbol'] == list_conversion[0]]
                    atomic_number = atomic_number_df.iloc[0][0]
                    df_2 = df_2.append(
                        {'label': list_conversion[0], 'atomic_number': atomic_number,
                         'x': float(list_conversion[1]), 'y': float(list_conversion[2]),
                         'z': float(list_conversion[3])}, ignore_index=True)
                    print('valid data line')
                except Exception:
                    print('not valid data line')
            molecules_from_files[str(molecule_name)] = df_2

        if len(error_array) == 0:
            error_array.append('No errors')

        # create a json object that will be saved to a summary file
        for key, value in molecules_from_files.items():
            coord_string = value.to_string().splitlines()

            coord_data = {

                'coordinates': {

                    'file': file_directory,
                    'data frame': df.to_json(),
                    'errors': error_array,
                    'units': unit_array[0],
                    'coordinates': coord_string

                }

            }

            # save information to json file called coord_test.json
            # with open("coord_test.json", "w") as coord_json:
            #     json.dump(coord_data, coord_json, indent=4)

    else:

        # extract information from .clt files
        for elem in clt_files:

            # open file
            file_object = open(elem, 'r')
            lines = file_object.readlines()

            molecule_name = os.path.basename(elem)
            molecule_name = os.path.splitext(molecule_name)[-2]

            # parse lines for data extraction
            for line in lines:

                # find out units of distance in file
                try:
                    res1 = split_bohr.parseString(line)
                    if res1[1] == 'Bohr':
                        unit_array.append(res1[1])
                except Exception:
                    print('invalid unit line')
                try:
                    res2 = split_angstrom.parseString(line)
                    if res2[1] == 'Angstrom':
                        unit_array.append(res2[1])

                except Exception:
                    print('not valid data line')

                try:
                    parsed_lines = clt_parser.parseString(line)
                    list_conversion = list(parsed_lines)
                    df = df.append(
                        {'label': list_conversion[0][0], 'atomic_number': float(list_conversion[1]),
                         'x': float(list_conversion[2]), 'y': float(list_conversion[3]),
                         'z': float(list_conversion[4])}, ignore_index=True)
                    print('valid data line')
                except Exception:
                    print('not valid data line')

            # perform necessary unit conversions
            if len(unit_array) == 1:
                if unit_array[0] == 'Angstrom':
                    print('Units are Angstrom')
                elif unit_array[0] == 'Bohr':
                    df['x'] = df['x'] / 1.89
                    df['y'] = df['y'] / 1.89
                    df['z'] = df['z'] / 1.89
            # ambiguous case, just have to assume it's bohr but add line in summary file explaining ambiguity
            elif len(unit_array) == 2:
                print('ambiguous units')
                unit_array.clear()
                unit_array.append('Unknown')
                error_array.append('Ambiguous unit in file.')

        # extract information from .xyz files:
        for elem in xyz_files:

            # empty dataframe to host data
            df_2 = pd.DataFrame(data={'label': [], 'atomic_number': [], 'x': [], 'y': [], 'z': []})

            # open file
            file_object = open(elem, 'r')
            lines = file_object.readlines()

            molecule_name = os.path.basename(elem)
            molecule_name = os.path.splitext(molecule_name)[-2]

            # parse lines for data extraction
            for line in lines:

                try:
                    parsed_lines = xyz_parser.parseString(line)
                    list_conversion = list(parsed_lines)
                    atomic_number_df = atom_database.database[atom_database.database['symbol'] == list_conversion[0]]
                    atomic_number = atomic_number_df.iloc[0][0]
                    df_2 = df_2.append(
                        {'label': list_conversion[0], 'atomic_number': atomic_number,
                         'x': float(list_conversion[1]), 'y': float(list_conversion[2]),
                         'z': float(list_conversion[3])}, ignore_index=True)
                    print('valid data line')
                except Exception:
                    print('not valid data line')

        if len(error_array) == 0:
            error_array.append('No errors')

        # create a json object that will be saved to a summary file

    coord_string = df.to_string().splitlines()

    coord_data = {

        'coordinates': {

            'file': file_directory,
            'data frame': df.to_json(),
            'errors': error_array,
            'units': unit_array[0],
            'coordinates': coord_string

        }

    }

    # with open("coord_test.json", "w") as coord_json:
    #     json.dump(coord_data, coord_json, indent=4)

    return coord_data


# takes coordinates of a molecule from 'extract info' function and works out approximate bond lengths
# and molecular connectivity
def atomic_pairs(molecule):

    # get atomic information
    array = []

    for i in range(len(molecule)):
        atom_number = molecule.get_value(i, col='atomic_number')
        radii = atom_database.database.get_value(index=int(atom_number - 1), col='cov_rad')
        array.append(radii)
    molecule.insert(2, 'cov_rad', array)

    # empty dataframe to append atomic pairs that are bonded
    atomic_pairs = pd.DataFrame(data={'index': [], 'pair': [], 'bond_length': [], 'probability': []})

    # fills an array with atomic pairs and removes the self duplicate, ([3,3]) for example
    index = []
    for i in range(len(molecule)):
        for j in range(len(molecule)):
            if i != j:
                index.append([i, j])
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

        # do this conversion earlier
        dist = np.linalg.norm((first_atom_coord - second_atom_coord))
        cov_rad_dist = molecule.iloc[i[0]][2] + molecule.iloc[i[1]][2]

        # if the distance between two atoms is less than the sum of their covalent radii, they are considered bonded.
        if dist < cov_rad_dist:
            atomic_pairs = atomic_pairs.append(
                {'index': i, 'pair': molecule.iloc[i[0]][1] + '-' + molecule.iloc[i[1]][1],
                 'bond_length': cov_rad_dist, 'probability': 'work this out'},
                ignore_index=True)

    # add gaussian probability of whether atom is actually bonded given a distance/cov rad measurement
    return atomic_pairs


# molecular connectivity algorithm, takes a coordinate data frame and returns a list of lists for each unique molecule
def connected_components(dataframe):

    # work out the molecular connectivity
    atom_pairing = atomic_pairs(dataframe)
    pairs = atom_pairing['index'].tolist()

    # use list of lists to define unique molecules
    molecule_list = []

    for i in pairs:
        temp_array = []
        for ii in pairs:
            temp_pair = [i[0], i[1]]

            if temp_pair[0] == ii[0]:
                temp_array.append(ii[1])
                temp_array = set(temp_array)
                temp_array = list(temp_array)
            if temp_pair[1] == ii[1]:
                temp_array.append(ii[0])
                temp_array = set(temp_array)
                temp_array = list(temp_array)

            for iii in temp_array:
                for j in pairs:
                    if iii == j[0]:
                        temp_array.append(j[1])
                        temp_array = set(temp_array)
                        temp_array = list(temp_array)
                    if iii == j[1]:
                        temp_array.append(j[0])
                        temp_array = set(temp_array)
                        temp_array = list(temp_array)

            if len(temp_array) > len(dataframe):
                break
        molecule_list.append(temp_array)

    molecule_list = [list(item) for item in set(tuple(row) for row in molecule_list)]

    return molecule_list


# function that converts .txt files to .xyz
def convert_to_xyz(file_dir):

    # converts .txt/.pdb into ordered .xyz files, will be a function for functions.py to call at beginning of viewer.
    file_list = os.listdir(file_dir)

    # list all different file extensions
    xyz = [i for i in file_list if os.path.splitext(i)[1] == '.xyz']
    clt = [i for i in file_list if os.path.splitext(i)[1] == '.clt']
    pdb = [i for i in file_list if os.path.splitext(i)[1] == '.pdb']
    txt = [i for i in file_list if os.path.splitext(i)[1] == '.txt']

    # convert generic txt's to xyz's (may not work for all txt's)
    for elem in range(len(txt)):

        # iterate over each txt file
        file = os.path.join(file_dir, txt[elem])

        # molecule name
        molecule_name = os.path.splitext(txt[elem])[0]

        # open file
        file_object = open(file, 'r')
        lines = file_object.readlines()

        # list to contain extracted information
        full_data_set = []

        # parse lines for data extraction
        for line in lines:

            try:
                # define how to read floats
                float_definition = Regex(r'[+-]?\d+\.\d*')

                # parse for the element and 3 spatial coords
                parse_float = Word(alphas) + float_definition + float_definition + float_definition
                parsed_line = parse_float.parseString(line)
                list_conversion = list(parsed_line)
                full_data_set.append(list_conversion)

            except Exception:
                print('invalid data line')

        # make newfile and prepare to write
        new_file_name = molecule_name + '.xyz'
        new_file = open(new_file_name, 'w')
        new_file.write(str(len(full_data_set)) + '\n' + molecule_name + '\n' + '\n' + '\n')

        # add atomic coords and elements
        for i in full_data_set:
            new_file.write(i[0] + '     ' + i[1] + '     ' + i[2] + '     ' + i[3])
            new_file.write('\n')

    return


# makes a 'pretty print' table to a .txt file, takes a pd.df and prints a table.
def pretty_table(dataframe, molecule_name):

    file_name = str(molecule_name) + '.txt'

    coord_string = dataframe.to_string().splitlines()

    data = {

        'Header Information': [{

            'Name of Molecule': molecule_name

        }],

        'Coordinates': coord_string

    }

    with open("coord_test.json", "w") as summary_file:
        json.dump(data, summary_file, indent=4)

    return()


# extract moments information from .mom file, akin to extract_coords function
def extract_moments(file_directory):

    # list to host directory for each unique .mom file
    mom_files = []
    # search through entire file hierarchy to find all .mom files to parse
    for root, dirs, files in os.walk(file_directory):
        for i in files:
            # select only .mom files and add them to list
            if os.path.splitext(os.path.basename(root + '/' + i))[1] == '.mom':
                mom_files.append(root + '/' + i)

    # define parsing grammar
    # find the df type from .mom file
    df_parser = Keyword("! Based on DF-type :") + Word(alphas)

    # parse floating point numbers
    float_parser = Combine(Optional('-') + Word(nums) + '.' + Word(nums))
    mom_parser = OneOrMore(float_parser)

    # parse a line common to all .mom files with the following structure: ATOM  X   Y   Z   Type <ATOM-TYPE>   Rank K
    atom_line = Word(alphas + nums) + mom_parser + OneOrMore(Word(alphas)) + Word(nums)

    # lists for storing information
    error_array, df_array, coords, atom = ([],)*4

    # json array to compile each atom multipole moment info
    json_result = {'moments': []}

    # empty dataframe to host atom information
    df = pd.DataFrame(data={'atom': [], 'type': [], 'rank': []})

    # dictionary to store sorted moment values
    atom_mom = {}

    # using pyparsing's 'search string' method
    for elem in mom_files:

        # open file
        file_object = open(elem, 'r')
        lines = file_object.readlines()

        mom_name = os.path.basename(elem)
        mom_name = os.path.splitext(mom_name)[-2]

        # parse lines for data extraction
        for line in lines:

            # get df type first
            try:
                res1 = df_parser.parseString(line)
                df_array.append(res1[1])
            except Exception:
                print('No DF-Type is specified in file')
                error_array.append('No DF-Type is specified in file')

            # get information about each atom
            try:
                res2 = atom_line.parseString(line)
                atom.append(res2[0])
                type = res2[5]
                rank = (res2[7])
                df = df.append({'atom': atom[len(atom) - 1], 'type': type, 'rank': rank}, ignore_index=True)

            except Exception:
                print('This is not a atom type line')

            # get moment values
            try:
                res3 = mom_parser.parseString(line)
                for i in res3:
                    coords.append(i)
            except Exception:
                print('This is not a moment value')

        coords_float = []

        for val in coords:
            coords_float.append(np.float(val))

        # assign the correct values from coords to the right moment value
        for i in range(len(atom)):

            # get atom information (+1 is so that Q0 is also counted as well as Q4: Q0, Q1, Q2, Q3, Q4)
            name = df.iloc[i]['atom']
            r = int(df.iloc[i]['rank']) + 1

            array, tot, cum_sum = ([],)*3

            # find correct number of coordinates to fill each moment configuration with
            for ii in range(r):
                s = 2 * ii + 1
                tot.append(s)
                cum_sum.append(np.cumsum(tot).tolist())
                cum_sum = cum_sum[len(cum_sum) - 1]

            total = np.sum(tot)

            # value in tot is the number of values stored in each Q layer
            for value in tot:
                temporary_array = []

                # k in range() ensures the correct number of moments is filled in each layer
                for k in range(value):
                    temporary_array.append(coords_float[k])

                array.append(temporary_array)

                for kkk in temporary_array:
                    coords_float.pop(coords_float.index(kkk))

            # fill a dictionary with atoms as keys and moments as values
            atom_mom[atom[i]] = array

        # need to loop over elements in dataframe to add each value for every atom in atom_mom, here we need to do
        # the JSON method too and probably wipe the contents of the dataframe at the beginning of each new loop
        for idx, kk in enumerate(atom_mom):

            # need to reshape lists, first, find max value list can be
            max_len = max(len(i) for i in atom_mom[kk])

            # pad short lists with NaN
            for col in atom_mom[kk]:
                col.extend((max_len - len(col)) * [np.nan])

            # convert to array
            arr = np.asarray(atom_mom[kk]).T

            # create indices depending on rank
            indices = []
            for ind in range(1, len(atom_mom[kk])):
                one = f'{ind}s'
                two = f'{ind}c'
                indices.append(one)
                indices.append(two)
            indices.insert(0, '0')

            # create df depending on rank also
            df_mom = pd.DataFrame(
                arr,
                columns=[f'Q{i}' for i in range(0, len(atom_mom[kk]))],
                index=indices
            )

            moments_string = df_mom.to_string().splitlines()

            mom_data = {

                'atom': atom[idx],
                'scheme': mom_name,
                'type': df['type'][idx],
                'rank': df['rank'][idx],
                'moments': moments_string,
                'file': elem

            }
            json_result['moments'].append({kk: mom_data})

        # save this information to a json file called mom_test.json
        # with open("mom_test.json", "w") as mom_json:
        #     json.dump(json_result, mom_json, indent=4)

    return json_result


# get list of relevent files, also produces dictionary with root folder and subsequent files
def get_files(file_directory):
    file_dict = {}

    coordinate_files, moment_files, energy_files = ([],)*3

    for root, dirs, files in os.walk(file_directory):
        for i in files:

            if os.path.splitext(os.path.basename(root + '/' + i))[1] == '.clt' \
                    or os.path.splitext(os.path.basename(root + '/' + i))[1] == '.xyz' \
                    or os.path.splitext(os.path.basename(root + '/' + i))[1] == '.pdb':
                coordinate_files.append(root + '/' + i)

            if os.path.splitext(os.path.basename(root + '/' + i))[1] == '.mom':
                moment_files.append(root + '/' + i)

            if os.path.splitext(os.path.basename(root + '/' + i))[1] == '.tgz':
                energy_files.append(root + '/' + i)

    file_dict['coordinates'] = coordinate_files
    file_dict['moments'] = moment_files
    file_dict['energy'] = energy_files

    return file_dict


# create file directory for new calculations and add json summary files to folder
def add_to_database(coordinates, moments, file_directory):

    # home path
    home = str(Path.home())

    # time this script is ran
    ts = time.strftime("%Y_%m_%d_%H;%M", time.gmtime())

    # # location of directory
    # file_dir = os.path.join(home, 'Desktop/project/example_molecules/ISA')
    # file_list = os.listdir(file_dir)

    # create database
    database_dir = home + '/pymoldatabase'

    try:
        os.mkdir(database_dir)

    except FileExistsError:
        print('Database already exists')

    ### BASIC - look at file extensions and understand the file

    file_dict = {}

    coordinate_files, moment_files, energy_files = ([],)*3

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

            if os.path.splitext(os.path.basename(root + '/' + i))[1] == '.tgz':
                energy_files.append(root + '/' + i)

    file_dict['coordinates'] = coordinate_files
    file_dict['moments'] = moment_files
    file_dict['energy'] = energy_files

    file_name = os.path.basename(file_directory)

    # new directory for this molecule in DB
    try:
        os.mkdir(database_dir + '/' + file_name)

    except FileExistsError:
        print('This molecule already exists')

    new_folder = database_dir + '/' + file_name + '/' + ts

    # make new folder for this file which will contain the json files
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)
    else:
        print('this dont work')

    # add json files to newly created folder
    with open((new_folder + '/' + "coordinates.json"), "w") as coord_json:
        json.dump(coordinates, coord_json, indent=4)

    with open((new_folder + '/' + "moments.json"), "w") as mom_json:
        json.dump(moments, mom_json, indent=4)

    return


# gives json_summary in mini GUI window for individual moment queries
def gui_moment_query(mom_data, list_of_atoms):

    root = tkinter.Tk()
    root.title("PyMolDat")
    num = 0
    for item in mom_data["moments"]:
        for k, v in item.items():
            for val in list_of_atoms:
                if k == val:
                    for i, j in v.items():

                        tkinter.Label(root, text=i, width=10, anchor="w", font=("Arial 10 bold", 13)).grid(row=num,
                                                                                                column=0, padx=10, sticky="ne")

                        tkinter.Label(root, text=j if i != "moments" else "\n".join(j), width=80, anchor="w",
                                 font=("Monaco", 10), justify='left').grid(
                            row=num, column=1, padx=5)

                        num += 1
        # break
    root.mainloop()

    return


# gives json_summary in mini GUI window for individual coordinate queries
def gui_coordinate_query(coord_data):

    root = tkinter.Tk()
    root.title("PyMolDat")
    num = 0
    for i, j in coord_data["coordinates"].items():

        tkinter.Label(root, text=i, width=10, anchor="w", font=("Arial 10 bold", 13)).grid(row=num,
                                                                                column=0, padx=10, sticky="ne")

        tkinter.Label(root, text=j if i != "coordinates" else "\n".join(j), width=80, anchor="w",
                 font=("Monaco", 10), justify='left').grid(
            row=num, column=1, padx=5)

        num += 1
# break
    root.mainloop()

    # need to add the matplotlib window here too

    return


# function to search through the database from keywords
def search_json():

    file_directory = home + '/' + 'pymoldatabase'

    choice = []
    for i in os.listdir(file_directory):

        if i != '.DS_Store':
            choice.append(i)
    print('These are the files you can select from for the next input: ' + str(choice))

    # this is where you finished, really this feature should be a tkinter file dialogue box alas...
    phrase = input('Please enter one of the file strings from the above choices')

    file_directory = home + '/' + 'pymoldatabase' + '/' + phrase
    choice = []
    for i in os.listdir(file_directory):

        if i != '.DS_Store':
            choice.append(i)
    print('These are the files you can select from for the next input: ' + str(choice))

    # this is where you finished, really this feature should be a tkinter file dialogue box alas...
    data_time = input('Please enter one of the file strings from the above choices')

    file_directory = home + '/' + 'pymoldatabase' + '/' + phrase + '/' + data_time

    choice = []
    for i in os.listdir(file_directory):

        if i != '.DS_Store':
            choice.append(os.path.splitext(i)[0])
    print('These are the files you can select from for the next input: ' + str(choice))

    main_branch = input('Choose from the above')
    # json_tree = objectpath.Tree(data[main_branch])

    file_directory = home + '/' + 'pymoldatabase' + '/' + phrase + '/' + data_time + '/' + main_branch + '.json'

    with open(file_directory, 'r') as datafile:
        data = json.load(datafile)

    if main_branch == 'moments':
        choice = []
        for i in data[main_branch]:
            for key, value in i.items():
                choice.append(key)
        print('These are the atoms you can select from in the next input: ' + str(choice))

        phrase = input('Please enter the list of atoms you want to see, i.e. H1, N2, H3')
        for i in data[main_branch]:
            for key, value in i.items():
                for ii in phrase.split(","):
                    print(ii)
                    if key == str(ii):
                        gui_moment_query(data, phrase.split(','))
                    break

    elif main_branch == 'coordinates':
        gui_coordinate_query(data)


    # result_tuple = tuple(json_tree.execute('$..units'))
    return


def pymoldat(file_directory):
    # get a dictionary describing the file hierarchy for the chosen file_directory
    file_dict = get_files(file_directory)

    # extract the coordinate information from file_directory
    coordinates = extract_coordinates(file_directory)

    # get an interactive data frame for console manipulation if so desired
    coords_dataframe = pd.read_json(coordinates['coordinates']['data frame'])

    # split up dataframe into each unique molecule
    connected_component = connected_components(coords_dataframe)

    # extract the moment information from file_directory
    moments = extract_moments(file_directory)

    # add information to database as json file
    add_to_database(coordinates, moments, file_directory)

    return


# class GUI(tkinter.Tk):
#
#     def __init__(self, parent, coords_dataframe):
#         tkinter.Tk.__init__(self, parent, coords_dataframe)
#         self.parent = parent
#         self.coords_dataframe = coords_dataframe
#         self.protocol("WM_DELETE_WINDOW", self.dest)
#         self.main()
#
#     def main(self, coords_dataframe):
#         self.fig = plt.figure()
#         self.fig = plt.figure(figsize=(5, 5))
#
#         self.frame = tkinter.Frame(self)
#         self.frame.pack(padx=15, pady=15)
#
#         self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
#         self.canvas.get_tk_widget().pack(side='top', fill='both')
#         self.canvas._tkcanvas.pack(side='top', fill='both', expand=1)
#
#         ax = Axes3D(self.fig)
#
#         # coordinates from data frame
#         x = coords_dataframe['x']
#         y = coords_dataframe['y']
#         z = coords_dataframe['z']
#
#         ax.scatter(x, y, z)
#
#         for a in range(len(x)):
#             ax.text(x[a], y[a], z[a], '%s' % (coords_dataframe.iloc[a]['label']), size=15, zorder=1, color='k')
#
#         self.toolbar = NavigationToolbar2TkAgg(self.canvas, self)
#         self.toolbar.update()
#         self.toolbar.pack()
#
#         self.btn = tkinter.Button(self, text='button', command=self.alt)
#         self.btn.pack(ipadx=250)
#
#     # directory navigator button (a la zortero)
#     def browse_button(self):
#         # Allow user to select a directory and store it in global var
#         # called folder_path
#         global file_dir
#         filename = filedialog.askdirectory()
#         file_dir.set(filename)
#         print(filename)
#
#         self.browse_button().update()
#         self.browse_button().pack(ipadx=250)
#
#
# if __name__ == "__main__":
#     app = GUI(None)
#     app.title('PyMolDat')
#     app.mainloop()


#
# class GUI:
#     def __init__(self, master):
#         self.master = master
#         self.mainframe = tkinter.Frame(self.master, bg='white')
#         self.mainframe.pack(fill=tkinter.BOTH, expand=True)
#
#     def gui_moment_query(self, mom_data, list_of_atoms):
#
#         num = 0
#         for item in mom_data["moments"]:
#             for k, v in item.items():
#                 for val in list_of_atoms:
#                     if k == val:
#                         for i, j in v.items():
#                             self.label_1 = tkinter.Label(root,
#                                                          text=i,
#                                                          width=10,
#                                                          anchor="w",
#                                                          font=("Arial 10 bold", 13)).grid(row=num,
#                                                                                           column=0,
#                                                                                           padx=10,
#                                                                                           sticky="ne")
#
#                             self.label_2 = tkinter.Label(root,
#                                                          text=j if i != "moments" else "\n".join(j),
#                                                          width=80,
#                                                          anchor="w",
#                                                          font=("Monaco", 10),
#                                                          justify='left').grid(row=num, column=1, padx=5)
#
#                             num += 1
#             # break
#         return
#
#
# if __name__ == "__main__":
#     root = tkinter.Tk()
#     obj = GUI(root)
#     root.mainloop()
#