import os
from pathlib import Path
import pandas as pd
import glob
import numpy as np
import json
from pyparsing import alphas, Word, Combine, nums, Keyword, OneOrMore, Optional
import atom_database
import functions
home = str(Path.home())

# extract info function is a general board-file method, the new way I think the software
# will work best is by running the 'basic_molecule_viewer' script for every file
# that is desired, rather than a full sweep. Hence, this function will simply find the .clt,
# and create the same df but return a single json object that will later be concatenated
# with the other json objects for different properties.

file_directory = os.path.join(home, 'Desktop/project/example_molecules/ISA/')

# list molecule files: below is an example for arg:
clt_files = glob.glob(file_directory + '*.clt')
xyz_files = glob.glob(file_directory + '*.xyz')

# empty dict to host df's
molecules_from_files = {}

# definitions of all the parsing tools used
float_parser = Combine(Optional('-') + Word(nums) + '.' + Word(nums))
coordinate_parser = OneOrMore(float_parser)

clt_parser = Word(alphas + nums) + coordinate_parser
xyz_parser = Word(alphas) + coordinate_parser

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
                print('No units given in this line')
            try:
                res2 = split_angstrom.parseString(line)
                if res2[1] == 'Angstrom':
                    unit_array.append(res2[1])

            except Exception:
                print('No units given in this line')

            try:
                parsed_lines = clt_parser.parseString(line)
                list_conversion = list(parsed_lines)
                df = df.append(
                    {'label': list_conversion[0][0], 'atomic_number': float(list_conversion[1]),
                     'x': float(list_conversion[2]), 'y': float(list_conversion[3]),
                     'z': float(list_conversion[4])}, ignore_index=True)

            except Exception:
                print('Not a valid data line')

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

    # split up dataframe into each unique molecule
    # connected_components = functions.connected_components(df)
    #
    # if len(connected_components) == 1:
    #     print('there is only one molecule in this file')
    # else:
    #     for i in connected_components:
    #         for j in i:


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

with open("coord_test.json", "w") as coord_json:
    json.dump(coord_data, coord_json, indent=4)
