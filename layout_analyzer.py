'''
main файл объединяющий все файлы
в качестве аргумента через командную строку получает название файлов
'''

import sys
import data
from functions import *


if __name__ == "__main__":
    max_combos_length = 2
    words_set_1grams = file_to_words_set('1grams-3.txt')
    words_set_sortchbukw = file_to_words_set('sortchbukw.csv')
    combos_1grams = combos_counter(words_set_1grams)
    combos_sortchbukw = combos_counter(words_set_sortchbukw)

    # йцукен
    icuken_combos_h_1grams, icuken_combos_c_1grams = (
        combos_dict_to_combos_count_dict(
            *conditional_combos_counter(
                combos_1grams, data.layout_map_icuken,
                data, max_combos_length))
        )
    icuken_combos_h_sortchbukw, icuken_combos_c_sortchbukw = (
        combos_dict_to_combos_count_dict(
            *conditional_combos_counter(
                combos_sortchbukw, data.layout_map_icuken,
                data, max_combos_length))
        )

    # вызов
    vyzov_combos_h_1grams, vyzov_combos_c_1grams = (
        combos_dict_to_combos_count_dict(
            *conditional_combos_counter(
                combos_1grams, data.layout_map_vyzov,
                data, max_combos_length))
        )
    vyzov_combos_h_sortchbukw, vyzov_combos_c_sortchbukw = (
        combos_dict_to_combos_count_dict(
            *conditional_combos_counter(
                combos_sortchbukw, data.layout_map_vyzov,
                data, max_combos_length))
        )

    visualization(
        icuken_combos_h_1grams, icuken_combos_h_sortchbukw,
        icuken_combos_c_1grams, icuken_combos_c_sortchbukw,
        vyzov_combos_h_1grams, vyzov_combos_h_sortchbukw,
        vyzov_combos_c_1grams, vyzov_combos_c_sortchbukw
    )
