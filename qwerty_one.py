def process(char_dict):
    """
    функция принимающая словарь: символ - ключ,
    их встреченное количество - значение;
    отдаёт словарь fins: палец -- нагрузка
    """

    # символы которые только с шифтом
    shift_symbs = '!\"№;%:?*()_+,ЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ'

    # возвращаемый словарь палец -- нагрузка
    fins = {
        'lfi2': 0,
        'lfi3': 0,
        'lfi4': 0,
        'lfi5': 0,
        'rfi2': 0,
        'rfi3': 0,
        'rfi4': 0,
        'rfi5': 0,
        'thumb': 0,
        #        'left': 0,
        #        'right': 0
    }

    # вес каждой клавиши, согласно её позиции
    complex_map = {
        'ё1234567890-=!\"№;%:?*()_+': 3,
        'йцукенгшщзхъячсмитьбю.,': 2
    }

    # позиция каждого символа (для нажатого мизинцем шифта)
    side_map = {
        ';%45кеапми№3увс\"2цыч!1ёйфя': 'r',
        ':?67нртгоь*8шлб(9щдю)_+,0-=зж.хэъ': 'l'
    }

    # символ -- палец
    fin_map = {
        ';%45кеапми': 'lfi2',
        '№3увс': 'lfi3',
        '\"2цыч': 'lfi4',
        '!1ёйфя': 'lfi5',
        ':?67нртгоь': 'rfi2',
        '*8шлб': 'rfi3',
        '(9щдю': 'rfi4',
        ')_+,0-=зж.хэъ': 'rfi5',
        ' ': 'thumb'
    }

    # прогонка полученного словаря через критерии, заполнение словаря fins
    for char, count in char_dict.items():
        if char in shift_symbs:
            char_lower = char.lower()
            finger = what_finger(char_lower, fin_map)
            if finger:
                compl = what_complex(char_lower, complex_map)
                fins[finger] += count * compl
                side = what_side(char_lower, side_map)
                for finger, value in fins.items():
                    if side in finger and '5' in finger:
                        fins[finger] += count
        else:
            finger = what_finger(char, fin_map)
            if finger:
                compl = what_complex(char, complex_map)
                fins[finger] += count * compl

#    for finger, value in fins.items():
#        if 'l' in finger:
#            fins['left'] += finger[]
#        if 'r' in finger:
#            fins['right'] += value
    return fins


def what_finger(char, fin_map):
    """
    получает: символ и карту символы -- палец;
    отдаёт: соответствующий палец
    """
    for symbols, finger in fin_map.items():
        if char in symbols:
            return finger
    return None


def what_side(char, side_map):
    """
    получает: символ и карту символы -- сторона;
    отдаёт: соответствующую сторону
    """
    for symbols, side in side_map.items():
        if char in symbols:
            return side


def what_complex(char, complex_map):
    """получает: символ и карту символы -- вес; отдаёт: соответствующий вес"""
    for symbols, compl in complex_map.items():
        if char in symbols:
            return compl
    return 1
