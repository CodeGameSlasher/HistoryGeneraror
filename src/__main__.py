from __init__ import *

from rich.console import Console

console = Console()
def cls(): console.clear()

words = WordList.from_file('src/words.txt')
generator = HistoryGenerator(words)

while True:
    cls()
    if len(generator.story) == 0:
        print(f'{len(generator.word_list)} слов')
    print(generator.story)
    print('Опции:')
    print('\t1. Генерировать слова(введите "1 {число_слов}" для большего числа новых слов за раз)')
    print('\t2. Выбор другого сида("2 {сид}", история будет очищена)')
    print('\t3. Выход')
    option = input('Выбор: ').split(' ')

    match option[0]:
        case '1':
            word_count = None if len(option) == 1 else int(option[1])
            generator.generate(word_count) if word_count else generator.generate()
        case '2':
            generator.set_seed(option[1])
        case '3':
            print('Пока!')
            exit()
        case _:
            generator.generate()