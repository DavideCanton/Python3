# coding=utf-8

"""
Calcolare il fattore primo più grande di 600851475143
"""

__author__ = 'davide'

from math import sqrt

from heapq import heappush, heapreplace
from math import *


def genera_primi():
    yield 2
    todel = [(4, 2)]
    n = 3
    while True:
        if todel[0][0] != n:
            yield n
            heappush(todel, (n * n, n))
        else:
            while todel[0][0] == n:
                p = todel[0][1]
                heapreplace(todel, (n + p, p))
        n += 1


def ex3(n):
    top = ceil(sqrt(n))

    for m in genera_primi():
        while not n % m:
            yield m
            n //= m
            top = ceil(sqrt(n))

        if m > top:
            if n != 1:
                yield n
            return

if __name__ == "__main__":
    n = 600851475143
    p = 1
    for d in ex3(n):
        print(d, end=" ")
        p *= d
    assert p == n
