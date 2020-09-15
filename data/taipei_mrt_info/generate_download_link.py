# this file would do scrape on the taipei goverment website dataset on the specific filetype
# note: the process respect taipei goverment website permission (i.e. robots.txt)

import builtins
import csv
import os
import requests

from bs4 import BeautifulSoup

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
INFO_PATH = os.path.join(CURRENT_DIR, 'data_info.csv')
OUTPUT_PATH = os.path.join(CURRENT_DIR, 'download_links.txt')

def get_info(filepath:str, name:str):
    with open(INFO_PATH, 'r') as f:
        for row in csv.reader(f, delimiter=','):
            if row[0] == name:
                return row[1]
        raise builtins.KeyError("{} not found in {}".format(name, filepath))
            

if __name__ == "__main__":
    html = get_info(INFO_PATH, 'main_source')
    response = requests.get(html)

    soup = BeautifulSoup(response.text, 'html.parser')

    soup_links = soup.find_all('a')
    download_list = []
    for link in soup_links:
        link_filetype = get_info(INFO_PATH, 'get_datatype')
        if link_filetype in link.text :
            download_list.append(link['href'])
    
    if download_list:
        with open(OUTPUT_PATH, 'w') as f:
            for link in download_list:
                f.write(link + '\n')

        

