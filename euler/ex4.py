__author__ = 'davide'

import itertools as it


def is_palindrome(n):
    s = str(n)
    return s == s[::-1]


def ex4():
    m = 0
    for i in range(999, 0, -1):
        for j in range(999, 0, -1):
            p = i * j
            if is_palindrome(p) and p > m:
                m = p
    return m


if __name__ == "__main__":
    print(ex4())