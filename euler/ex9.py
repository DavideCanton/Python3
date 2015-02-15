__author__ = 'Kami'

import itertools as it


def find_triplet():
    for c in it.count(5):
        for b in range(1, c):
            for a in range(1, b):
                if a * a + b * b == c * c and a + b + c == 1000:
                    return a, b, c


if __name__ == "__main__":
    a, b, c = find_triplet()
    print(a * b * c)
