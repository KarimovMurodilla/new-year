"""
Проверка текста на кириллице
"""


def all_ru(word):
    for letter in word:
        code = ord(letter)
        if not(1040 <= code <= 1103) and code != 1025 and code != 1105 and code != 32:
            # print(letter)
            return False
    return True