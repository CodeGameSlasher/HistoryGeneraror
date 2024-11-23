from string import punctuation

from spellchecker import SpellChecker

spell = SpellChecker('ru')


def correct(text: str) -> str:
    # find those words that maybe misspelled
    misspelled = spell.unknown(text.translate(str.maketrans(' ', ' ', punctuation)).split(' '))

    correct_list: dict = {''.join({word}): spell.correction(word) for word in misspelled if
                          word != spell.correction(word)}
    print(correct_list)
    corrected_text = ''
    for word in text.lower().split():
        print(word)
        if word in correct_list.keys():
            corrected_text += correct_list.get(word) + ' '
        else:
            corrected_text += word + ' '
    return corrected_text.strip('\n\r ').capitalize()


if __name__ == "__main__":
    result = correct('Кагда тебя спать?')
    print(result)
