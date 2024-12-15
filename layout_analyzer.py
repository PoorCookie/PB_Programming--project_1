import qwerty_one

def count_characters_in_file(filename):
    char_count = {}
    
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            for char in line:
                if char in char_count:
                    char_count[char] += 1
                else:
                    char_count[char] = 1
    
    return char_count

if __name__ == "__main__":
    char_dict = count_characters_in_file('voina-i-mir.txt')
    finger_dict = qwerty_one.process(char_dict)
    for finger, count in finger_dict.items():
        print(f"{finger}: {count}")

#print (char_dict)