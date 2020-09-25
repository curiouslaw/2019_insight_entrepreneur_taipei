from typing import Union

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
