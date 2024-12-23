'''
подключаемый файл с функциями,
необходимыми для подсчёта символов в файле, нагрузки на пальцы
'''
import matplotlib.pyplot as plt
import numpy as np


def characters_in_file_counter(filenames):
    '''
    получает: названия файлов
    возвращает словари:
    chars - 'символ': количество повторений
    '''

    chars = {}
    for filename in filenames:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip(' ')
                for char in line:
                    if char in chars:
                        chars[char] += 1
                    else:
                        chars[char] = 1

    return chars


def key_from_value(item, the_dict):
    '''
    получает: сканкод, словарь
    возвращает: ключ, в значения которого входит сканкод
    '''
    for key, value in the_dict.items():
        if item in value:
            return key


def scancode_from_char(char, the_dict):
    '''
    получает: символ, словарь
    возвращает: первый элемент списка элемента получаемого словаря,
    ключ которого = char
    '''
    for key, scancode in the_dict.items():
        if char == key:
            return scancode[0]


def load_calculator(chars_dict, imported_layout_map, data):
    '''
    получает:
    словарь - 'символ': количество
    словарь - 'символ': 'сканкод клавиши'
    файл со словарями соответствия сканкодов - цены/пальца
    возвращает: словарь 'final_fingers_load' - 'палец': нагрузка
    '''

    # возвращаемый словарь
    final_fingers_load = {
        'lfi5': 0,
        'lfi4': 0,
        'lfi3': 0,
        'lfi2': 0,
        'lfi1': 0,
        'rfi1': 0,
        'rfi2': 0,
        'rfi3': 0,
        'rfi4': 0,
        'rfi5': 0
    }

    # блок прогона каждой клавиши, поиск соответствия
    # символа из словаря 'chars' с файлом разметки раскладки
    # после - сопоставление нагрузки и пальца
    for char, count in chars_dict.items():
        for key, value in imported_layout_map.items():
            if char == key:
                if len(value) > 1:  # если согласно файла разметки
                    # раскладки символ набирается с мод. клавишей
                    for key in value:
                        scancode = key
                        price = key_from_value(scancode, data.key_price)
                        finger = key_from_value(scancode, data.key_finger)
                        if not finger:
                            continue
                        final_fingers_load[finger] += count * price
                else:
                    scancode = value[0]
                    price = key_from_value(scancode, data.key_price)
                    finger = key_from_value(scancode, data.key_finger)
                    if not finger:
                        continue
                    final_fingers_load[finger] += count * price

    return final_fingers_load


def formated_fingers_result_out(the_dict):
    '''
    получает:
    словарь - 'палец': нагрузка на него
    выводит:
    форматированное содержание словаря в консоль
    '''
    for finger, count in the_dict.items():
        print(f'{finger}: {count}')
    print('\n')


def visualization(
        layout1, layout2, layout3, layout4, files):
    '''
    функция визуализации результатов
    '''

    layout1 = list(layout1.values())
    layout2 = list(layout2.values())
    layout3 = list(layout3.values())
    layout4 = list(layout4.values())

    fig = plt.figure(figsize=(15, 7))
    grid = fig.add_gridspec()

    # горизонтальная гистограмма
    ax1 = fig.add_subplot(grid[0, :])

    fingers = ['П Мизинец', 'П Безымянный', 'П Средний',
               'П Указательный', 'П Большой', 'Л большой',
               'Л Указательный', 'Л Средний', 'Л Безымянный',
               'Л Мизинец']
    index = np.arange(len(fingers))
    bar_width = 0.2

    for i in range(len(fingers)):
        ax1.barh(index[9 - i] + bar_width * 1.5,
                 layout1[i], bar_width, label='Йцукен'
                 if i == 0 else '', color=['#ff3333'], alpha=1.0)
        ax1.barh(index[9 - i] + bar_width * 0.5,
                 layout2[i], bar_width, label='Скоропис'
                 if i == 0 else '', color=['#99ff33'], alpha=1.0)
        ax1.barh(index[9 - i] - bar_width * 0.5,
                 layout3[i], bar_width, label='Вызов'
                 if i == 0 else '', color=['#0077ff'], alpha=1.0)
        ax1.barh(index[9 - i] - bar_width * 1.5,
                 layout4[i], bar_width, label='Диктор'
                 if i == 0 else '', color=['#b60aff'], alpha=1.0)

    ax1.set_xlabel('Количество нажатий')
    ax1.set_title('Анализ на основе файлов: ' + ', '.join(files))
    ax1.set_yticks(index)
    ax1.set_yticklabels(fingers)
    ax1.legend()

    # настройки и отображение
    fig.canvas.manager.set_window_title(
        'Сбор статистики для оптимизации русских раскладок\
 (количество нажатий)')

    plt.tight_layout()
    plt.show()
