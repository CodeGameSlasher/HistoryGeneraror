from time import time
from json import loads, dumps
from random import choice, seed

class WordList(list[str]):
    def __init__(self, words: list[str]):
        [self.append(word.strip('\n\r\t ')) for word in words if word]

    @classmethod
    def from_file(cls, filename: str = 'words.txt', encoding: str = 'utf-8'):
        for encode in [encoding, 'utf-8', 'windows-1251']:
            try:
                with open(filename, 'r', encoding=encode) as file:
                    words = file.readlines() if encode == 'utf-8' else [loads(dumps(dict(word=word), ensure_ascii=False)).get('word') for word in file.readlines()]
                    break
            except Exception as e:
                continue
        else:
            raise FileNotFoundError(f'Word list file not found in {filename} with supported encodings.')
        
        return cls(words)
    
    def save_to_file(self, filename: str = 'words.txt', encoding = 'utf-8'):
        with open(filename, 'w', encoding=encoding) as file:
            file.write('\n'.join(self))

class History(list[str]):
    def __init__(self, history: list[str] = []):
        [self.append(item) for item in history]

    def __str__(self):
        return '' if len(self) < 0 else ' '.join(self).strip().replace('  ', ' ').capitalize()

class HistoryGenerator:
    def __init__(self, words: WordList, history: History = History()):
        self.words = words
        self.history = history
        self.seed = int(time() + len(words))

    @property
    def story(self):
        return str(self.history)
    
    @story.setter
    def set_story(self, story: History):
        self.history = story
    
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