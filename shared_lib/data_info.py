import builtins
import csv


class DataInfo:
    """Class object to interact with data_info.csv in the data project

        Args:
            filepath (str): data_info.csv filepath
    """
    def __init__(self, filepath: str):

        self.filepath = filepath

    def get_info(self, data_attribute: str):
        with open(self.filepath, 'r') as f:
            for row in csv.reader(f, delimiter=','):
                if row[0] == data_attribute:
                    return row[1]

            raise builtins.KeyError("{} not found in {}".format(
                data_attribute, self.filepath
            ))
