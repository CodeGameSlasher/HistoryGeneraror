from string import punctuation, ascii_letters

cyrillic_letters = u"абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

def sort_text(text: str):
    data = ''.join(symbol if symbol in cyrillic_letters else '\n' for symbol in text).splitlines()
    data = list(set(data))
    data = sorted(data, key=str.lower)
    data = [word for word in data if word not in ['', ' ']]

    return '\n'.join(data)

def sort_file(filename: str = 'words.txt', encoding: str = 'utf-8'):
    with open(filename, 'r', encoding=encoding) as file:
        text = sort_text(file.read())

    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)
        file.truncate()

        print(f'{len(text.splitlines())} слов')

if __name__ == '__main__':
    sort_file()