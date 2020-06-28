import os
from pathlib import Path
import functions
import atom_database
import time
import json

# placeholders
coordinates = {'coordinates': {'coordinates': ['   atomic_number label         x         y         z',
   '0            8.0     O  0.000000  0.000000  0.000000',
   '1            1.0     H  0.953671  0.080487  0.000000',
   '2            1.0     H -0.322529  0.901078  0.000000',
   '3            7.0     N  0.000000  0.000000  0.000000',
   '4            1.0     H  0.016139 -1.016724  0.000000',
   '5            1.0     H  0.506990  0.319103  0.821659',
   '6            1.0     H  0.506990  0.319103 -0.821659'],
  'data frame': '{"atomic_number":{"0":8.0,"1":1.0,"2":1.0,"3":7.0,"4":1.0,"5":1.0,"6":1.0},"label":{"0":"O","1":"H","2":"H","3":"N","4":"H","5":"H","6":"H"},"x":{"0":0.0,"1":0.9536708571,"2":-0.3225285556,"3":0.0,"4":0.0161394392,"5":0.506989545,"6":0.506989545},"y":{"0":0.0,"1":0.0804865344,"2":0.9010779788,"3":0.0,"4":-1.0167244656,"5":0.3191031376,"6":0.3191031376},"z":{"0":0.0,"1":0.0,"2":0.0,"3":0.0,"4":0.0,"5":0.8216592381,"6":-0.8216592381}}',
  'errors': ['No errors'],
  'file': '/Users/gianluca/Desktop/project/example_molecules/ISA/',
  'units': 'Bohr'}}
moments = {'moments': [{'N1': {'atom': 'N1',
    'file': '/Users/gianluca/Desktop/project/example_molecules/ISA/OUT/NH3_ISA-GRID.mom',
    'moments': ['          Q0        Q1        Q2        Q3        Q4',
     '0  -1.064525 -0.000004  0.340138  0.000004  0.047612',
     '1s       NaN -0.105246 -0.000006 -0.208369  0.000035',
     '1c       NaN  0.036201 -0.000002 -0.482417  0.000005',
     '2s       NaN       NaN -0.454872 -0.000004  0.734665',
     '2c       NaN       NaN  0.383145  0.000003  0.979878',
     '3s       NaN       NaN       NaN -0.105177 -0.000029',
     '3c       NaN       NaN       NaN -0.097678  0.000015',
     '4s       NaN       NaN       NaN       NaN  0.454980',
     '4c       NaN       NaN       NaN       NaN -0.005097'],
    'rank': '4',
    'scheme': 'NH3_ISA-GRID',
    'type': 'N'}},
  {'H3': {'atom': 'H3',
    'file': '/Users/gianluca/Desktop/project/example_molecules/ISA/OUT/NH3_ISA-GRID.mom',
    'moments': ['          Q0        Q1        Q2        Q3        Q4',
     '0   0.353619 -0.000000  0.022593 -0.000000  0.016054',
     '1s       NaN -0.020984 -0.000000 -0.010761 -0.000000',
     '1c       NaN -0.009221 -0.000000  0.007970 -0.000000',
     '2s       NaN       NaN -0.016711 -0.000000  0.015248',
     '2c       NaN       NaN  0.016692 -0.000000 -0.009410',
     '3s       NaN       NaN       NaN  0.003688 -0.000001',
     '3c       NaN       NaN       NaN  0.025270 -0.000001',
     '4s       NaN       NaN       NaN       NaN  0.005240',
     '4c       NaN       NaN       NaN       NaN  0.010030'],
    'rank': '4',
    'scheme': 'NH3_ISA-GRID',
    'type': 'HN'}},
  {'H4': {'atom': 'H4',
    'file': '/Users/gianluca/Desktop/project/example_molecules/ISA/OUT/NH3_ISA-GRID.mom',
    'moments': ['          Q0        Q1        Q2        Q3        Q4',
     '0   0.355424  0.013163  0.011901  0.007411 -0.012933',
     '1s       NaN -0.012893 -0.004149  0.015750  0.008439',
     '1c       NaN  0.012746 -0.005790  0.003681  0.013541',
     '2s       NaN       NaN -0.022555  0.004799  0.003075',
     '2c       NaN       NaN  0.017714  0.020630  0.003709',
     '3s       NaN       NaN       NaN -0.004436  0.008474',
     '3c       NaN       NaN       NaN -0.002779  0.008116',
     '4s       NaN       NaN       NaN       NaN -0.001628',
     '4c       NaN       NaN       NaN       NaN  0.006952'],
    'rank': '4',
    'scheme': 'NH3_ISA-GRID',
    'type': 'HN'}},
  {'H5': {'atom': 'H5',
    'file': '/Users/gianluca/Desktop/project/example_molecules/ISA/OUT/NH3_ISA-GRID.mom',
    'moments': ['          Q0        Q1        Q2        Q3        Q4',
     '0   0.355421 -0.013164  0.011902 -0.007411 -0.012934',
     '1s       NaN -0.012894  0.004148  0.015751 -0.008440',
     '1c       NaN  0.012746  0.005790  0.003681 -0.013543',
     '2s       NaN       NaN -0.022556 -0.004800  0.003076',
     '2c       NaN       NaN  0.017715 -0.020631  0.003710',
     '3s       NaN       NaN       NaN -0.004436 -0.008476',
     '3c       NaN       NaN       NaN -0.002779 -0.008116',
     '4s       NaN       NaN       NaN       NaN -0.001628',
     '4c       NaN       NaN       NaN       NaN  0.006953'],
    'rank': '4',
    'scheme': 'NH3_ISA-GRID',
    'type': 'HN'}},
  {'N1': {'atom': 'N1',
    'file': '/Users/gianluca/Desktop/project/example_molecules/ISA/OUT/NH3_ISA.mom',
    'moments': ['          Q0        Q1        Q2        Q3        Q4',
     '0  -1.064533 -0.000007  0.335373 -0.000034 -0.017676',
     '1s       NaN -0.130782 -0.000007 -0.990753  0.000019',
     '1c       NaN  0.044770 -0.000006 -1.404081  0.000034',
     '2s       NaN       NaN -0.451296 -0.000067  0.804011',
     '2c       NaN       NaN  0.378061 -0.000150  0.911492',
     '3s       NaN       NaN       NaN -0.096208  0.000019',
     '3c       NaN       NaN       NaN -0.714299  0.000027',
     '4s       NaN       NaN       NaN       NaN  0.441683',
     '4c       NaN       NaN       NaN       NaN  0.107567'],
    'rank': '4',
    'scheme': 'NH3_ISA',
    'type': 'N'}},
  {'H3': {'atom': 'H3',
    'file': '/Users/gianluca/Desktop/project/example_molecules/ISA/OUT/NH3_ISA.mom',
    'moments': ['          Q0        Q1        Q2        Q3        Q4',
     '0   0.353608 -0.000001  0.008389 -0.000003  0.014938',
     '1s       NaN -0.020138  0.000001 -0.008956  0.000011',
     '1c       NaN -0.011952 -0.000002 -0.013778  0.000006',
     '2s       NaN       NaN -0.042028  0.000005 -0.002432',
     '2c       NaN       NaN  0.015945  0.000000 -0.035642',
     '3s       NaN       NaN       NaN  0.005689 -0.000000',
     '3c       NaN       NaN       NaN -0.000196  0.000006',
     '4s       NaN       NaN       NaN       NaN -0.014408',
     '4c       NaN       NaN       NaN       NaN  0.016101'],
    'rank': '4',
    'scheme': 'NH3_ISA',
    'type': 'HN'}},
  {'H4': {'atom': 'H4',
    'file': '/Users/gianluca/Desktop/project/example_molecules/ISA/OUT/NH3_ISA.mom',
    'moments': ['          Q0        Q1        Q2        Q3        Q4',
     '0   0.355543  0.014180  0.026525  0.004023 -0.017858',
     '1s       NaN -0.011466  0.015769 -0.009499  0.004331',
     '1c       NaN  0.013083  0.007198 -0.009804  0.013932',
     '2s       NaN       NaN -0.018736 -0.004213 -0.015855',
     '2c       NaN       NaN  0.025705  0.002607 -0.024676',
     '3s       NaN       NaN       NaN -0.002677  0.013785',
     '3c       NaN       NaN       NaN -0.006283  0.005618',
     '4s       NaN       NaN       NaN       NaN -0.010890',
     '4c       NaN       NaN       NaN       NaN  0.012265'],
    'rank': '4',
    'scheme': 'NH3_ISA',
    'type': 'HN'}},
  {'H5': {'atom': 'H5',
    'file': '/Users/gianluca/Desktop/project/example_molecules/ISA/OUT/NH3_ISA.mom',
    'moments': ['          Q0        Q1        Q2        Q3        Q4',
     '0   0.355539 -0.014183  0.026524 -0.004026 -0.017865',
     '1s       NaN -0.011466 -0.015768 -0.009489 -0.004317',
     '1c       NaN  0.013084 -0.007197 -0.009803 -0.013921',
     '2s       NaN       NaN -0.018737  0.004210 -0.015864',
     '2c       NaN       NaN  0.025709 -0.002620 -0.024688',
     '3s       NaN       NaN       NaN -0.002672 -0.013795',
     '3c       NaN       NaN       NaN -0.006286 -0.005612',
     '4s       NaN       NaN       NaN       NaN -0.010898',
     '4c       NaN       NaN       NaN       NaN  0.012263'],
    'rank': '4',
    'scheme': 'NH3_ISA',
    'type': 'HN'}}]}


# home path
home = str(Path.home())

# time this script is ran
ts = time.gmtime()
time = time.strftime("%Y_%m_%d_%H;%M", ts)

# location of directory
file_dir = os.path.join(home, 'Desktop/project/example_molecules/ISA')
file_list = os.listdir(file_dir)

# create database
database_dir = home + '/pymoldatabase'

try:
    os.mkdir(database_dir)

except FileExistsError:
    print('Database already exists')

### BASIC - look at file extensions and understand the file

file_dict = {}

coordinate_files = []

moment_files = []

energy_files = []

# get all files in file hierarchy and sort into each file type
for root, dirs, files in os.walk(file_dir):
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

file_name = os.path.basename(file_dir)

# new directory for this molecule in DB
try:
    os.mkdir(database_dir + '/' + file_name)

except FileExistsError:
    print('This molecule already exists')

new_folder = database_dir + '/' + file_name + '/' + time

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

