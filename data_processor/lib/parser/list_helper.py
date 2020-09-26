from typing import List


def fix_divider_error(string: str, divider: str, replace: str) -> str:
    if divider in string:
        return string.replace(divider, replace)
    else:
        return string


def fix_endian_encoding_string(string: str) -> str:
    if (string[0] == '\ufeff') or (string[0] == '\ufeff\u0000') or (string[0] == '\u0000\ufeff'):
        new_string = string[1:]
        return new_string
    else:
        return string


def textfile_into_list(filepath: str) -> List[str]:
    with open(filepath, 'r') as f:
        text_data = f.read()

    text_data = fix_endian_encoding_string(text_data)
    text_data = fix_divider_error(text_data, "}{", "}\n{")
    text_data = text_data.split('\n')

    return text_data


def clean_endian_encoding(string_list: List[str]) -> str:
    if (string_list[0] == '\ufeff') or (string_list[0] == '\ufeff\u0000') or (string_list[0] == '\u0000\ufeff'):
        del string_list[0]


def clean_empty_line(string_list: List[str]) -> None:
    for i in range(len(string_list)):
        if string_list[i] == '':
            del string_list[i]


