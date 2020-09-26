from typing import Callable, Union

import pandas as pd


def change_column(df: pd.DataFrame, column: str, function: Callable) -> None:
    df[column] = df[column].apply(function)


def change_on_multiple_columns(df: pd.DataFrame, column_selector: Callable[..., bool],
    function: Callable) -> None:
    for column in [x for x in df.columns if column_selector(x)]:
        change_column(df, column, function)


def try_fix_encoding(string: str) -> str:
    if string:
        try:
            return string.encode('latin1').decode('utf8')
        except Exception:
            return string
    else:
        return ""


def try_get_dict(dictionary: dict, string: str) -> str:
    if match := dictionary.get(string):
        return match
    else:
        return string


def find_helper(lookup: str, string: str) -> Union[str, bool]:
    if lookup in string:
        return string.find(lookup)
    else:
        return False
