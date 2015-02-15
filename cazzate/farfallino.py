__author__ = 'davide'

import re


def trad(s):
    s = re.sub(r"([aeiou])", r"\1f\1", s)
    return re.sub(r"([AEIOU])", r"\1F\1", s)


if __name__ == "__main__":
    while True:
        try:
            s = input("Frase>")
        except EOFError:
            exit()
        else:
            print(trad(s))