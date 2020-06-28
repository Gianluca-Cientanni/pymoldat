import os
from pathlib import Path
import functions
import atom_database
import time
import json
from pyparsing import alphas, Word, Regex, printables, alphanums, nums, Keyword, OneOrMore

# home path
home = str(Path.home())

# time this script is ran
ts = time.gmtime()
time = time.strftime("%Y-%m-%d_%H:%M:%S", ts)

# directory where molecule files are stored
file_dir = os.path.join(home, 'Desktop/project/example_molecules/')

# function extracts atomic coordinates
information = functions.extract_position(file_dir)

# load bond details from database
database = atom_database.database

# add covalent radii information to each atom
chosen_atom = information['pyridine']

# work out the molecular connectivity
atom_pairing = functions.atomic_pairs(chosen_atom)
pair_list = atom_pairing['index'].tolist()

# location of directory
file_dir = os.path.join(home, 'Desktop/project/example_molecules/')
file_list = os.listdir(file_dir)

coord_string = chosen_atom.to_string().splitlines()

data = {

    'Header Information': [{

        'Time of calculation': time,
        'Name of Molecule': 'pyridine'

    }],

    'Coordinates': coord_string

}

with open("coord_test.json", "w") as summary_file:
    json.dump(data, summary_file, indent=4)


