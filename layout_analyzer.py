'''
main файл объединяющий все файлы
в качестве аргумента через командную строку получает название файла
'''

import sys
import data
from functions import *


if __name__ == "__main__":
    chars_dict = characters_in_file_counter(
        sys.argv[1:])

    # йцукен
    icuken_fdict = load_calculator(
        chars_dict, data.layout_map_icuken, data)

    # скоропис
    skoropis_fdict = load_calculator(
        chars_dict, data.layout_map_skoropis, data)

    # вызов
    vyzov_fdict = load_calculator(
        chars_dict, data.layout_map_vyzov, data)

    # диктор
    dictor_fdict = load_calculator(
        chars_dict, data.layout_map_dictor, data)

    print('Йцукен:')
    formated_fingers_result_out(icuken_fdict)
    print('СКОРОПИС:')
    formated_fingers_result_out(skoropis_fdict)
    print('ВЫЗОВ:')
    formated_fingers_result_out(vyzov_fdict)
    print('ДИКТОР:')
    formated_fingers_result_out(dictor_fdict)
    visualization(icuken_fdict, skoropis_fdict, vyzov_fdict, dictor_fdict,
                  sys.argv[1:])
