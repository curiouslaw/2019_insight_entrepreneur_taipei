from functools import partial
from multiprocessing import Pool
from typing import Dict, Union, List, Tuple

import geopandas as gpd
import pandas as pd

from shapely.geometry import Point

from .geolib_helper import load_normalize_gov_shp_data


class GeoCoder:
    def __init__(self, shp_filepath: str, taipei_only: bool = False):
        self.shp_gdf: gpd.GeoDataFrame = load_normalize_gov_shp_data(shp_filepath)

        if taipei_only:
            self.shp_gdf = self.shp_gdf[self.shp_gdf['county_chinese_name'].str.fullmatch('臺北市')]
            self.shp_gdf.reset_index(drop=True, inplace=True)

    def long_lat_to_place(self, longitude: float, latitude: float,
        single_match: bool = True) -> Union[pd.Series, pd.DataFrame]:

        point = Point(longitude, latitude)

        if single_match:
            for index, row in self.shp_gdf.iterrows():
                if point.within(row.geometry):
                    return row.drop('geometry')
            return False
        else:
            found = self.shp_gdf.geometry.apply(lambda x: point.within(x))
            if any(found):
                return self.shp_gdf[found].drop('geometry', axis=1)
            else:
                return False

    def point_to_dict(self, key_id_point_tuple: Tuple[Union[str, int], Point],
        value_key: str = 'village_code', single_match: bool = True) -> dict:

        key_id, point = key_id_point_tuple

        if single_match:
            for index, row in self.shp_gdf.iterrows():
                if point.within(row.geometry):
                    return {key_id: row[value_key]}
            return {key_id: None}
        else:
            found = self.shp_gdf.geometry.apply(lambda x: point.within(x))
            if any(found):
                return {key_id: self.shp_gdf[found][value_key].values}
            else:
                return {key_id: None}

    def point_to_dict_multiprocessing(self, key_id_point_tuple_list: List[tuple],
        value_key: str = 'village_code', single_match: bool = True,
        processor_use=None) -> List[dict]:

        f = partial(self.point_to_dict,
            value_key=value_key, single_match=single_match)

        with Pool(processes=processor_use) as pool:
            return_dict_list = pool.map(f, key_id_point_tuple_list)

        return return_dict_list




