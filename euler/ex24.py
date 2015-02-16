__author__ = 'davide'

from itertools import permutations


def main():
    s = "0123456789"
    for i, p in enumerate(permutations(s), start=1):
        if i == 1000000:
            print("".join(p))
            break


if __name__ == "__main__":
    main()