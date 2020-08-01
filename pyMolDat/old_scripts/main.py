import functions
import os
from pathlib import Path

# home path
home = str(Path.home())

# location of calculations on which you want information extracted from
file_directory = os.path.join(home, 'Desktop/project/example_molecules/ISA/')

functions.pymoldat(file_directory)

# view the information in the database
functions.search_json()

#
# class GUI(tkinter.Tk):
#
#     def __init__(self, parent):
#         tkinter.Tk.__init__(self, parent)
#         self.parent = parent
#         self.protocol("WM_DELETE_WINDOW", self.dest)
#         self.main()
#
#     def main(self):
#         self.fig = plt.figure()
#         self.fig = plt.figure(figsize=(5, 5))
#
#         self.frame = tkinter.Frame(self)
#         self.frame.pack(padx=15, pady=15)
#
#         self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
#         self.canvas.get_tk_widget().pack(side='top', fill='both')
#         self.canvas._tkcanvas.pack(side='top', fill='both', expand=1)
#
#         ax = Axes3D(self.fig)
#
#         # coordinates from data frame
#         x = coords_dataframe['x']
#         y = coords_dataframe['y']
#         z = coords_dataframe['z']
#
#         ax.scatter(x, y, z)
#
#         for a in range(len(x)):
#             ax.text(x[a], y[a], z[a], '%s' % (coords_dataframe.iloc[a]['label']), size=15, zorder=1, color='k')
#
#         self.toolbar = NavigationToolbar2TkAgg(self.canvas, self)
#         self.toolbar.update()
#         self.toolbar.pack()
#
#         self.btn = tkinter.Button(self, text='button', command=self.alt)
#         self.btn.pack(ipadx=250)
#
#     # directory navigator button (a la zortero)
#     def browse_button(self):
#         # Allow user to select a directory and store it in global var
#         # called folder_path
#         global file_dir
#         filename = filedialog.askdirectory()
#         file_dir.set(filename)
#         print(filename)
#
#         self.browse_button().update()
#         self.browse_button().pack(ipadx=250)
#
#
# if __name__ == "__main__":
#     app = GUI(None)
#     app.title('PyMolDat')
#     app.mainloop()


# attempt at splitting data frame, not sure if I should keep this
# if len(connected_components) == 1:
#     print('there is only one molecule in this file')
# else:
#     for idx, value in enumerate(connected_components):
#         molecules['molecule %s' % (str(idx))] = value

# def callback():
#     name = fd.askopenfilename()
#     print(name)
#
#
# errmsg = 'Error!'
# tk.Button(text='File Open', command=callback).pack(fill='x')

# scrollbar = tk.Scrollbar(root)
# scrollbar.pack(side='right', fill='y')
#
# mylist = tk.Listbox(root, yscrollcommand=scrollbar.set)
# for line in range(100):
#     mylist.insert('end', "This is line number " + str(line))
#
# mylist.pack(side='left', fill='both')
# scrollbar.config(command=mylist.yview)
#
# scrollbar = tk.Scrollbar(root)
# scrollbar.pack(side='right', fill='y')
#
# listbox = tk.Listbox(root, yscrollcommand=scrollbar.set)
# for i in range(1000):
#     listbox.insert('end', str(i))
# listbox.pack(side='left', fill='both')
#
# scrollbar.config(command=listbox.yview)


# scrollbar = tk.Scrollbar(root)
# scrollbar.pack(side='right', fill='y')
#
# mylist = tk.Listbox(root, yscrollcommand=scrollbar.set)
# for line in range(100):
#     mylist.insert('end', "This is line number " + str(line))
#
# mylist.pack(side='left', fill='both')
# scrollbar.config(command=mylist.yview)
#
# scrollbar = tk.Scrollbar(root)
# scrollbar.pack(side='right', fill='y')
#
# listbox = tk.Listbox(root, yscrollcommand=scrollbar.set)
# for i in range(1000):
#     listbox.insert('end', str(i))
# listbox.pack(side='left', fill='both')
#
# scrollbar.config(command=listbox.yview)

# root = tkinter.Tk()
# root.title("PyMolDat")
# num = 0
# for item in moments_summary["moments"]:
#     for k, v in item.items():
#         for i, j in v.items():
#
#             tkinter.Label(root, text=i, width=10, anchor="w", font=("Arial 10 bold", 13)).grid(row=num,
#                                                                                     column=0, padx=10, sticky="ne")
#
#             tkinter.Label(root, text=j if i != "moments" else "\n".join(j), width=80, anchor="w",
#                      font=("Monaco", 10), justify='left').grid(
#                 row=num, column=1, padx=5)
#
#             num += 1
#     # break
# root.mainloop()
