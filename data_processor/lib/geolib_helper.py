import os
from builtins import KeyError

import geopandas as gpd

from .pandas_helper import (
    find_helper,
    try_get_dict,
    try_fix_encoding,
    change_on_multiple_columns
)


def get_shp_filepath(data_dirpath: str) -> str:
    os_walk = os.walk(data_dirpath)

    for dirpath, _, file_list in [x for x in os_walk]:
        for filename in file_list:
            if filename.endswith('.shp'):
                return os.path.join(dirpath, filename)

    raise KeyError('shp file that would be used for reference is not found')


def normalize_gov_shp_data_column_name(column_name: str) -> str:
    column_name = column_name.lower()

    full_name_dict = {
        'county': 'county',
        'town': 'township',
        'vill': 'village'
    }

    if (split_index := find_helper('id', column_name)):
        return try_get_dict(full_name_dict, column_name[:split_index]) + '_' + 'id'
    elif (split_index := find_helper('code', column_name)):
        return try_get_dict(full_name_dict, column_name[:split_index]) + '_' + 'code'
    elif (split_index := find_helper('name', column_name)):
        return try_get_dict(full_name_dict, column_name[:split_index]) + '_' + 'chinese_name'
    elif (split_index := find_helper('eng', column_name)):
        return try_get_dict(full_name_dict, column_name[:split_index]) + '_' + 'english_name'
    else:
        return column_name


def load_normalize_gov_shp_data(filepath: str):
    gdf = gpd.read_file(filepath)
    change_on_multiple_columns(gdf, lambda x: 'name' in x.casefold(), try_fix_encoding)
    gdf.columns = map(normalize_gov_shp_data_column_name, gdf.columns)

    return gdf
