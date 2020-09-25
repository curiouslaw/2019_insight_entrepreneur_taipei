import os
from builtins import KeyError

import pandas as pd

from lib import shared_lib
from shared_lib.data_info import DataInfo
from pypinyin import pinyin

from lib.data_keys import (
    contain_chinese_character,
    load_dictionary,
    UsedKeys
)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)


def normalize_data(filepath: str, helper_dict_filepath: str,
                   area_dimension_table: pd.DataFrame) -> pd.DataFrame:
    data_df = pd.read_csv(filepath)

    # translate use generated google translate library if there is any chinese character
    if any([contain_chinese_character(x) for x in data_df.columns]):
        helper_dict = load_dictionary(helper_dict_filepath)
        data_df = data_df.rename(columns=helper_dict)

    data_df = data_df.rename(columns={
        data_df.columns[0]: 'township_chinese_name',
        data_df.columns[1]: 'village_chinese_name',
    })

    return data_df


def attach_key_id_by_name(data_df: pd.DataFrame, dimension_table: pd.DataFrame,
    key_obj: UsedKeys) -> pd.DataFrame:
    column_keys = key_obj.column_key_list
    attach_id = key_obj.key_id

    # used heuristic process on dimension table, there might be duplicate on name matching cause based on geometry
    dimension_table.fillna('', inplace=True)
    dimension_table = dimension_table[~dimension_table.duplicated(column_keys, keep='first')]

    keyed = pd.merge(data_df, dimension_table[column_keys + [attach_id]],
        'left', on=column_keys, validate='m:1')

    unmatched_data = sum(keyed[attach_id].isnull())
    if unmatched_data:
        print("There is unmatched {} data from {} after exact matching, "
            "will try fuzzy matching".format(unmatched_data, len(keyed)))

        dimension_table['township_chinese_name_pinyin'] = dimension_table['township_chinese_name'].apply(pinyin).apply(str)
        dimension_table['village_chinese_name_pinyin'] = dimension_table['village_chinese_name'].apply(pinyin).apply(str)

        keyed['township_chinese_name_pinyin'] = keyed['township_chinese_name'].apply(pinyin).apply(str)
        keyed['village_chinese_name_pinyin'] = keyed['village_chinese_name'].apply(pinyin).apply(str)

        # same county id but search for same pinyin (there might use different hanzi)
        for index, row in keyed[keyed[attach_id].isnull()].iterrows():
            match_0 = dimension_table['county_id'] == row['county_id']
            match_1 = dimension_table[match_0]['township_chinese_name_pinyin'] == row['township_chinese_name_pinyin']
            match_2 = dimension_table[match_0]['village_chinese_name_pinyin'] == row['village_chinese_name_pinyin']

            if sum(match_1 & match_2) == 1:
                keyed.loc[index, 'village_code'] = dimension_table[match_0][match_1 & match_2].iloc[0]['village_code']

        # same county id, try search for similarity
        for index, row in keyed[keyed[attach_id].isnull()].iterrows():
            match_0 = dimension_table['county_id'] == row['county_id']
            match_1 = dimension_table[match_0]['township_chinese_name']\
                .apply(lambda x: True if used_keys.compute_similarity(row['township_chinese_name'], x) > 0.5 else False)
            match_2 = dimension_table[match_0]['village_chinese_name']\
                .apply(lambda x: True if used_keys.compute_similarity(row['village_chinese_name'], x) > 0.5 else False)

            if sum(match_1 & match_2) == 1:
                keyed.loc[index, 'village_code'] = dimension_table[match_0][match_1 & match_2].iloc[0]['village_code']

        # same county id, try search for similarity
        for index, row in keyed[keyed[attach_id].isnull()].iterrows():
            match_0 = dimension_table['county_id'] == row['county_id']
            match_1 = dimension_table[match_0]['township_chinese_name']\
                .apply(lambda x: True if used_keys.compute_similarity(row['township_chinese_name'], x) > 0.5 else False)
            match_2 = dimension_table[match_0]['village_chinese_name']\
                .apply(lambda x: True if used_keys.compute_similarity(row['village_chinese_name'], x) > 0.8 else False)

            if sum(match_1 & match_2) == 1:
                keyed.loc[index, 'village_code'] = dimension_table[match_0][match_1 & match_2].iloc[0]['village_code']

        # same county id, try search for similarity only on village chinese name
        for index, row in keyed[keyed[attach_id].isnull()].iterrows():
            match_0 = dimension_table['county_id'] == row['county_id']
            match_1 = dimension_table[match_0]['village_chinese_name']\
                .apply(lambda x: True if used_keys.compute_similarity(row['village_chinese_name'], x) > 0.8 else False)

            if sum(match_1) == 1:
                keyed.loc[index, 'village_code'] = dimension_table[match_0][match_1].iloc[0]['village_code']

        print("{} unmatched data after fuzzy matching".format(sum(keyed[attach_id].isnull())))

        del keyed['township_chinese_name_pinyin']
        del keyed['village_chinese_name_pinyin']

        del dimension_table['township_chinese_name_pinyin']
        del dimension_table['village_chinese_name_pinyin']

    return keyed


if __name__ == '__main__':
    pd.options.mode.chained_assignment = None  # quiet pandas warning on chained operation

    data_name = 'taipei_income_by_village'
    data_dir = os.path.join(BASE_DIR, 'data', data_name)
    data_info_path = os.path.join(data_dir, 'data_info.csv')
    helper_dict_filepath = os.path.join(CURRENT_DIR, 'data', 'chinese_english_column_helper_dict.pkl')
    area_dimension_table = pd.read_csv(os.path.join(CURRENT_DIR, 'data', 'area_dimension_table.csv'))

    data_info = DataInfo(data_info_path)

    input_filepath = data_info.get_structured_filepath()
    output_filepath = data_info.get_normalized_filepath()

    used_keys = UsedKeys()
    data_df = normalize_data(input_filepath, helper_dict_filepath, area_dimension_table)
    data_df = attach_key_id_by_name(data_df, area_dimension_table, used_keys)

    # quick testing if there is key in the file before saving
    if used_keys.list_contain_used_key(data_df.columns):
        pass
    else:
        raise KeyError("list doesn't contain any used key")

    data_df.to_csv(output_filepath, index=False)
