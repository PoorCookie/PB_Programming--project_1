'''
main файл объединяющий все файлы
в качестве аргумента через командную строку получает название файлов
'''

import sys
import data
from functions import *


if __name__ == "__main__":
    filenames = sys.argv[1:]
    chars_dict = characters_in_file_counter(
        filenames)
    # йцукен
    icuken_fdict, icuken_hdict = load_calculator(chars_dict,
                                                 data.layout_map_icuken, data)

    # скоропис
    skoropis_fdict, skoropis_hdict = load_calculator(
        chars_dict, data.layout_map_skoropis, data)

    # вызов
    vyzov_fdict, vyzov_hdict = load_calculator(
        chars_dict, data.layout_map_vyzov, data)

    # диктор
    dictor_fdict, dictor_hdict = load_calculator(
        chars_dict, data.layout_map_dictor, data)

    print('Йцукен:')
    formated_fingers_result_out(icuken_fdict)
    formated_hands_result_out(icuken_hdict)
    print('СКОРОПИС:')
    formated_fingers_result_out(skoropis_fdict)
    formated_hands_result_out(skoropis_hdict)
    print('ВЫЗОВ:')
    formated_fingers_result_out(vyzov_fdict)
    formated_hands_result_out(vyzov_hdict)
    print('ДИКТОР:')
    formated_fingers_result_out(dictor_fdict)
    formated_hands_result_out(dictor_hdict)
    visualization(icuken_fdict, skoropis_fdict, vyzov_fdict, dictor_fdict,
                  filenames, icuken_hdict, skoropis_hdict, vyzov_hdict,
                  dictor_hdict)
