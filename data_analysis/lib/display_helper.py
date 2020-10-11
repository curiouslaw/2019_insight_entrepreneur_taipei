import pandas as pd
from tabulate import tabulate


def display_df(data_frame: pd.DataFrame, style: str = 'psql') -> None:
    sample_df = data_frame.head()

    display_col = []
    for col in sample_df.columns:
        _col_split = col.split('_')
        _col_display = []
        for i, x in enumerate(_col_split):
            if i % 2 == 0 and i != 0:
                _col_display.append('\n')
            _col_display.append(x)

            if i != len(_col_split) - 1:
                _col_display.append('_')

        _col_display_str = ('').join(_col_display)
        display_col.append(_col_display_str)

    print('here is the example of the table:')
    print(tabulate(sample_df, headers=display_col, tablefmt=style))
