import os

import pandas as pd

from lib import shared_lib
from shared_lib.data_info import DataInfo

from lib.parser import json_helper

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def make_json_df(filepath: str) -> pd.DataFrame:
    json_data = json_helper.textfile_into_json_list(filepath)
    json_data = json_data[-1]['data']
    json_df = pd.DataFrame.from_dict(json_data)

    return json_df


if __name__ == '__main__':
    data_dir = os.path.join(BASE_DIR, 'data', 'taipei_travel_network')
    data_info_path = os.path.join(data_dir, 'data_info.csv')
    data_info = DataInfo(data_info_path)

    input_filepath_list = data_info.get_download_filepath_list()
    output_filepath = data_info.get_structured_filepath()

    df_data = pd.DataFrame()

    for path in input_filepath_list:
        print('INFO: reading data from {}'.format(path))
        df_data = df_data.append(make_json_df(path), ignore_index=True)

    df_data.to_csv(output_filepath, index=False)
    print("INFO: data processed and saved in {}".format(output_filepath))
