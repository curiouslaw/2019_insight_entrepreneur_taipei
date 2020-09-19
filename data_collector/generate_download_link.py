# This file would do scrape on the taipei goverment website dataset on the
# specific filetype
#
# Note:
# - The process respect taipei goverment website permission (i.e. robots.txt)

import argparse
import os
import requests
import itertools
import sys
from typing import List

from bs4 import BeautifulSoup

from lib import shared_lib
from shared_lib.data_info import DataInfo


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def build_argparser():
    available_data_name = ['taipei_mrt_info', 'taipei_map_points',
        'taiwan_twd97_map_data_village', 'taiwan_twd97_map_data_city',
        'taiwan_twd97_map_data_province']
    parser = argparse.ArgumentParser(
        description='example:\n'
            '  python {} {}\n'.format(sys.argv[0], available_data_name[0]),
        epilog="to download links:\n"
            "  run 'bash download_and_extract_url.sh [data_name]' to download the file",

        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('data_name',
        type=str, choices=available_data_name, metavar='data_name',
        help="available choices: [ " + ' | '.join(available_data_name) + ' ]'
    )

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    return parser


def try_to_get_link(url: str, filetype: str) -> List[str]:
    if 'data.gov.tw/dataset/' in url:
        print("INFO: found pattern for {}".format(url))
        print("INFO: would start open the website, will wait indefinitely")
        print("INFO: if this never finish, it might have some connection problem, quit the process with [CTRL + C]")

        response = requests.get(url, timeout=None)

        print("INFO: getting the website finished, start generating download link")
        soup = BeautifulSoup(response.text, 'html.parser')
        soup_links = soup.find_all('a')

        download_list = []

        for link in soup_links:
            filetype = filetype.casefold()
            if filetype == link.text.casefold():
                download_list.append(link['href'])

        if download_list:
            return download_list
        else:
            print('ERROR: download link not found, web style might be changed')
            sys.exit(0)

    else:
        print('ERROR: generate link might not supported')
        sys.exit(0)


if __name__ == "__main__":
    # setting arguments parser
    parser = build_argparser()
    args = parser.parse_args()

    data_name = args.data_name
    print("INFO: start getting links for data {}".format(data_name))

    data_dir = os.path.join(BASE_DIR, 'data', data_name)
    data_info_path = os.path.join(data_dir, 'data_info.csv')

    data_info = DataInfo(data_info_path)

    if not (url := data_info.get_info('main_source')):
        url = data_info.get_info_contain_force('main_source_')

    download_filetype = data_info.get_info('get_datatype')
    links_filepath = data_info.get_info_force('download_links_filepath')
    output_filepath = os.path.join(data_dir, links_filepath)

    if isinstance(url, list):
        download_list = []
        for x in url:
            download_list.append(try_to_get_link(x, download_filetype))
        download_list = itertools.chain.from_iterable(download_list)
    else:
        download_list = try_to_get_link(url, download_filetype)

    if download_list:
        with open(output_filepath, 'w') as f:
            for link in download_list:
                f.write(link + '\n')

    print("INFO: finished getting links, saved link data in {}".format(
        output_filepath))
    print("INFO: please run 'bash download_and_extract_url.sh {}' to download the file".format(
        data_name))

