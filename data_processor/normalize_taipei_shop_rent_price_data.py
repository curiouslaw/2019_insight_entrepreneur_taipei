import os

import pandas as pd

from lib import shared_lib
from shared_lib.data_info import DataInfo

from data_processor.lib.data_keys import (
    contain_chinese_character,
    load_dictionary,
    UsedKeys
)

from lib.geocoding import GeoCoder
from lib.geolib_helper import get_shp_filepath

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)


def normalize_data(filepath: str, helper_dict: str) -> pd.DataFrame:
    data_df = pd.read_csv(filepath)

    # translate use generated google translate library if there is any chinese character
    if any([contain_chinese_character(x) for x in data_df.columns]):
        data_df = data_df.rename(columns=helper_dict)

    data_df['price'] = data_df['price'].apply(lambda x: int(x.replace(',', '')))

    return data_df


def attach_key_id_by_geocoding(data_df: pd.DataFrame, geo_coder: GeoCoder) -> pd.DataFrame:
    long_lat_tuple_lookup = list(zip(data_df['longitude'], data_df['latitude']))
    long_lat_tuple_dict = geo_coder.long_lat_tuple_to_dict_multiprocessing(long_lat_tuple_lookup)

    data_df['village_code'] = data_df.apply(
        lambda x: long_lat_tuple_dict.get((x['longitude'], x['latitude'])), axis=1)

    return data_df


if __name__ == '__main__':
    data_name = 'taipei_shop_rent_price'
    data_dir = os.path.join(BASE_DIR, 'data', data_name)
    data_info_path = os.path.join(data_dir, 'data_info.csv')
    helper_dict_filepath = os.path.join(CURRENT_DIR, 'data', 'chinese_english_column_helper_dict.pkl')
    village_shp_filepath = get_shp_filepath(os.path.join(BASE_DIR, 'data', 'taiwan_twd97_map_data_village'))

    data_info = DataInfo(data_info_path)

    input_filepath = data_info.get_structured_filepath()
    output_filepath = data_info.get_normalized_filepath()

    used_keys = UsedKeys()
    geo_coder = GeoCoder(village_shp_filepath, taipei_only=True)
    helper_dict = load_dictionary(helper_dict_filepath)

    data_df = normalize_data(input_filepath, helper_dict)
    print('INFO: do geocoding (on all cores), might take a while')
    data_df = attach_key_id_by_geocoding(data_df, geo_coder)

    # quick testing if there is key in the file before saving
    if used_keys.list_contain_key_id(data_df.columns):
        pass
    else:
        raise KeyError("list doesn't contain any used key")

    data_df.to_csv(output_filepath, index=False)
