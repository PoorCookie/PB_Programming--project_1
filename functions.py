'''
подключаемый файл с функциями,
необходимыми для подсчёта символов в файле,
нагрузки на пальцы, визуализации результатов
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
    возвращает:
    словарь 'final_fingers_load' - 'палец': нагрузка
    словарь 'final_hands_load' - 'рука': нагрузка
    '''

    # возвращаемый словарь
    final_fingers_load = {
        'lfi5': 0,
        'lfi4': 0,
        'lfi3': 0,
        'lfi2': 0,
        # 'lfi1': 0,
        # 'rfi1': 0,
        'rfi2': 0,
        'rfi3': 0,
        'rfi4': 0,
        'rfi5': 0
    }
    final_hands_load = {}
    lcounter = 0
    rcounter = 0

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

    for key, value in final_fingers_load.items():
        if 'l' in key:
            lcounter += value
        if 'r' in key:
            rcounter += value

    if lcounter > 0 and rcounter > 0:
        final_hands_load['lh'] = round(lcounter / (lcounter + rcounter) * 100)
        final_hands_load['rh'] = round(rcounter / (lcounter + rcounter) * 100)
    elif rcounter > 0:
        final_hands_load['rh'] = 100
    elif lcounter > 0:
        final_hands_load['lh'] = 100

    return final_fingers_load, final_hands_load


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


def formated_hands_result_out(the_dict):
    '''
    получает:
    словарь - 'рука': нагрузка на неё
    выводит:
    форматированное содержание словаря в консоль
    '''
    for finger, count in the_dict.items():
        print(f'{finger}: {count}%')
    print('\n')


# функция визуализации результатов
def visualization(
        layout1, layout2, layout3, layout4, files, hh1, hh2, hh3, hh4):

    layout1 = list(layout1.values())
    layout2 = list(layout2.values())
    layout3 = list(layout3.values())
    layout4 = list(layout4.values())

    hh1 = list(hh1.values())
    hh2 = list(hh2.values())
    hh3 = list(hh3.values())
    hh4 = list(hh4.values())

    fig = plt.figure(figsize=(15, 7))
    grid = fig.add_gridspec(2, 4, height_ratios=[2, 1])

    # горизонтальная гистограмма
    ax1 = fig.add_subplot(grid[0, :])

    fingers = ['П Мизинец', 'П Безымянный', 'П Средний',
               'П Указательный', 'Л Указательный',
               'Л Средний', 'Л Безымянный', 'Л Мизинец']
    index = np.arange(len(fingers))
    bar_width = 0.2

    for i in range(len(fingers)):
        ax1.barh(index[7 - i] + bar_width * 1.5,
                 layout1[i], bar_width, label='Йцукен'
                 if i == 0 else '', color=['#ff3333'], alpha=1.0)
        ax1.barh(index[7 - i] + bar_width * 0.5,
                 layout2[i], bar_width, label='Скоропис'
                 if i == 0 else '', color=['#99ff33'], alpha=1.0)
        ax1.barh(index[7 - i] - bar_width * 0.5,
                 layout3[i], bar_width, label='Вызов'
                 if i == 0 else '', color=['#0077ff'], alpha=1.0)
        ax1.barh(index[7 - i] - bar_width * 1.5,
                 layout4[i], bar_width, label='Диктор'
                 if i == 0 else '', color=['#b60aff'], alpha=1.0)

    ax1.set_xlabel('Величина штрафа')
    ax1.set_title('Анализ на основе файлов: ' + ', '.join(files))
    ax1.set_yticks(index)
    ax1.set_yticklabels(fingers)
    ax1.legend()

    # круговые диаграммы
    labels = ['Левая рука', 'Правая рука']
    axs = [fig.add_subplot(grid[1, i]) for i in range(4)]

    hh_values = [hh1, hh2, hh3, hh4]
    hh_titles = ['Йцукен', 'Скоропис', 'Вызов', 'Диктор']
    pie_colors = ['#30d5c8', '#ff0033']

    for i, ax in enumerate(axs):
        ax.pie(hh_values[i], labels=labels, autopct='%1.1f%%',
               startangle=90, colors=pie_colors)
        ax.set_title(hh_titles[i], fontdict={'fontweight':
                                             'bold', 'fontsize': 12})

    # настройки и отображение
    fig.canvas.manager.set_window_title(
        'Сбор статистики для оптимизации русских раскладок\
 (величина штрафов и нагрузка на руки)')

    plt.tight_layout()
    plt.show()
