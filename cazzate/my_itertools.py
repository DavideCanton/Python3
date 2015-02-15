__author__ = 'davide'

import itertools as it
import functools as ft
import random


def iterate(func, nums, acc=0):
    acc_func = lambda acc, _: func(acc)
    return ft.reduce(acc_func, range(nums), acc)


def bounds(iterable, key=None):
    if key is None:
        key = lambda x: x

    start = list(it.islice(iterable, 0, 1))[0]

    def acc_func(acc, val):
        m, M = acc
        val = key(val)
        if val < m:
            m = val
        if val > M:
            M = val
        return m, M

    return ft.reduce(acc_func, iterable, (start, start))


if __name__ == "__main__":
    l = random.sample(range(10 ** 9), 10 ** 3)
    print(bounds(l))