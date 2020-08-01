import os
from pathlib import Path
import networkx as nx
import functions
import atom_database
import random as rand
import sys


# home path
home = str(Path.home())

# directory where molecule files are stored
file_dir = os.path.join(home, 'Desktop/project/example_molecules/')

# function extracts atomic coordinates
information = functions.extract_info(file_dir)

# load bond details from database
database = atom_database.database

# add covalent radii information to each atom
chosen_atom = information['H2O_n16_boat-a']

# work out the molecular contivity
atom_pairing = functions.atomic_pairs(chosen_atom)
pairs = atom_pairing['index'].tolist()

# start by going through pairs list sequentially
start_pair = pairs[0]

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

        if len(temp_array) > len(chosen_atom):
            break
    molecule_list.append(temp_array)

molecule_list = [list(item) for item in set(tuple(row) for row in molecule_list)]

# old code that doesn't work
#
# # first check if there is only 1 molecule in file
# # if len(pairs) == len(chosen_atom):
# #     print('There is only one molecule in this file')
# #     for i in range(len(chosen_atom)):
# #         molecule_list.append(i)
# #     sys.exit()
#
# # maximum number of molecules is given by number of atoms in file hence create upper limit
# for i in range(len(chosen_atom)):
#     molecule_list.append([])
#
# # add starting atom also
# molecule_list[0].append(start_pair[0])
#
#
# # select first atom, find pairs, perform non-duplicate check, next iteration
# for idx, i in enumerate(molecule_list):
#     for ii in i:
#         temp_array = []
#         # this loop finds what the selected ii atom is connected to in the pair list, and then adds it to temp array
#         for iii in pairs:
#             if ii == iii[0]:
#                 temp_array.append(iii[1])
#             if ii == iii[1]:
#                 temp_array.append(iii[0])
#         # this loop
#         for k in temp_array:
#             if k not in i:
#                 molecule_list[idx].append(k)
#
# # delete unnecessary lists
# index_list = []
# for i in molecule_list:
#     if len(i) == 0:
#         index_list.append(molecule_list.index(i))
#         if len(index_list) >= 1:
#             break
#
# molecule_list = molecule_list[:index_list[0]]
#
#
#
# # get pairs of this random number
# for i in pairs:
#     if i[0] == start_atom or i[1] == start_atom:
#         for j in i:
#             if j != start_atom:
#                 molecule_list[0].append(j)
#
# for ii in molecule_1:
#     for i in pairs:
#         if i[0] == ii or i[1] == ii:
#             for j in i:
#                 if j != ii:
#                     if j not in molecule_1:
#                         molecule_1.append(j)
#     if len(molecule_1) == len(pairs):
#         print('There is only one molecule in this file')
#         break
#
# if len(molecule_1) < len(pairs):
#     other_pairs = pairs
#     for i in other_pairs:
#         for j in molecule_1:
#             if j in molecule_1:
#                 other_pairs.pop(i)
#
#
#
# # [i for i in pairs if start_atom not in i]
# # get pairs of those connected to initial random number
#
#
# def search_list(list, int):
#
#     for i in list:
#         if i[0] == int or i[1] == int:
#             for j in i:
#                 if j != int and j not in molecule_1:
#                     molecule_1.append(int)
#                     set_list.add(int)
#         else:
#             continue
#
#     return()
#
#
# for ii in molecule_1:
#     for i in pairs:
#         if i[0] == ii or i[1] == ii:
#             for j in i:
#                 if j != ii:
#                     molecule_1.append(ii)
#                     print(molecule_1)
#                 else:
#                     print('this atom already is in molecule list')
#         else:
#             break
#
#
#
# for ii in molecule_1:
#     search_list(pairs, ii)
#
# # until i find a method that can use this to find Eulerian paths, i must resort to array manipulation
# # # create a graph
# # G = nx.Graph()
# #
# # # add nodes
# # G.add_nodes_from([i for i in range(len(pairs))])
# #
# # # add edges
# # G.add_edges_from(pairs)
# #
# # # check if network is Eulerian
# #
#
