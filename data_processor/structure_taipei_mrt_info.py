import os
import re
import subprocess

import pandas as pd

from lib import shared_lib
from shared_lib.data_info import DataInfo


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_row_number(filepath: str, footer_lookup: int = 20) -> int:
    """Get data number from the source information, use the C "tail" command and regex to capture the data number

    Args:
        filepath (str): path to the file
        footer_lookup (int, optional): line number look up from bottom, default 20

    Returns:
        int: data number retrieved
    """
    t = subprocess.Popen(['tail', '-{}'.format(footer_lookup), filepath], stdout=subprocess.PIPE)
    stdout, _ = t.communicate()
    stdout = stdout.decode('utf-8')

    match = re.search('(\([\s+]?)([0-9]+)([\s+]?個資料.*\))', stdout)
    row_number = match.group(2)

    return int(row_number)


def read_parse_save(input_filepath: str, output_filepath: str) -> None:
    print('INFO: reading data from {}'.format(input_filepath))
    row_number = get_row_number(input_filepath)

    df = pd.read_table(input_filepath, sep='\s+', skiprows=[1], nrows=row_number)

    print('INFO: saving parsed data into {}'.format(output_filepath))
    df.to_csv(output_filepath, index=False)


if __name__ == '__main__':
    data_dir = os.path.join(BASE_DIR, 'data', 'taipei_mrt_info')
    data_info_path = os.path.join(data_dir, 'data_info.csv')
    data_info = DataInfo(data_info_path)

    input_filepath_list = data_info.get_download_filepath_list()
    output_dirpath = data_info.get_structured_dirpath()

    for path in input_filepath_list:
        print('INFO: processing data from {}'.format(path))
        _filename = os.path.basename(path)
        _filename = _filename.split('.')[0]
        _output_filepath = os.path.join(output_dirpath, _filename)
        _output_filepath = _output_filepath + '.csv'

        read_parse_save(path, _output_filepath)
