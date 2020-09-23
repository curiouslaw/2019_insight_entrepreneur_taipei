from builtins import KeyError
import os
from typing import Union

import geopandas as gpd
import pandas as pd

from lib.pandas_helper import change_on_multiple_columns


def try_fix_encoding(string: str) -> str:
    if string:
        try:
            return string.encode('latin1').decode('utf8')
        except Exception:
            return string
    else:
        return ""


def try_translate(dictionary: dict, string: str) -> str:
    if match := dictionary.get(string):
        return match
    else:
        return string


def find_helper(lookup: str, string: str) -> Union[str, bool]:
    if lookup in string:
        return string.find(lookup)
    else:
        return False


def get_shp_filepath(data_dirpath: str) -> str:
    os_walk = os.walk(data_dirpath)

    for dirpath, _, file_list in [x for x in os_walk]:
        for filename in file_list:
            if filename.endswith('.shp'):
                return os.path.join(dirpath, filename)

    raise KeyError('shp file that would be used for reference is not found')


def normalize_column_name(column_name: str) -> str:
    full_name_dict = {
        'county': 'county',
        'town': 'township',
        'vill': 'village'
    }

    if (split_index := find_helper('id', column_name)):
        return try_translate(full_name_dict, column_name[:split_index]) + '_' + 'id'
    elif (split_index := find_helper('code', column_name)):
        return try_translate(full_name_dict, column_name[:split_index]) + '_' + 'code'
    elif (split_index := find_helper('name', column_name)):
        return try_translate(full_name_dict, column_name[:split_index]) + '_' + 'chinese_name'
    elif (split_index := find_helper('eng', column_name)):
        return try_translate(full_name_dict, column_name[:split_index]) + '_' + 'english_name'
    else:
        return column_name


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)


if __name__ == '__main__':
    data_dir = os.path.join(BASE_DIR, 'data')

    county_data_dirpah = os.path.join(data_dir, 'taiwan_twd97_map_data_county')
    town_data_dirpath = os.path.join(data_dir, 'taiwan_twd97_map_data_township')
    village_data_dirpath = os.path.join(data_dir, 'taiwan_twd97_map_data_village')

    filename = 'area_dimension_table.csv'
    output_filepath_list = [
        os.path.join(CURRENT_DIR, 'data', filename),
        os.path.join(data_dir, 'normalized-data_warehouse', filename),  # to make things easier to lookup for non-technical user
    ]

    county_shp = gpd.read_file(get_shp_filepath(county_data_dirpah))
    town_shp = gpd.read_file(get_shp_filepath(town_data_dirpath))
    village_shp = gpd.read_file(get_shp_filepath(village_data_dirpath))

    # delete geometry data, make into simple df column with dimension data
    county_df = county_shp.drop('geometry', axis=1)
    town_df = town_shp.drop('geometry', axis=1)
    village_df = village_shp.drop('geometry', axis=1)

    # fix encoding on some bad chinese character encoding
    change_on_multiple_columns(town_df, lambda x: 'name' in x.casefold(), try_fix_encoding)
    change_on_multiple_columns(county_df, lambda x: 'name' in x.casefold(), try_fix_encoding)
    change_on_multiple_columns(village_df, lambda x: 'name' in x.casefold(), try_fix_encoding)

    # make sure if id is unique, use for later matching
    assert not any(county_df['COUNTYCODE'].duplicated()), 'duplicated county id_code detected, please check the source data'
    assert not any(town_df['TOWNCODE'].duplicated()), 'duplicated county id_code detected, please check the source data'
    assert not any(village_df['VILLCODE'].duplicated()), 'duplicated county id_code detected, please check the source data'

    merged_df = village_df
    merged_df = pd.merge(merged_df, town_df, how='inner')
    merged_df = pd.merge(merged_df, county_df, how='inner')

    merged_df.columns = map(lambda x: x.lower(), merged_df.columns)
    merged_df.columns = map(normalize_column_name, merged_df.columns)

    for filepath in output_filepath_list:
        merged_df.to_csv(filepath, index=False)
