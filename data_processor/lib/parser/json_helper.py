import json
from typing import List

import pandas as pd

from .list_helper import textfile_into_list, clean_empty_line


def text_list_into_json_list(text_list: List[str]) -> List[dict]:
    json_list = text_list.copy()
    for i, x in enumerate(json_list):
        json_list[i] = json.loads(x)

    return json_list


def textfile_into_json_list(filepath: List[str]) -> List[dict]:
    text_data = textfile_into_list(filepath)
    clean_empty_line(text_data)
    json_list = text_list_into_json_list(text_data)

    return json_list


def normalize_json_into_df(json_list: List[str]) -> pd.DataFrame:
    df = pd.DataFrame()
    for x in json_list:
        df_add = pd.DataFrame.from_dict(x)
        df = df.append(df_add, ignore_index=True, verify_integrity=True)

        del df_add

    return df
