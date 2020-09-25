import csv
import os
import pickle
import re
from difflib import SequenceMatcher
from typing import List


def get_tabular_data_dirpath(data_dir: str) -> List[str]:
    table_dirpath = []
    data_name_list = os.listdir(data_dir)

    for folder in data_name_list:
        check_folder = os.path.join(data_dir, folder)
        if os.path.isdir(check_folder):
            if 'structured' in os.listdir(check_folder):
                structured_table = os.path.join(data_dir, folder)
                table_dirpath.append(structured_table)

    return table_dirpath


def get_tabular_data_filepath(data_dir: str) -> List[str]:
    table_filepath = []

    for table_dirpath in get_tabular_data_dirpath(data_dir):
        check_folder = os.path.join(table_dirpath, 'structured')
        for filename in os.listdir(check_folder):
            if not (filename.startswith('.')):
                table_filepath.append(os.path.join(check_folder, filename))

    return table_filepath


def contain_chinese_character(string: str) -> bool:
    match = re.search('[\u4e00-\u9fff]+', string)
    if match:
        return True
    else:
        return False


def get_csv_column_name(filepath: str) -> List[str]:
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        column = next(reader)
    return column


def save_dictionary(dict_obj: dict, filepath: str) -> None:
    with open(filepath, 'wb') as f:
        pickle.dump(dict_obj, f)


def load_dictionary(filepath: str) -> dict:
    with open(filepath, 'rb') as f:
        dictionary = pickle.load(f)
        return dictionary


class UsedKeys:
    column_key_list = ['county_id', 'township_chinese_name', 'village_chinese_name']
    key_id = 'village_code'

    def compute_similarity(self, string_a: str, string_b: str) -> float:
        seq = SequenceMatcher(None, a=string_a, b=string_b)
        return seq.ratio()

    def compute_similarity_list(self, string: str, compare_list: List[str]) -> dict:
        key_compare = string.casefold()
        diff_value = map(lambda x: self.compute_similarity(a=key_compare, b=x), compare_list)
        diff_dict = dict(zip(compare_list, diff_value))

        return diff_dict

    def get_most_similar_keys(self, string: str, compare_list: List[str]) -> str:
        diff_dict = self.compute_similarity_list(string, compare_list)

        return max(diff_dict)

    def list_contain_used_key(self, check_list: List[str]) -> bool:
        if any((x in self.column_key_list for x in check_list)):
            return True
        else:
            return False
