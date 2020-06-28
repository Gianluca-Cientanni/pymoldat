import os
from pathlib import Path
home = str(Path.home())
import pandas as pd
from pyparsing import alphanums, nums, printables, Word
from pyparsing import alphas, Word, Regex, tokenMap, Combine, printables
import json
import functions


# extend JSON encoder to be able to seralise Dataframes
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'to_json'):
            return obj.to_json(orient='records')
        return json.JSONEncoder.default(self, obj)


# define where database is stored
database_dir = os.path.join(home, 'Desktop/project/pyMolDat/scripts/atoms.f90')


# create empty dataframe to host data, Grimme VDW radius is used
database = pd.DataFrame(data={'symbol': [], 'element': [], 'atomic_number': [], 'weight': [], 'slater_radii': [],
                        'vdw_radii': [], 'c6_coefficient': [], 'cov_rad': []})

# define how to read floats (pos + neg)
float_definition = Regex(r'[+-]?\d+\.\d*')

# define how we will parse the database
parser_1 = Word(alphas) + '(' + Word(nums) + ')' + '=' + Word(alphas) + '(' + "'" + Word(alphas) + "'" +\
                 ',' + "'" + Word(alphas) + "'" + ',' + float_definition + ',' + float_definition + ',' + Word(alphas) + ',' \
                 + float_definition + ',' + float_definition + ',' + float_definition + ',' + float_definition + ')'

# parser 2 and 3 account for slight variations in database file that aren't easily parsable
parser_2 = Word(alphas) + '(' + Word(nums) + ')' + '=' + Word(alphas) + '(' + "'" + Word(alphas) + "'" +\
                 ',' + "'" + Word(alphas) + "'" + ',' + float_definition + ',' + float_definition + ',' + float_definition + ',' \
                 + float_definition + ',' + float_definition + ',' + float_definition + ',' + float_definition + ')'


parser_3 = Word(alphas) + '(' + Word(nums) + ')' + '=' + Word(alphas) + '(' + "'" + Word(alphas) + "'" +\
                 ',' + "'" + Word(alphas) + "'" + ',' + float_definition + ',' + float_definition + ',' + Word(alphas) + ',' \
                 + float_definition + ',' + float_definition + ',' + float_definition + ',' + Word(nums) + ')'

# open the database file and read indivdual lines
file_object = open(database_dir, 'r')
lines = file_object.readlines()

# parse lines for data extraction, cov_rad is kept in Bohr and converted to Angstroms later
for line in lines:

    try:
        # parse for information
        parsed_line = parser_1.parseString(line)
        list_conversion = list(parsed_line)
        list_conversion[27] = float(list_conversion[27])
        database = database.append(
            {'symbol': list_conversion[8], 'element': list_conversion[12], 'atomic_number': int(list_conversion[2]),
             'weight': float(list_conversion[17]), 'slater_radii': float(list_conversion[21]),
             'vdw_radii': float(list_conversion[23]), 'c6_coefficient': float(list_conversion[25]),
             'cov_rad': float(list_conversion[27])}, ignore_index=True)

    except Exception:
        print('invalid data line')

    try:
        parsed_line = parser_2.parseString(line)
        list_conversion = list(parsed_line)
        list_conversion[27] = float(list_conversion[27])
        database = database.append(
            {'symbol': list_conversion[8], 'element': list_conversion[12], 'atomic_number': int(list_conversion[2]),
             'weight': float(list_conversion[17]), 'slater_radii': float(list_conversion[21]),
             'vdw_radii': float(list_conversion[23]), 'c6_coefficient': float(list_conversion[25]),
             'cov_rad': float(list_conversion[27])}, ignore_index=True)

    except Exception:
        print('invalid data line')

    try:
        parsed_line = parser_3.parseString(line)
        list_conversion = list(parsed_line)
        list_conversion[27] = float(list_conversion[27])
        database = database.append(
            {'symbol': list_conversion[8], 'element': list_conversion[12], 'atomic_number': int(list_conversion[2]),
             'weight': float(list_conversion[17]), 'slater_radii': float(list_conversion[21]),
             'vdw_radii': float(list_conversion[23]), 'c6_coefficient': float(list_conversion[25]),
             'cov_rad': float(list_conversion[27])}, ignore_index=True)

    except Exception:
        print('invalid data line')
