'''
main файл объединяющий все файлы
в качестве аргумента через командную строку получает название файлов
'''

import sys
import data
from functions import *


if __name__ == "__main__":
    filenames = sys.argv[1:-1]
    chars_dict, words_dict = characters_and_words_in_file_counter(
        filenames)
    max_combos_length = int(sys.argv[-1])
    combos = combos_counter(words_dict, max_combos_length)
    # йцукен
    icuken_fdict, icuken_hdict = load_calculator(chars_dict,
                                                 data.layout_map_icuken, data)
    icuken_combos_h, icuken_combos_c = combos_dict_to_combos_count_dict(
        *conditional_combos_counter(
            combos, data.layout_map_icuken, data, max_combos_length))

    # скоропис
    skoropis_fdict, skoropis_hdict = load_calculator(
        chars_dict, data.layout_map_skoropis, data)
    skoropis_combos_h, skoropis_combos_c = combos_dict_to_combos_count_dict(
        *conditional_combos_counter(
            combos, data.layout_map_skoropis, data, max_combos_length))

    # вызов
    vyzov_fdict, vyzov_hdict = load_calculator(
        chars_dict, data.layout_map_vyzov, data)
    vyzov_combos_h, vyzov_combos_c = combos_dict_to_combos_count_dict(
        *conditional_combos_counter(
            combos, data.layout_map_vyzov, data, max_combos_length))

    # диктор
    dictor_fdict, dictor_hdict = load_calculator(
        chars_dict, data.layout_map_dictor, data)
    dictor_combos_h, dictor_combos_c = combos_dict_to_combos_count_dict(
        *conditional_combos_counter(
            combos, data.layout_map_dictor, data, max_combos_length))

    print('Йцукен:')
    formated_fingers_result_out(icuken_fdict)
    formated_hands_result_out(icuken_hdict)
    formated_combos_results_out(icuken_combos_h, icuken_combos_c)
    print('СКОРОПИС:')
    formated_fingers_result_out(skoropis_fdict)
    formated_hands_result_out(skoropis_hdict)
    formated_combos_results_out(skoropis_combos_h, skoropis_combos_c)
    print('ВЫЗОВ:')
    formated_fingers_result_out(vyzov_fdict)
    formated_hands_result_out(vyzov_hdict)
    formated_combos_results_out(vyzov_combos_h, vyzov_combos_c)
    print('ДИКТОР:')
    formated_fingers_result_out(dictor_fdict)
    formated_hands_result_out(dictor_hdict)
    formated_combos_results_out(dictor_combos_h, dictor_combos_c)
    visualization(icuken_fdict, skoropis_fdict, vyzov_fdict, dictor_fdict,
                  filenames, icuken_hdict, skoropis_hdict, vyzov_hdict,
                  dictor_hdict, icuken_combos_h, skoropis_combos_h,
                  vyzov_combos_h, dictor_combos_h, icuken_combos_c,
                  skoropis_combos_c, vyzov_combos_c, dictor_combos_c)
