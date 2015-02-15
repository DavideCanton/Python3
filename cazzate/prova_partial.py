__author__ = 'davide'

from functools import partial, singledispatch


def f(x, y):
    return x - y


if __name__ == "__main__":
    print(f(2, 1))  # 1
    fp = partial(f, y=1)
    print(fp(5))  # 5