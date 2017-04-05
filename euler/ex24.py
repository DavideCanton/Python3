__author__ = 'davide'

from itertools import permutations, islice


def main():
    s = "0123456789"
    p = "".join(next(islice(permutations(s), 1000000, 1000001)))
    print(p)

if __name__ == "__main__":
    main()