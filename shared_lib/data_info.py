import csv
import os
from typing import List, Union
from builtins import FileNotFoundError, KeyError, IndexError


class DataInfo:
    """Class object to interact with data_info.csv in the data project

        Args:
            filepath (str): data_info.csv filepath

        Method:
            get_info    search and return what data_attribute info, if not found return False.
    """
    def __init__(self, filepath: str):
        if not os.path.isfile(filepath):
            raise FileNotFoundError("data_info.csv is not found in {}".format(filepath))
        
        self.filepath = filepath

    def get_info(self, data_attribute: str):
        """Read data_info.csv and try to find data attribute

        Args:
            data_attribute (str): data attribute that want to be found

        Returns:
            - if data_attribute found, return the info
            - if data_attribute not found, return False (bool)
        """
        with open(self.filepath, 'r') as f:
            for row in csv.reader(f, delimiter=','):
                try:
                    if row[0] == data_attribute:
                        return row[1]
                except IndexError:
                    pass

            # if data attribute not found
            return False

    def get_info_force(self, data_attribute: str):
        if not (data_info := self.get_info(data_attribute)):
            raise KeyError("data_info.csv does not contain {} data".format(data_attribute))

        return data_info

    def get_info_contain(self, data_attribute: str) -> Union[bool, List[str]]:
        """Read through all of the data_info.csv and get the data attribute that ocntain some string.

        Args:
            data_attribute (str): string to be search on

        Returns:
            Union[str, List[str]]: the matched data_attribute or False if not found anything
        """
        data_info = []
        with open(self.filepath, 'r') as f:
            for row in csv.reader(f, delimiter=','):
                try:
                    if data_attribute in row[0]:
                        data_info.append(row[1])
                except IndexError:
                    pass

        if data_info:
            return data_info
        else:
            return False

    def get_info_contain_force(self, data_attribute: str) -> List[str]:
        if not (data_info := self.get_info_contain(data_attribute)):
            raise KeyError("data_info.csv does not contain {} data".format(data_attribute))

        return data_info

    def get_download_filepath(self) -> Union[str, List[str]]:
        """Method for getting the download data filepath / list of filepath
        from the data_info.csv. Would always try to look for single filepath
        if possible.

        Raises:
            KeyError: [description]

        Returns:
            Union[str, List[str]]: would return filepath if possible, but
        """
        if (filepath := self.get_info('download_filepath')):
            return filepath
        if (dirpath := self.get_info('download_filepath')):
            return os.listdir(dirpath)
        raise KeyError("data info does't contain download_filepath or download_dirpath attribute.")
