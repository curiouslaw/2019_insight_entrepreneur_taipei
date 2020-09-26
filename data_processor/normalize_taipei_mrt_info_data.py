import os
import shutil

import pandas as pd

from lib import shared_lib
from shared_lib.data_info import DataInfo

from data_processor.lib.data_keys import (
    contain_chinese_character,
    load_dictionary,
    UsedKeys
)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)


def normalize_data(filepath: str, column_zh_en_dict: dict) -> pd.DataFrame:
    data_df = pd.read_csv(filepath)

    # translate use generated google translate library if there is any chinese character
    if any([contain_chinese_character(x) for x in data_df.columns]):
        data_df.rename(columns=column_zh_en_dict, inplace=True)

    data_df.rename(
        columns={
            'pit_stop': 'station_in',
            'outbound': 'station_out'
        }, inplace=True
    )

    return data_df


def attach_key_id_by_join(data_df: pd.DataFrame,
    station_index_lookup: pd.DataFrame) -> pd.DataFrame:
    # code the village_code for station_in
    data_df = pd.merge(
        data_df,
        station_index_lookup['village_code'],
        how='left', left_on='station_in', right_index=True
    )
    data_df.rename(columns={'village_code': 'station_in_village_code'}, inplace=True)

    # code the village_code for station_out
    data_df = pd.merge(
        data_df,
        station_index_lookup['village_code'],
        how='left', left_on='station_out', right_index=True
    )
    data_df.rename(columns={'village_code': 'station_out_village_code'}, inplace=True)

    return data_df


if __name__ == '__main__':
    data_name = 'taipei_mrt_info'
    data_dir = os.path.join(BASE_DIR, 'data', data_name)
    data_info_path = os.path.join(data_dir, 'data_info.csv')
    helper_dict_filepath = os.path.join(CURRENT_DIR, 'data', 'chinese_english_column_helper_dict.pkl')
    station_dimension_filepath = os.path.join(CURRENT_DIR, 'data', 'taipei_mrt_map_coordinate.csv')

    data_info = DataInfo(data_info_path)

    input_filepath_list = data_info.get_structured_filepath_list()
    output_dirpath = data_info.get_normalized_dirpath()

    used_keys = UsedKeys()
    helper_dict = load_dictionary(helper_dict_filepath)
    station_dimension_data = pd.read_csv(station_dimension_filepath)
    station_dimension_data.set_index('station_name', inplace=True)

    if os.path.isdir(output_dirpath):
        shutil.rmtree(output_dirpath)
        os.mkdir(output_dirpath)
    else:
        os.mkdir(output_dirpath)

    for path in input_filepath_list:
        print("INFO: processing data from {}".format(path))
        _filename = os.path.basename(path)
        _filename = _filename.split('.')[0]
        _filename, _month = _filename.split('_')

        _filename = 'taipei_mrt_passenger_statistic'

        _output_filepath = os.path.join(output_dirpath, '_'.join([_filename, _month]))
        _output_filepath = _output_filepath + '.csv'

        data_df = normalize_data(path, helper_dict)
        data_df = attach_key_id_by_join(data_df, station_dimension_data)

        # quick testing if there is key in the file before saving. We could also
        # check data sanity / quality in here
        if used_keys.list_contain_key_id(data_df.columns) or \
            any([used_keys.key_id in x for x in data_df.columns]):
            pass
        else:
            raise KeyError("list doesn't contain any used key")

        print('INFO: writing data into {}'.format(_output_filepath))
        data_df.to_csv(_output_filepath, index=False)
