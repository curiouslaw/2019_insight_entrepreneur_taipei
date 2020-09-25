import os

import pandas as pd

from lib import shared_lib
from shared_lib.data_info import DataInfo

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


if __name__ == '__main__':
    data_dir = os.path.join(BASE_DIR, 'data', 'taipei_income_by_district')
    data_info_path = os.path.join(data_dir, 'data_info.csv')
    data_info = DataInfo(data_info_path)

    input_filepath_list = data_info.get_download_filepath_list()
    output_filepath = data_info.get_structured_filepath()

    df_data = pd.DataFrame()

    for path in input_filepath_list:
        print('INFO: processing data from {}'.format(path))
        _county_id = os.path.basename(path).split('.')[0].split('-')[1]
        _read_csv = pd.read_csv(path)
        _read_csv['county_id'] = _county_id
        df_data = df_data.append(_read_csv, ignore_index=True)

    print('INFO: saving data to {}'.format(output_filepath))
    df_data.to_csv(output_filepath, index=False)
