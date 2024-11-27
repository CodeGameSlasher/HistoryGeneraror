from __init__ import *

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
