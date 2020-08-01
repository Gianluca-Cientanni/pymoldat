import os
from pathlib import Path
import pandas as pd
import glob
import numpy as np
import json
import atom_database
home = str(Path.home())

file_directory = os.path.join(home, 'Desktop/project/pyMolDat/scripts/coord_test.json')

open_json = json.load(open(file_directory))


