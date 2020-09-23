"""
This is to generate chinese dictionary for the column name as a helper
"""

import os

import googletrans

from lib.data_keys import (
    get_tabular_data_filepath, 
    get_csv_column_name,
    contain_chinese_character,
    save_dictionary
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


if __name__ == '__main__':
    data_dir = os.path.join(BASE_DIR, 'data')
    output_path = os.path.join(BASE_DIR, 'data_processor', 'data', 'chinese_english_column_helper_dict.pkl')

    # get all column name
    print("INFO: getting all column name")
    tabular_data_filepath = get_tabular_data_filepath(data_dir)

    all_column_name = []
    for path in tabular_data_filepath:
        all_column_name.extend(get_csv_column_name(path))

    # only filter the chinese column name
    chinese_column_name = [x for x in all_column_name if contain_chinese_character(x)]

    # ask help from mr google translate, send it on a single http request!
    print("INFO: getting translation from google translate")
    translator = googletrans.Translator()
    translation = translator.translate(chinese_column_name, dest='en', src='zh-cn')
    translation = [x.text for x in translation]
    translation = map(lambda x: x.lower(), translation)
    translation = map(lambda x: x.replace(' ', '_'), translation)

    chinese_english_column_name_dictionary = dict(zip(chinese_column_name, translation))

    print("INFO: saving dictionary in {}".format(output_path))
    save_dictionary(chinese_english_column_name_dictionary, output_path)
