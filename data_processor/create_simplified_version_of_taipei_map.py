import os

from lib.geolib_helper import get_shp_filepath, load_normalize_gov_shp_data

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)


if __name__ == '__main__':
    data_dir = os.path.join(BASE_DIR, 'data')
    area_dimension_table_filepath = os.path.join(data_dir, 'area_dimension_table.csv')
    village_shp_filepath = get_shp_filepath(os.path.join(data_dir, 'taiwan_twd97_map_data_village'))

    data_mart_dirpath = os.path.join(data_dir, 'aggregated-data_mart')
    output_village_filepath = os.path.join(data_mart_dirpath, 'simplified_taipei_village.geojson')
    output_township_filepath = os.path.join(data_mart_dirpath, 'simplified_taipei_township.geojson')

    village_gpd = load_normalize_gov_shp_data(village_shp_filepath)

    taipei_village_gpd = village_gpd[village_gpd['county_chinese_name'] == '臺北市']
    taipei_village_gpd.set_index('village_code', drop=False, inplace=True)

    taipei_township_gpd = taipei_village_gpd[['township_code', 'geometry']].dissolve(by='township_code')

    # select tolerance of 0.05km, 1 point is about 111 km
    tolerance = 0.05 / 111

    # save for village detail geojson
    simplified_village_gpd = taipei_village_gpd.copy()
    simplified_village_gpd['geometry'] = simplified_village_gpd.simplify(tolerance, preserve_topology=False)
    simplified_village_gpd[['geometry']].to_file(output_village_filepath, driver='GeoJSON')

    # save for township detail geojson
    simplified_township_gpd = taipei_township_gpd.copy()
    simplified_township_gpd['geometry'] = simplified_township_gpd.simplify(tolerance, preserve_topology=False)
    simplified_township_gpd[['geometry']].to_file(output_township_filepath, driver='GeoJSON')
