import os

import geopandas as gpd
import pandas as pd

from lib.pandas_helper import (
    change_on_multiple_columns,
    try_fix_encoding
)
from lib.geolib_helper import get_shp_filepath, normalize_gov_shp_data_column_name


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
    assert not any(county_df.duplicated('COUNTYCODE')), 'duplicated county id_code detected, please check the source data'
    assert not any(town_df.duplicated('TOWNCODE')), 'duplicated county id_code detected, please check the source data'
    assert not any(village_df.duplicated('VILLCODE')), 'duplicated county id_code detected, please check the source data'

    merged_df = village_df
    merged_df = pd.merge(merged_df, town_df, how='left')
    merged_df = pd.merge(merged_df, county_df, how='left')

    merged_df.columns = map(normalize_gov_shp_data_column_name, merged_df.columns)

    for filepath in output_filepath_list:
        merged_df.to_csv(filepath, index=False)
