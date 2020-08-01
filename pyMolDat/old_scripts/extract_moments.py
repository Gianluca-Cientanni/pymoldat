import os
from pathlib import Path
import pandas as pd
import glob
import numpy as np
import json
from pyparsing import alphas, Word, nums, Keyword, Combine, Optional, OneOrMore
home = str(Path.home())

# this function extracts the multipole moments from the relevent .mom file
file_directory = os.path.join(home, 'Desktop/project/example_molecules/ISA')

mom_files = []
for root, dirs, files in os.walk(file_directory):
    for i in files:
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

regex_float = r'(^[+-]?\d+(?:\.\d+)?(?:[eE][+-]\d+)?$)'

# error array for error information in json
error_array = []

# df type array to store info for json
df_array = []

# coordinate array
coords = []

# atom array
atom = []

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

        array = []
        tot = []
        cum_sum = []

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

                'scheme': mom_name,
                'type': df['type'][idx],
                'rank': df['rank'][idx],
                'moments': moments_string,
                'file': elem

        }
        json_result['moments'].append({kk: mom_data})

    with open("mom_test.json", "w") as mom_json:
        json.dump(json_result, mom_json, indent=4)
