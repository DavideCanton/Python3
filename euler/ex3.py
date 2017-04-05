# coding=utf-8

"""
Calcolare il fattore primo più grande di 600851475143
"""

__author__ = 'davide'

from euler._utils import genera_primi
import math


def ex3(n):
    top = math.ceil(math.sqrt(n))

    for m in genera_primi():
        while not n % m:
            yield m
            n //= m
            top = math.ceil(math.sqrt(n))

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
