import os
from pathlib import Path
home = str(Path.home())
import pandas as pd
import glob
from pyparsing import alphanums, nums, printables, Word, Regex, alphas, Keyword, OneOrMore
import atom_database


# list molecule files: below is an example for arg:
file_dir = os.path.join(home, 'Desktop/project/example_molecules/')
file_list = os.listdir(file_dir)
clt_files = glob.glob(file_dir + '*.clt')
xyz_files = glob.glob(file_dir + '*.xyz')

# ignore numbers
# THIS WORKS ACCORDING TO ONLINE TEST REGEX THING
ignore = Regex('^\s*([A-Za-z]{1,2})\d*\s*$')

# empty dict to host df's
molecules_from_clt = {}
# define parsing tools

clt_parser = Word(alphas + nums) + Word(nums + '.' + nums) + Word(printables + '.' + printables) + \
             Word(printables + '.' + printables) + Word(printables + '.' + printables)

xyz_parser = Word(alphas) + Word(printables + '.' + printables) + Word(printables + '.' + printables) + \
             Word(printables + '.' + printables)

bohr = Keyword('Bohr')
angstrom = Keyword('Angstrom')
word = ~bohr + Word(alphas)
sentence = OneOrMore(word)
split_bohr = sentence('unit') + bohr + sentence('degree')
split_angrstom = Keyword('Units') + angstrom
unit_array = []

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
            res2 = split_angrstom.parseString(line)
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

        except Exception:
            print('not valid data line')

        # perform necessary unit conversions
        if len(unit_array) == 1:
            if unit_array[0] == 'Angstrom':
                continue
            else:
                df['x'] = df['x'] / 1.89
                df['y'] = df['y'] / 1.89
                df['z'] = df['z'] / 1.89
        # ambiguous case, just have to assume it's bohr but add line in summary file explaining ambiguity
        elif len(unit_array) == 2:
            print('ambiguous units')


    molecules_from_clt[str(molecule_name)] = df

# empty dict to host df's
molecules_from_xyz = {}

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

        except Exception:
            print('not valid data line')
    molecules_from_xyz[str(molecule_name)] = df_2

