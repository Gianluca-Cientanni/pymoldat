import os
from pathlib import Path
home = str(Path.home())
from pyparsing import alphas, Word, Regex, tokenMap, Combine, printables


# converts .txt/.pdb into ordered .xyz files, will be a function for functions.py to call at beginning of viewer.
file_dir = os.path.join(home, 'Desktop/project/example_molecules/')
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
    new_file_name = os.path.splitext(txt[elem])[0] + '.xyz'
    new_file = open(new_file_name, 'w')
    new_file.write(str(len(full_data_set)) + '\n' + os.path.splitext(txt[elem])[0] + '\n' + '\n' + '\n')

    # add atomic coords and elements
    for i in full_data_set:
        new_file.write(i[0] + '     ' + i[1] + '     ' + i[2] + '     ' + i[3])
        new_file.write('\n')
