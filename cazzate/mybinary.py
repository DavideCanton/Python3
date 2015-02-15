import inspect
import itertools as it
from functools import wraps


def comb(n, k):
    return ("".join(map(str, number))
            for number in it.product((0, 1), repeat=n)
            if sum(number) == k)


def bin_args(n):
    return (list(map(int, list(("{:0>" + str(n) + "}").format(bin(i)[2:]))))
            for i in range(1 << n))


def pretty(func, n):
    for args in bin_args(n):
        print(str(args)[1:-1], ':-', func(*args))


def toint(b):
    return int(''.join(map(str, b)), 2)


def maptobool(func):
    @wraps(func)
    def wrapper(*a, **kw):
        a = tuple(map(bool, a))
        return func(*a, **kw)

    return wrapper


@maptobool
def f(a, b, c):
    return a and b or not c


if __name__ == '__main__':
    print(list(comb(3, 1)))
    print(list(bin_args(4)))
    pretty(f, 3)
