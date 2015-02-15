__author__ = 'Davide'

DEFAULTS = {
    1: 'one',
    2: 'two',
    3: 'three',
    4: 'four',
    5: 'five',
    6: 'six',
    7: 'seven',
    8: 'eight',
    9: 'nine',
    10: 'ten',
    11: 'eleven',
    12: 'twelve',
    13: 'thirteen',
    14: 'fourteen',
    15: 'fifteen',
    16: 'sixteen',
    17: 'seventeen',
    18: 'eighteen',
    19: 'nineteen',
    20: 'twenty',
    30: 'thirty',
    40: 'forty',
    50: 'fifty',
    60: 'sixty',
    70: 'seventy',
    80: 'eighty',
    90: 'ninety',
    100: 'hundred',
    1000: 'thousand'
}


def wordize(n):
    print(n, end=" ")
    s = []
    if n >= 1000:
        r = n // 1000
        s.append(DEFAULTS[r] + " " + DEFAULTS[1000])
        n %= 1000

    if n >= 100:
        r = n // 100
        s.append(DEFAULTS[r] + " " + DEFAULTS[100])
        n %= 100

    if n in DEFAULTS:
        s.append(DEFAULTS[n])
    elif n:
        s.append(DEFAULTS[n // 10 * 10] + DEFAULTS[n % 10])

    res = " and ".join(s)
    print(res)
    return res


def len_no_spaces(s):
    return len(s.replace(" ", ""))


if __name__ == "__main__":
    print(sum(len_no_spaces(wordize(n)) for n in range(1, 1001)))
