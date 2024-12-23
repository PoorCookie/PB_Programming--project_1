'''
подключаемый файл с функциями,
необходимыми для подсчёта символов в файле, нагрузки на пальцы
'''
import matplotlib.pyplot as plt
import numpy as np


def characters_and_words_in_file_counter(filenames):
    '''
    получает: названия файлов
    возвращает словари:
    chars - 'символ': количество повторений
    words - 'слово': количество повторений
    '''

    chars = {}
    words = {}
    letters = (
        'аАбБвВгГдДеЕёЁжЖзЗиИйЙкКлЛмМнНоОп'
        'ПрРсСтТуУфФхХцЦчЧшШщЩъЪыЫьЬэЭюЮяЯ'
    )

    word_temp = ''

    for filename in filenames:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip(' ')
                for char in line:
                    if char in chars:
                        chars[char] += 1
                    else:
                        chars[char] = 1
                    if char in letters:
                        word_temp += char
                    elif word_temp != '':
                        if word_temp in words:
                            words[word_temp] += 1
                            word_temp = ''
                        else:
                            words[word_temp] = 1
                            word_temp = ''
                # добавление последнего слова, если оно есть
                # вынужденная мера, тк если строка кончается на слове,
                # оно не запишется, тк цикл записи запускается только после
                # того как встретится 'не буква'
                if word_temp != '':
                    if word_temp in words:
                        words[word_temp] += 1
                    else:
                        words[word_temp] = 1

    return chars, words


def combos_counter(words_dict, max_combos_length):
    '''
    получает:
    словарь - 'слово': количество повторений
    словарь - 'символ': 'сканкод клавиши'
    словарь - 'рука': 'скандкод клавиши'
    возвращает:
    словарь 'two_letters' - 'комбинация из 2х букв': количество потворений
    '''
    # combo_temp = ''
    combos = {}
    for current_combos_length in range(2, max_combos_length + 1):
        combos[current_combos_length] = {}

        for word, encounters in words_dict.items():
            if len(word) >= current_combos_length:
                for letter_number in range(
                        len(word) - current_combos_length + 1):
                    combo = ''
                    for i in range(current_combos_length):
                        combo += word[letter_number + i]

                    if combo in combos[current_combos_length]:
                        combos[current_combos_length][combo] += encounters
                    else:
                        combos[current_combos_length][combo] = encounters

    return combos


def conditional_combos_counter(
        whole_combos_dict, imported_layout_map, data, max_combos_length):
    '''
    получает:
    словарь - 'комбинация из 2х букв': количество повторений
    словарь - 'символ': 'сканкод клавиши'
    словарь - 'рука': 'скандкод клавиши'
    возвращает: словарь
    'two_letters_one_hand_combos' - 'комбинация из 2х букв':
    количество потворений
    '''
    za_hando = {}
    comfort = {}

    for combos_length in range(2, max_combos_length + 1):
        za_hando[combos_length] = {}
        comfort[combos_length] = {}

    for current_combos_length in range(2, max_combos_length + 1):
        combos_dict = whole_combos_dict[current_combos_length]
        for combo, encounters in combos_dict.items():
            for i in range(current_combos_length - 1):
                if (scancode_from_char(combo[i], imported_layout_map)
                    is None or scancode_from_char(
                        combo[i + 1], imported_layout_map) is None):
                    break
                if (key_from_value(scancode_from_char
                    (combo[i], imported_layout_map), data.key_hand)
                    != key_from_value(scancode_from_char
                    (combo[i + 1], imported_layout_map),
                        data.key_hand)):
                    break
            else:
                if combo in za_hando[current_combos_length]:
                    za_hando[current_combos_length][combo] += encounters
                else:
                    za_hando[current_combos_length][combo] = encounters
        for combo, encounters in za_hando[current_combos_length].items():
            for i in range(current_combos_length - 1):
                if (scancode_from_char(combo[i], imported_layout_map)
                    is None or scancode_from_char(
                        combo[i + 1], imported_layout_map) is None):
                    break
                if int(key_from_value(scancode_from_char(
                    combo[i], imported_layout_map), data.key_finger)[
                        3]) - int(key_from_value(scancode_from_char(
                        combo[i + 1], imported_layout_map),
                        data.key_finger)[3]) != 1:
                    break
            else:
                if combo in comfort[current_combos_length]:
                    comfort[current_combos_length][combo] += encounters
                else:
                    comfort[current_combos_length][combo] = encounters

    return za_hando, comfort


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

# def two_letters_scancodes_vychytator(letter1, letter2, imported_layout_map):
# return int(scancode_from_char(letter1, imported_layout_map)) -
# int(scancode_from_char(letter2, imported_layout_map))


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
    for finger, count in the_dict.items():
        print(f'{finger}: {count}')
    print('\n')


def formated_hands_result_out(the_dict):
    for finger, count in the_dict.items():
        print(f'{finger}: {count}%')
    print('\n')


def combos_dict_to_combos_count_dict(hand_combos, comfort_combos):
    hand_combos_count, comfort_combos_count = {}, {}
    for combos_length, combos in hand_combos.items():
        hand_combos_count[combos_length] = 0
        for combo, count in combos.items():
            hand_combos_count[combos_length] += count
    for combos_length, combos in comfort_combos.items():
        comfort_combos_count[combos_length] = 0
        for combo, count in combos.items():
            comfort_combos_count[combos_length] += count

    return hand_combos_count, comfort_combos_count


def formated_combos_results_out(hand_combos_count, comfort_combos_count):
    for (combos_length, count1), (count2) in zip(
            hand_combos_count.items(), comfort_combos_count.values()):
        print(f'буквенных сочетаний длины {combos_length}:')
        print(f'одноручных: {count1}\nудобных: {count2}\n')
    print('\n\n\n\n')


def total_sum_of_dict_values(the_dict):
    the_sum = 0
    for value in the_dict.values():
        the_sum += value
    # return the_sum
    print('количество одноручных двубуквенных сочетаний: ', the_sum, '\n\n')


# функция визуализации результатов
def visualization(
        layout1, layout2, layout3, layout4, files, hh1, hh2, hh3, hh4, dict1,
        dict2, dict3, dict4, dict5, dict6, dict7, dict8):

    layout1 = list(layout1.values())
    layout2 = list(layout2.values())
    layout3 = list(layout3.values())
    layout4 = list(layout4.values())

    hh1 = list(hh1.values())
    hh2 = list(hh2.values())
    hh3 = list(hh3.values())
    hh4 = list(hh4.values())

    # создаем фигуру с основным графиком и 4 круговыми диаграммами
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

    ax1.set_xlabel('')
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
        'Сбор статистики для оптимизации русских раскладок')

    # второе окно
    # Цвета для гистограммы
    colors = ['#ff3333', '#99ff33', '#0077ff', '#b60aff']
    labels = ['Йцукен', 'Скоропис', 'Вызов', 'Диктор']

    # Собираем данные в список для первой и второй гистограммы
    data_left = [dict1, dict2, dict3, dict4]
    data_right = [dict5, dict6, dict7, dict8]

    max_value = max(
        max(d.values()) for d in data_left + data_right
    )

    # Индексы для столбиков
    index = np.arange(len(dict1))  # Количество элементов в каждом словаре
    bar_width = 0.2  # Ширина столбиков

    # Создаем фигуру с двумя осями (левая и правая гистограммы)
    fig1, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(12, 6))

    # Построение гистограмм для левой части
    for i, d in enumerate(data_left):
        values = list(d.values())
        ax_left.barh(
            index + i * bar_width,
            values,
            color=colors[i],
            label=labels[i],
            height=bar_width)

    # Построение гистограмм для правой части
    for i, d in enumerate(data_right):
        values = list(d.values())
        ax_right.barh(
            index + i * bar_width,
            values,
            color=colors[i],
            label=labels[i],
            height=bar_width)

    # Настройка осей
    ax_left.set_xlabel('Количество сочетаний')
    ax_left.set_ylabel('Длина сочетания')
    ax_right.set_xlabel('Количество сочетаний')
    ax_right.set_ylabel('Длина сочетания')

    # Настройка положения меток на оси Y для обеих гистограмм
    ax_left.set_yticks(index + bar_width * (len(data_left) - 1) / 2)
    ax_left.set_yticklabels(list(dict1.keys()))
    ax_right.set_yticks(index + bar_width * (len(data_right) - 1) / 2)
    ax_right.set_yticklabels(list(dict5.keys()))

    # Добавление подписей под гистограммами
    ax_left.set_title('Одноручные сочетания', fontsize=14)
    ax_right.set_title('Одноручные удобные сочетания', fontsize=14)

    # Перемещение легенды в нижнюю часть окна
    # ax_left.legend(loc='upper center', ncol=4, bbox_to_anchor=(0.5, -0.15))
    # ax_right.legend(loc='upper center', ncol=4, bbox_to_anchor=(0.5, -0.15))

    # Инвертирование оси Y для обеих гистограмм (чтобы столбики шли снизу
    # вверх)
    ax_left.invert_yaxis()
    ax_right.invert_yaxis()

    # Устанавливаем одинаковый предел для оси X для обеих гистограмм
    ax_left.set_xlim(0, max_value)
    ax_right.set_xlim(0, max_value)

    plt.tight_layout()
    plt.show()
