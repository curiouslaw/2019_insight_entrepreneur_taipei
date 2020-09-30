import os
from urllib.parse import parse_qsl, urlparse

import pandas as pd

from lib import shared_lib
from shared_lib.data_info import DataInfo

from lib.parser import json_helper

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def selection_function(element):
    selected = element['data']['data']
    return selected


def structure_main_data(filepath: str) -> pd.DataFrame:
    json_data = json_helper.textfile_into_json_list(filepath)
    json_data = map(selection_function, json_data)
    json_df = json_helper.normalize_json_into_df(json_data)

    return json_df


def get_lat_long_from_url(url: str) -> dict:
    if url in ['TIMEOUT', 'N/A']:
        return {'latitude': None, 'longitude': None}

    query = urlparse(url).query
    parameter = dict(parse_qsl(query))
    latitude, longitude = parameter['q'].split(',')

    return {'latitude': latitude, 'longitude': longitude}


def get_id_from_url(url: str) -> int:
    parsed_url = url
    parsed_url = os.path.split(parsed_url)[-1]
    parsed_url = parsed_url.split('-')[-1]
    parsed_url = parsed_url.split('.')[0]

    return int(parsed_url)


def structure_lat_long_data(filepath: str) -> pd.DataFrame:
    json_data = json_helper.textfile_into_json_list(filepath)
    json_df = json_helper.normalize_json_into_df(json_data)

    json_df = json_df[~json_df['current_url'].str.contains('error')]

    data_df = pd.DataFrame()
    data_df['id'] = json_df['current_url'].apply(get_id_from_url)
    data_df['longitude'] = json_df['get_request'].apply(lambda x: get_lat_long_from_url(x)['longitude'])
    data_df['latitude'] = json_df['get_request'].apply(lambda x: get_lat_long_from_url(x)['latitude'])

    data_df.reset_index(drop=True, inplace=True)

    return data_df


if __name__ == '__main__':
    data_dir = os.path.join(BASE_DIR, 'data', 'taipei_shop_rent_price')
    data_info_path = os.path.join(data_dir, 'data_info.csv')
    data_info = DataInfo(data_info_path)

    input_dirpath = data_info.get_download_dirpath()
    output_filepath = data_info.get_structured_filepath()

    main_data_df = structure_main_data(os.path.join(input_dirpath, '591_xhr_responses.json'))
    long_lat_data_df = structure_lat_long_data(os.path.join(input_dirpath, '591_lat_long_lookup.json'))

    merged_df = pd.merge(main_data_df, long_lat_data_df, how='left', on='id')

    merged_df.to_csv(output_filepath, index=False)
    print("INFO: data processed and saved in {}".format(output_filepath))
