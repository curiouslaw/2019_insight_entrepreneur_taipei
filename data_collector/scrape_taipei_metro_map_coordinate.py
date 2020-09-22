# This file would for to www.metro.taipei, get some links to scrape and take data
# on it based on the requred data
#
# Note:
# - The process respect www.metro.taipei website permission (i.e. robots.txt)
# - Please use the code for education purpose or reference only,
#   don't use the code to exploit or do something harmful for the company
# - Each scrape is different, this approach is the pragmatic approach with
#   only one connection running sequentially (which is a good approach for this
#   case). For more scalable design (in Python) you could explore scrapy
#   framework.

import argparse
import os
import sys
import time

import pandas as pd
from selenium import webdriver

from lib import shared_lib
from shared_lib.data_info import DataInfo

from lib.web_scrapper.web_explorer import check_page
from lib.web_scrapper.web_explorer.taipei_metro import WebExplorerTaipeiMetro

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def build_argparser() -> argparse.ArgumentParser:
    available_option = ['show', 'hide']

    parser = argparse.ArgumentParser(
        description='If you are curious what the scrapper do, use "show" option\n\n'
            'use show:\n'
            '  python {} -o show\n'.format(sys.argv[0], available_option[0]),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('-o', dest='option',
        type=str, choices=available_option, metavar='option',
        default='hide',
        help="available choices: [ " + ' | '.join(available_option) + ' ]'
    )

    return parser


if __name__ == '__main__':
    parser = build_argparser()
    args = parser.parse_args()
    option = args.option

    data_dir = os.path.join(BASE_DIR, 'data', 'taipei_mrt_map_coordinate')
    data_info_path = os.path.join(data_dir, 'data_info.csv')
    data_info = DataInfo(data_info_path)

    output_filename = 'taipei_mrt_map_coordinate.csv'
    output_filepath = os.path.join(data_info.get_download_dirpath(), output_filename)

    # set webdriver, request interceptor scope, and wait object
    print("note: the program heavily depend on your internet connection")
    print("INFO: setup crawler, use Chrome driver")
    webdriver_options = webdriver.ChromeOptions()
    if option == 'hide':
        webdriver_options.headless = True
    elif option == 'show':
        webdriver_options.headless = False

    driver = webdriver.Chrome(options=webdriver_options)
    driver.set_page_load_timeout(30)
    start_url = data_info.get_info_force('main_source')

    web_explorer = WebExplorerTaipeiMetro(driver, start_url)
    check_page(driver)

    sys.stderr = object  # hacky way to silent thread response fail

    print("INFO: starting the crawler")
    # get all of the station
    available_station_links = web_explorer.scrape_available_station_links()

    # go to the station one by one and grab long lat data
    total_page = len(available_station_links) 
    current_page_num = 1

    long_lat_data = {}

    for link in available_station_links:
        print("INFO: getting data for page {} of {}".format(
            current_page_num, total_page))
        print("INFO: getting data for page {}".format(link))
        web_explorer.get(link)

        long_lat_data = {
            **long_lat_data,
            **web_explorer.scrape_longitude_latitude_data()  # this is where the scraping function called
        }
        time.sleep(1)  # try to be polite ok..
        print("INFO: finished getting data for page {}".format(current_page_num))

        current_page_num = current_page_num + 1

    driver.close()

    print("INFO: finished getting all data. Data saved in: {}"
        .format(output_filepath)
    )

    df_data = pd.DataFrame().from_dict(long_lat_data, orient='index')
    df_data.index = df_data.index.set_names('station_name')
    df_data = df_data.reset_index()
    df_data.to_csv(output_filepath, index=False)
