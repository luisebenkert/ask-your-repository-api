import random

class TypoGenerator:
    proximities = {
        'a': ['q', 'w', 's', 'y'],
        'b': ['v', 'g', 'h', 'n'],
        'c': ['x', 'd', 'f', 'v'],
        'd': ['s', 'e', 'r', 'f', 'c', 'x'],
        'e': ['w', 's', 'd', 'r'],
        'f': ['d', 'r', 't', 'g', 'v', 'c'],
        'g': ['f', 't', 'z', 'h', 'b', 'v'],
        'h': ['g', 'z', 'u', 'j', 'n', 'b'],
        'i': ['u', 'j', 'k', 'l', 'o'],
        'j': ['h', 'u', 'i', 'k', 'm', 'n'],
        'k': ['j', 'i', 'o', 'l', 'm'],
        'l': ['k', 'o', 'p',],
        'm': ['n', 'j', 'k'],
        'n': ['b', 'h', 'j', 'm'],
        'o': ['i', 'k', 'l', 'p'],
        'p': ['o', 'l'],
        'q': ['w', 'a', 's'],
        'r': ['e', 'd', 'f', 't'],
        's': ['a', 'w', 'e', 'd', 'x', 'y'],
        't': ['r', 'f', 'g', 'z'],
        'u': ['z', 'h', 'j', 'i'],
        'v': ['c', 'f', 'g', 'b'],
        'w': ['q', 'a', 's', 'e'],
        'x': ['y', 's', 'd', 'c'],
        'y': ['a', 's', 'x'],
        'z': ['t', 'g', 'h', 'u'],
    }

    def letter_missed(word):
        if len(word) < 2:
            return
        index = random.randint(0, len(word)-1)
        typo = word[:index] + word[index + 1:]
        return typo

    def letter_doubled(word):
        index = random.randint(0, len(word)-1)
        letter = word[index]
        typo = word[:index] + letter + word[index:]
        return typo

    def letter_swapped(word):
        if len(word) < 2:
          return
        index = random.randint(0, len(word)-2)
        first = word[index]
        second = word[index + 1]
        typo = word[:index] + second + first + word[index + 2:]
        return typo

    def key_missed(word):
        index = random.randint(0, len(word)-1)
        letter = word[index]
        prox = TypoGenerator.proximities[letter]
        key = prox[random.randint(0, len(prox)-1)]
        typo = word[:index] + key + word[index + 1:]
        return typo

    def key_added(word):
        index = random.randint(0, len(word)-1)
        letter = word[index]
        prox = TypoGenerator.proximities[letter]
        key = prox[random.randint(0, len(prox)-1)]
        typo = word[:index] + key + word[index:]
        return typo