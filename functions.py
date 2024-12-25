'''
подключаемый файл с функциями,
необходимыми для подсчёта символов в файле,
нагрузки на пальцы, визуализации результатов
'''
import matplotlib.pyplot as plt
import numpy as np


def file_to_words_set(filename):
    '''
    получает:
    название файла
    возвращает:
    множество 'words_set'
    '''

    words_set = set()
    letters = (
        'аАбБвВгГдДеЕёЁжЖзЗиИйЙкКлЛмМнНоОп'
        'ПрРсСтТуУфФхХцЦчЧшШщЩъЪыЫьЬэЭюЮяЯ'
    )

    word_temp = ''

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip(' ')
            for char in line:
                if char in letters:
                    word_temp += char
                elif word_temp != '':
                    if word_temp not in words_set:
                        words_set.add(word_temp)
                        word_temp = ''

            # добавление последнего слова, если оно есть
            # вынужденная мера, тк если строка кончается на слове,
            # оно не запишется, тк цикл записи запускается только после
            # того как встретится 'не буква'
            if word_temp != '':
                if word_temp not in words_set:
                    words_set.add(word_temp)

    return words_set


def combos_counter(words_set):
    '''
    получает:
    множество со словами
    возвращает:
    словарь 'combos' - '2': 'комбинации' : количество повторений
    '''

    current_combos_length = 2
    combos = {}
    combos[current_combos_length] = {}

    for word in words_set:
        if len(word) >= current_combos_length:
            for letter_number in range(len(word) - current_combos_length + 1):
                combo = ''
                for i in range(current_combos_length):
                    combo += word[letter_number + i]

                if combo not in combos[current_combos_length]:
                    combos[current_combos_length][combo] = 1

    return combos


def conditional_combos_counter(
        whole_combos_dict, imported_layout_map, data, max_combos_length):
    '''
    получает:
    словарь - 'комбинация из 2х букв': количество повторений
    словарь - 'символ': 'сканкод клавиши'
    файл со словарями соответствия сканкодов - цены/пальца
    переменная - максимальная длина комбинации
    возвращает:
    словарь 'za_hando' - длина комбинации: 'комбинация': количество потворений
    ^для одноручных комбинаций
    словарь 'comfort' - длина комбинации: 'комбинация': количество потворений
    ^для одноручных удобных комбинаций
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


def combos_dict_to_combos_count_dict(hand_combos, comfort_combos):
    '''
    получает:
    словарь - 'рука': нагрузка на неё
    выводит:
    словарь 'hand_combos_count' - длина комбо: количество
    словарь 'comfort_combos_count' - длина комбо: количество
    '''
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


def visualization(
        dict1, dict2, dict3, dict4, dict5, dict6, dict7, dict8):
    '''
    функция визуализации результатов
    '''

    # цвета для гистограммы
    colors = ['#ff3333', '#a33333']
    labels = ['1grams', 'sortchbukw']

    data_left = [dict1, dict2]
    data_right = [dict3, dict4]

    max_value = max(
        max(d.values()) for d in data_left + data_right
    )

    # индексы для столбиков
    index = np.arange(len(dict1))  # Количество элементов в каждом словаре
    bar_width = 0.2  # Ширина столбиков

    # создание фигуры с двумя осями (левая и правая гистограммы)
    fig1, (ax_left1, ax_right1) = plt.subplots(1, 2, figsize=(12, 6))
    fig1.suptitle("Йцукен", fontsize=16)

    # построение гистограмм для левой части
    for i, d in enumerate(data_left):
        values = list(d.values())
        ax_left1.barh(
            index + i * bar_width,
            values,
            color=colors[i],
            label=labels[i],
            height=bar_width)

    # построение гистограмм для правой части
    for i, d in enumerate(data_right):
        values = list(d.values())
        ax_right1.barh(
            index + i * bar_width,
            values,
            color=colors[i],
            label=labels[i],
            height=bar_width)

    # настройка осей
    ax_left1.set_xlabel('Количество сочетаний')
    ax_left1.set_ylabel('Длина сочетания')
    ax_right1.set_xlabel('Количество сочетаний')
    ax_right1.set_ylabel('Длина сочетания')

    # настройка положения меток на оси Y для обеих гистограмм
    ax_left1.set_yticks(index + bar_width * (len(data_left) - 1) / 2)
    ax_left1.set_yticklabels(list(dict1.keys()))
    ax_right1.set_yticks(index + bar_width * (len(data_right) - 1) / 2)
    ax_right1.set_yticklabels(list(dict5.keys()))

    # добавление подписей под гистограммами
    ax_left1.set_title('Одноручные сочетания', fontsize=14)
    ax_right1.set_title('Одноручные удобные сочетания', fontsize=14)

    # инвертирование оси Y для обеих гистограмм (чтобы столбики шли снизу
    # вверх)
    ax_left1.invert_yaxis()
    ax_right1.invert_yaxis()

    # устанавливаем одинаковый предел для оси X для обеих гистограмм
    ax_left1.set_xlim(0, max_value)
    ax_right1.set_xlim(0, max_value)

    # цвета для гистограммы
    colors = ['#0077ff', '#00777f']
    labels = ['1grams', 'sortchbukw']

    data_left = [dict5, dict6]
    data_right = [dict7, dict8]

    max_value = max(
        max(d.values()) for d in data_left + data_right
    )

    # индексы для столбиков
    index = np.arange(len(dict1))  # Количество элементов в каждом словаре
    bar_width = 0.2  # Ширина столбиков

    ax_right1.legend(loc='upper right')

    # создание фигуры с двумя осями (левая и правая гистограммы)
    fig2, (ax_left2, ax_right2) = plt.subplots(1, 2, figsize=(12, 6))
    fig2.suptitle("Вызов", fontsize=16)

    # построение гистограмм для левой части
    for i, d in enumerate(data_left):
        values = list(d.values())
        ax_left2.barh(
            index + i * bar_width,
            values,
            color=colors[i],
            label=labels[i],
            height=bar_width)

    # построение гистограмм для правой части
    for i, d in enumerate(data_right):
        values = list(d.values())
        ax_right2.barh(
            index + i * bar_width,
            values,
            color=colors[i],
            label=labels[i],
            height=bar_width)

    # настройка осей
    ax_left2.set_xlabel('Количество сочетаний')
    ax_left2.set_ylabel('Длина сочетания')
    ax_right2.set_xlabel('Количество сочетаний')
    ax_right2.set_ylabel('Длина сочетания')

    # настройка положения меток на оси Y для обеих гистограмм
    ax_left2.set_yticks(index + bar_width * (len(data_left) - 1) / 2)
    ax_left2.set_yticklabels(list(dict1.keys()))
    ax_right2.set_yticks(index + bar_width * (len(data_right) - 1) / 2)
    ax_right2.set_yticklabels(list(dict5.keys()))

    # добавление подписей под гистограммами
    ax_left2.set_title('Одноручные сочетания', fontsize=14)
    ax_right2.set_title('Одноручные удобные сочетания', fontsize=14)

    # инвертирование оси Y для обеих гистограмм (чтобы столбики шли снизу
    # вверх)
    ax_left2.invert_yaxis()
    ax_right2.invert_yaxis()

    # устанавливаем одинаковый предел для оси X для обеих гистограмм
    ax_left2.set_xlim(0, max_value)
    ax_right2.set_xlim(0, max_value)

    ax_right2.legend(loc='upper right')

    plt.show()
