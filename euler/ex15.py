import operator
from functools import reduce

__author__ = 'Kami'


def prod(seq):
    return reduce(operator.mul, seq, 1)


def num(n):
    return prod(n // i + 1 for i in range(1, n + 1))


if __name__ == "__main__":
    print(num(20))
