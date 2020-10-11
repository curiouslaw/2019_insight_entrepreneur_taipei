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
import os
import sys
import time

from seleniumwire import webdriver
from webdriver_manager.firefox import GeckoDriverManager

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

    data_dir = os.path.join(BASE_DIR, 'data', 'taipei_shop_rent_price')
    data_info_path = os.path.join(data_dir, 'data_info.csv')
    data_info = DataInfo(data_info_path)

    output_filename = '591_xhr_responses.json'
    output_filepath = os.path.join(data_info.get_download_dirpath(), output_filename)

    # set webdriver, request interceptor scope, and wait object
    print("note: the program heavily depend on your internet connection")
    print("INFO: setup crawler, use Firefox driver")
    webdriver_options = webdriver.FirefoxOptions()
    if option == 'hide':
        webdriver_options.headless = True
    elif option == 'show':
        webdriver_options.headless = False

    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(),
                               options=webdriver_options)
    driver.set_page_load_timeout(30)
    url_regex = '.*business\.591\.com\.tw\/home\/search\/rsList\?.*'
    driver.scopes = [url_regex]
    start_url = 'https://www.591.com.tw/'

    web_explorer = WebExplorer591(driver, start_url)
    check_page(driver)

    sys.stderr = object  # hacky way to silent thread response fail

    # start page as new guest
    print("INFO: starting the crawler")

    # arrived at homepage, go to the city and category
    web_explorer.initial_guest_page_to_home_page('台北', '店面')

    # starting to get data
    print("INFO: starting to get data")
    last_page_num = web_explorer.get_last_page_num()
    current_page_num = 1

    while True:
        if last_page_num:
            print("INFO: getting data for page {} of {}".format(
                current_page_num, last_page_num))
        else:
            print("INFO: getting data for page {}".format(current_page_num))

        time.sleep(3)  # friendly for the server
        driver.wait_for_request(url_regex)
        print("INFO: page {} finished, moving to next page...".format(current_page_num))

        web_explorer.scroll_down_until_end()
        current_page_num = current_page_num + 1

        next_page_available = web_explorer.click_next_button()

        if not next_page_available:
            break

    print("INFO: seems like no more next page, wrapping data")
    web_explorer.save_all_responses(output_filepath, 'utf-8')

    driver.close()
    print('INFO: getting data from {} finished. File saved on {}'
        .format(start_url, output_filepath))
