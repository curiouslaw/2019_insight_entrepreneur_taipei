from difflib import SequenceMatcher
from typing import List


class UsedKeys:
    used_keys = ''

    def compute_similarity(self, compare_list: List[str]) -> dict:
        key_compare = self.used_keys.casefold()
        diff_value = map(lambda x: SequenceMatcher(a=key_compare, b=x).ratio, compare_list)
        diff_dict = dict(zip(compare_list, diff_value))

        return diff_dict

    def get_most_similar_keys(self, compare_list: List[str]) -> str:
        diff_dict = self.compute_similarity(compare_list)

        return max(diff_dict)
