# This file would intercept the XHR request of shop front data of www.591.tw
#
# Note:
# - The process respect www.591.com.tw website permission (i.e. robots.txt)
# - Please use the code for education purpose or reference only,
#   don't use the code to exploit or do something harmful for the company
# - Each scrape is different, this approach is the pragmatic approach with
#   only one connection running sequentially (which is a good approach for this
#   case). For more scalable design (in Python) you could explore scrapy
#   framework.

import argparse
import json
import os
import sys
import time
from builtins import IndexError
from typing import List

from seleniumwire import webdriver
from selenium.common.exceptions import TimeoutException

from lib import shared_lib
from shared_lib.data_info import DataInfo

from lib.web_scrapper.web_explorer import check_page
from lib.web_scrapper.web_explorer._591_tw import WebExplorer591

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def build_argparser() -> argparse.ArgumentParser:
    available_option = ['show', 'hide']

    parser = argparse.ArgumentParser(
        description='If you are curious what the scrapper do, use "show" option\n\n'
            'use show:\n'
            '  python {} -o show\n'.format(sys.argv[0], available_option[0]),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('-o', '--option', dest='option',
        type=str, choices=available_option, metavar='',
        default='hide',
        help="available choices: [ " + ' | '.join(available_option) + ' ]'
    )
    
    parser.add_argument('-s', '--start-from', dest='start_from',
        type=int, metavar='', default=None, help="use this if you want to continue from certain data index, on default would start from 1"
    )

    return parser


def get_listing_list_id(filepath: str) -> List[int]:
    with open(filepath, 'r') as f:
        data = f.read()

    data_list = [x for x in data.split('\n')]
    data_list = [json.loads(x) for x in data_list if x!='']

    list_id = []

    for data in data_list:
        data_list = [x['id'] for x in data['data']['data']]
        list_id.extend(data_list)

    list_id = [int(x) for x in list_id]

    return list_id


if __name__ == '__main__':
    parser = build_argparser()
    args = parser.parse_args()
    option = args.option
    if (start_index := args.start_from):
        start_index = start_index - 1

    data_dir = os.path.join(BASE_DIR, 'data', 'taipei_shop_rent_price')
    data_info_path = os.path.join(data_dir, 'data_info.csv')
    data_info = DataInfo(data_info_path)

    download_dirpath = data_info.get_download_dirpath()
    main_xhr_response_filepath = os.path.join(download_dirpath, '591_xhr_responses.json')
    output_filename = '591_lat_long_lookup.json'
    output_filepath = os.path.join(download_dirpath, output_filename)

    list_post_id = get_listing_list_id(main_xhr_response_filepath)

    # set webdriver, request interceptor scope, and wait object
    print("note: this scrapping will take hours (there are some brakes "
        "to respect the website). The program heavily depend on your internet connection")
    print("INFO: setup crawler, use Chrome driver")
    webdriver_options = webdriver.ChromeOptions()
    if option == 'hide':
        webdriver_options.headless = True
    elif option == 'show':
        webdriver_options.headless = False

    driver = webdriver.Chrome(options=webdriver_options)
    driver.set_page_load_timeout(60)
    url_regex = '.*maps\.google\.com\.tw\/maps?.*'
    driver.scopes = [url_regex]
    start_url = 'https://www.591.com.tw/'

    web_explorer = WebExplorer591(driver, start_url)
    check_page(driver)

    # sys.stderr = object  # a hacky way to quier the warning

    # start page as new guest
    print("INFO: starting the crawler")

    # arrived at homepage, go to the city and category
    web_explorer.initial_guest_page_to_home_page('台北', '店面')
    web_explorer.scroll_down_until_end()
    web_explorer.click_next_button()

    # starting to get data
    print("INFO: starting to get data, will save each progress in {}".format(output_filepath))
    total_data = len(list_post_id)

    if not start_index:
        if os.path.isfile(output_filepath):
            os.remove(output_filepath)
    result = []

    for index, post_id in enumerate(list_post_id):
        # break if want to use start for
        if start_index:
            if index < start_index:
                continue

        print("INFO: getting data for index {} of {}".format(index + 1, total_data))
        del driver.requests

        web_explorer.go_to_page_id(post_id)
        print("INFO: capturing data on {}".format(driver.current_url))
        time.sleep(0.5)  # friendly for the server

        web_explorer.scroll_down_until_end()

        if not web_explorer.check_page_error():
            try:
                driver.wait_for_request(url_regex)
            except TimeoutException:
                pass

            try:
                catch_request = driver.requests.pop()
                result.append(json.dumps({"current_url": driver.current_url, "get_request": catch_request.url}))
            except IndexError:
                result.append(json.dumps({"current_url": driver.current_url, "get_request": "TIMEOUT"}))
        else:
            result.append(json.dumps({"current_url": driver.current_url, "get_request": "N/A"}))

        with open(output_filepath, 'a') as f:  # just for precaution if something happen
            f.write(result[-1])
            f.write('\n')

        time.sleep(0.5)  # friendly for the server

    if not start_index:
        with open(output_filepath, 'w') as f:  # overwrite with full object, in case there is error
            f.write('\n'.join(result))

    driver.close()
    print('INFO: getting data finished. File saved on {}'
        .format(start_url, output_filepath))
