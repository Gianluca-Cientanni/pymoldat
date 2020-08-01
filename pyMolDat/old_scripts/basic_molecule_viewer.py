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

# choose molecule to view (needs a GUI button here), needs to be a function embedded in tkinter!!

# preparing spatial coordinates for plotting
xs = chosen_atom["x"].tolist()
ys = chosen_atom["y"].tolist()
zs = chosen_atom["z"].tolist()
s = chosen_atom["atomic_number"].tolist()

# reshape to make coordinates of each point
df_points = chosen_atom[['x', 'y', 'z']]
array_of_points = df_points.values

# embedding matplotlib into tkinter, plotting (x,y,z) coords and vectors between atoms to represent bonding, dummy
# button feature also included, need to make label for each atomic coordinate

# define basic tkinter class for building frame


class E(tkinter.Tk):

    def __init__(self, parent):
        tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.protocol("WM_DELETE_WINDOW", self.dest)
        self.main()

    def main(self):
        self.fig = plt.figure()
        self.fig = plt.figure(figsize=(5, 5))

        self.frame = tkinter.Frame(self)
        self.frame.pack(padx=15, pady=15)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(side='top', fill='both')
        self.canvas._tkcanvas.pack(side='top', fill='both', expand=1)

        ax = Axes3D(self.fig)

        ax.scatter(xs, ys, zs)

        for a in range(len(xs)):
            ax.text(xs[a], ys[a], zs[a], '%s' % (chosen_atom.iloc[a]['label']), size=15, zorder=1, color='k')

        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self)
        self.toolbar.update()
        self.toolbar.pack()

        self.btn = tkinter.Button(self, text='button', command=self.alt)
        self.btn.pack(ipadx=250)


    # directory navigator button (a la zortero)
    def browse_button(self):
        # Allow user to select a directory and store it in global var
        # called folder_path
        global file_dir
        filename = filedialog.askdirectory()
        file_dir.set(filename)
        print(filename)

    def alt (self):
        print('end my suffering')
    def dest(self):
        self.destroy()
        sys.exit()

    # temporary molecule selector for information df



if __name__ == "__main__":
    app = E(None)
    app.title('Embedding in TK')
    app.mainloop()

