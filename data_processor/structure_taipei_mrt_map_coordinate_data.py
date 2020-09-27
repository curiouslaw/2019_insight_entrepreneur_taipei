import os

import pandas as pd

from lib import shared_lib
from shared_lib.data_info import DataInfo
from shapely.geometry.point import Point

from lib.geolib_helper import get_shp_filepath
from lib.geocoding import GeoCoder

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)


if __name__ == '__main__':
    data_dir = os.path.join(BASE_DIR, 'data', 'taipei_mrt_map_coordinate')
    data_info_path = os.path.join(data_dir, 'data_info.csv')
    data_info = DataInfo(data_info_path)
    shp_filepath = get_shp_filepath(os.path.join(BASE_DIR, 'data', 'taiwan_twd97_map_data_village'))

    input_filepath_list = data_info.get_download_filepath_list()
    output_filepath = data_info.get_structured_filepath()
    extra_output_filepath = os.path.join(CURRENT_DIR, 'data', 'taipei_mrt_map_coordinate.csv')

    geo_coder = GeoCoder(shp_filepath)

    df_data = pd.DataFrame()

    # actually this is the case where no structural need to be included, 
    # usually in real case we usually just directly do normalization (next step).
    for path in input_filepath_list:
        print('INFO: processing data from {}'.format(path))
        _read_csv = pd.read_csv(path)
        _read_csv.columns = map(lambda x: x.lower(), _read_csv.columns)
        df_data = df_data.append(_read_csv, ignore_index=True)

    assert not any(df_data.duplicated('station_name'))

    print('INFO: add village_code from reverse geocoding, might take a while...')
    long_lat_tuple_lookup = list(zip(df_data['longitude'], df_data['latitude']))
    long_lat_tuple_dict = geo_coder.long_lat_tuple_to_dict_multiprocessing(long_lat_tuple_lookup)

    df_data['village_code'] = df_data.apply(lambda x: long_lat_tuple_dict.get((x['longitude'], x['latitude'])), axis=1)

    # get all case, with suffix or non-suffix case
    df_data['station_name'] = df_data['station_name'].apply(lambda x: x[:-1] if x[-1] == '站' else x)
    df_data_suffix = df_data.copy()
    df_data_suffix['station_name'] = df_data_suffix['station_name'] + '站' 

    df_data = df_data.append(df_data_suffix, ignore_index=True)

    print('INFO: saving data to {}'.format(output_filepath))
    df_data.to_csv(output_filepath, index=False)

    print('INFO: also saving data to {}'.format(extra_output_filepath))
    df_data.to_csv(extra_output_filepath, index=False)
