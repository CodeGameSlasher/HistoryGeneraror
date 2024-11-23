from time import time
from json import loads, dumps
from random import choice, seed

from rich.console import Console
from speakerpy.lib_speak import Speaker
from speakerpy.lib_sl_text import SeleroText

console = Console()
def cls(): console.clear()

class Voicer(Speaker):
    def __init__(self, model='v3_1_ru', lang='ru', actor='kseniya', engine='hip'):
        super().__init__(model, lang, actor, engine)

    def correct_text(self, text):
        text = SeleroText(text, self.language).text
        return text
    
    def say(self, text, samplerate=48000):
        for chunk in SeleroText(text, self.language).chunk():
            self.speak(chunk, samplerate)


class WordList(list[str]):
    def __init__(self, words: list[str]):
        words = [word.strip('\n\r\t ') for word in words if word]
        self.extend(words)

    @classmethod
    def from_file(cls, filename: str = 'words.txt', encoding: str = 'utf-8'):
        for encode in [encoding, 'utf-8', 'windows-1251']:
            try:
                with open(filename, 'r', encoding=encode) as file:
                    words = [loads(dumps(dict(word=word), ensure_ascii=False)).get('word') for word in file.readlines()]
                    break
            except Exception as e:
                console.print(f'[red]{e}')

        with open('log', 'w') as file:
            file.write(f'Last encoding: {encode}\nLength: {len(words)}')
        
        return cls(words)
    
    def save_to_file(self, filename: str = 'words.txt', encoding = 'utf-8'):
        with open(filename, 'w', encoding=encoding) as file:
            file.write('\n'.join(self))

class History(list[str]):
    def __init__(self, history: list[str] = []):
        self.extend(history)

    def __str__(self):
        return '' if len(self) < 0 else ' '.join(self).strip().replace('  ', ' ').capitalize()

class HistoryGenerator:
    def __init__(self, words: WordList):
        self.words = words
        self.history = History()
        self.seed = int(time() + len(words))

    @property
    def story(self):
        return str(self.history)
    
    @property
    def word_list(self):
        return self.words.copy()
    
    def set_seed(self, value: str):
        if not isinstance(value, int):
            self.seed = int.from_bytes(bytes(value, encoding='utf-8') if isinstance(value, str) else bytes(value))
        self.history = History()
        seed(self.seed)
    
    def generate(self, word_count: int = 1):
        if word_count < 0:
            raise ValueError(f'{word_count} < 0!')
        else:
            self.history.extend(choice(self.words) for _ in range(word_count))
        return self.story
        

if __name__ == '__main__':
    speaker = Voicer()
    words = WordList.from_file()
    generator = HistoryGenerator(words)

    while True:
        cls()
        if len(generator.story) == 0:
            console.print(f'{len(generator.word_list)} слов')
        console.print(generator.story)
        console.print('Опции:')
        console.print('\t1. Генерировать слова(введите "1 {число_слов}" для большего числа новых слов за раз)')
        console.print('\t2. Выбор другого сида("2 {сид}", история будет очищена)')
        console.print('\t3. Проговорить')
        console.print('\t4. Выход')
        option = input('Выбор: ').split(' ')

        match option[0]:
            case '1':
                word_count = None if len(option) == 1 else int(option[1])
                generator.generate(word_count) if word_count else generator.generate()
            case '2':
                generator.set_seed(option[1])
            case '3':
                speaker.say(generator.story)
            case '4':
                console.print('Пока!')
                exit()
            case _:
                generator.generate()
