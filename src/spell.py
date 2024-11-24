from string import punctuation
from random import choice

from spellchecker import SpellChecker

spell = SpellChecker('ru')


def correct(text: str) -> str:
    # find those words that maybe misspelled
    misspelled = spell.unknown(text.translate(str.maketrans(' ', ' ', punctuation)).split(' '))

    correct_list: dict[str, str] = {''.join({word}): spell.correction(word) for word in misspelled if word != spell.correction(word) and isinstance(spell.correction(word), str)}

    corrected_text = ''
    for word in text.lower().split():
        word = word.translate(str.maketrans(' ', ' ', punctuation))
        if correct_list.get(word):
            corrected_text += correct_list.get(word) + ' '
        else:
            corrected_text += word + ' '
    return corrected_text.strip('\n\r ').capitalize()


if __name__ == "__main__":
    result = correct('Алло, Всж')
    print(result)
