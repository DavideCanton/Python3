from functools import reduce
import operator

__author__ = 'Kami'


def prod(seq):
    return reduce(operator.mul, seq, 1)


def num(n):
    return prod((n + i) // i for i in range(1, n + 1))


if __name__ == "__main__":
    print(num(20))
