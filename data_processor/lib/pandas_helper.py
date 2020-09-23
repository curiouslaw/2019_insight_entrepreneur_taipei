from typing import Callable

import pandas as pd


def change_column(df: pd.DataFrame, column: str, function: Callable) -> None:
    df[column] = df[column].apply(function)


def change_on_multiple_columns(df: pd.DataFrame, column_selector: Callable[..., bool],
    function: Callable) -> None:
    for column in [x for x in df.columns if lambda x: column_selector(x)]:
        change_column(df, column, function)
