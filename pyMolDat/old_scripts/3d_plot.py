import os
from pathlib import Path
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import tkinter
from tkinter import filedialog
import sys
import functions
import atom_database
import pandas as pd
import json
import numpy as np
import time

# home path
home = str(Path.home())

# time this script is ran
ts = time.gmtime()
time = time.strftime("%Y-%m-%d_%H:%M:%S", ts)

# directory where molecule files are stored
file_dir = os.path.join(home, 'Desktop/project/example_molecules/')

# function extracts atomic coordinates
information = functions.extract_info(file_dir)

# load bond details from database
database = atom_database.database

# add covalent radii information to each atom
chosen_atom = information['pyridine']

# work out the molecular connectivity
atom_pairing = functions.atomic_pairs(chosen_atom)
pair_list = atom_pairing['index'].tolist()

# preparing spatial coordinates for plotting
xs = chosen_atom["x"].tolist()
ys = chosen_atom["y"].tolist()
zs = chosen_atom["z"].tolist()
s = chosen_atom["atomic_number"].tolist()

# reshape to make coordinates of each point
df_points = chosen_atom[['x', 'y', 'z']]
array_of_points = df_points.values

# define plot size
fig = plt.figure(figsize=(5,5))

# use mplot3d Axes method
ax = Axes3D(fig)
scatter = ax.scatter(xs, ys, zs)

# add atomic labels to each atom
for a in range(len(xs)):
    ax.text(xs[a], ys[a], zs[a], '%s' % (chosen_atom.iloc[a]['label']), size=15, zorder=1, color='k')

# show plot
plt.show()


