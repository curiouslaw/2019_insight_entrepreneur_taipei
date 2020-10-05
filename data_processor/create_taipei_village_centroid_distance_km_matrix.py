import os
import pandas as pd

from lib.geolib_helper import get_shp_filepath, load_normalize_gov_shp_data

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)


if __name__ == '__main__':
    data_dir = os.path.join(BASE_DIR, 'data')
    village_shp_filepath = get_shp_filepath(os.path.join(BASE_DIR, 'data', 'taiwan_twd97_map_data_village'))

    filename = 'taipei_village_centroid_distance_km_matrix.csv'
    output_filepath_list = [
        os.path.join(CURRENT_DIR, 'data', filename),
        os.path.join(data_dir, 'normalized-data_warehouse', filename)
    ]

    output_filepath = os.path.join(CURRENT_DIR, 'data', 'taipei_village_centroid_distance_km_matrix.csv')

    villages_shp_gdp = load_normalize_gov_shp_data(village_shp_filepath)

    taipei_area_only = villages_shp_gdp[villages_shp_gdp['county_chinese_name'] == '臺北市']
    taipei_area_only.set_index('village_code', inplace=True)

    taipei_area_only['centroid'] = taipei_area_only.centroid

    distance_km_matrix_dict = {}
    for index, row in taipei_area_only.iterrows():
        _distance_km_dict = taipei_area_only['centroid'].apply(lambda x: row['centroid'].distance(x) * 111).to_dict()
        distance_km_matrix_dict = {**distance_km_matrix_dict, **{index: _distance_km_dict}}

    distance_km_matrix_df = pd.DataFrame(distance_km_matrix_dict)
    distance_km_matrix_df.index = distance_km_matrix_df.index.rename('village_code')

    for path in output_filepath_list:
        distance_km_matrix_df.to_csv(path)
