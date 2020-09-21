import os

import pandas as pd

from lib import shared_lib
from shared_lib.data_info import DataInfo

from data_processor.lib.data_keys import (
    contain_chinese_character,
    load_dictionary,
    UsedKeys
)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)


def normalize_data(filepath: str, helper_dict_filepath: str) -> pd.DataFrame:
    data_df = pd.read_csv(filepath)

    # translate use generated google translate library if there is any chinese character
    if any([contain_chinese_character(x) for x in data_df.columns]):
        helper_dict = load_dictionary(helper_dict_filepath)
        data_df = data_df.rename(columns=helper_dict)

    data_df['price'] = data_df['price'].apply(lambda x: int(x.replace(',','')))

    return data_df


if __name__ == '__main__':
    data_name = 'taipei_shop_rent_price'
    data_dir = os.path.join(BASE_DIR, 'data', data_name)
    data_info_path = os.path.join(data_dir, 'data_info.csv')
    helper_dict_filepath = os.path.join(CURRENT_DIR, 'data', 'chinese_english_column_helper_dict.pkl')

    data_info = DataInfo(data_info_path)

    input_filepath = data_info.get_structured_filepath()
    output_filepath = data_info.get_normalized_filepath()

    used_keys = UsedKeys()
    data_df = normalize_data(input_filepath, helper_dict_filepath)

    # quick testing if there is key in the file before saving
    if used_keys.list_contain_used_key(data_df.columns):
        pass
    else:
        raise KeyError("list doesn't contain any used key")

    data_df.to_csv(output_filepath, index=False)
