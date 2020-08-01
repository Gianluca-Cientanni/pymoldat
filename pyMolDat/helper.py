import pandas as pd
import os


class ExtractData:

    def open_file(self, file):
        file_obj = open(file, 'r')
        data = file_obj.readlines()
        molecule_name = os.path.basename(file)
        molecule_name = os.path.splitext(molecule_name)[-2]
        file_contents = {
            'name': molecule_name,
            'data': data
        }

        return file_contents

    def xyz(self, file):
        file_contents = ExtractData.open_file(self, file)
        



        return
