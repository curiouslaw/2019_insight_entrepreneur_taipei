from typing import Dict, List
from urllib.parse import urlparse, parse_qsl

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

from . import WebExplorer


def parse_query_from_url(url: str) -> dict:
    parsed_url = urlparse(url)
    parsed_query = dict(parse_qsl(parsed_url.query))

    return parsed_query


class WebExplorerTaipeiMetro(WebExplorer):
    def __init__(self, driver_obj: object, url: str):
        self.driver = driver_obj
        self.url = url
        super().__init__(self.driver, self.url)

    def get_available_station_object(self) -> List[WebElement]:
        return self.get_web_elements_obj((By.XPATH, '//map/area[contains(@href, "tw/station/")]'))

    def scrape_available_station_links(self) -> List[str]:
        web_element_list = self.get_available_station_object()
        available_station_links = [x.get_attribute('href') for x in web_element_list]

        return available_station_links

    def scrape_longitude_latitude_data(self) -> Dict[str, Dict[str, str]]:
        station_name_web_element = self.find_a_web_element_obj((By.XPATH, '//td[@class="station__img"]')) 
        long_lat_web_element = self.find_a_web_element_obj((By.XPATH, '//a[contains(@href, "googlemap") and contains(@href, "Longitude")  and contains(@href, "Latitude")]'))

        station_name = station_name_web_element.text
        long_lat = parse_query_from_url(long_lat_web_element.get_attribute('href'))

        return {station_name: long_lat}
