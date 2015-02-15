__author__ = 'davide'

from heapq import heappush, heapreplace
from math import *
import time


def is_perfect(num):
    somma = 1
    for k in range(2, int(ceil(num ** 0.5))):
        if num % k == 0:
            somma = somma + k + num / k
    if num ** 0.5 % 1 == 0:
        somma += num ** 0.5
    return somma == num


def find_perfect(limit):
    results = []
    k = 1
    while len(results) < limit:
        j = 2 ** k * (2 ** (k + 1) - 1)
        if is_perfect(j):
            results.append(j)
        k += 1

    return results


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


def find_perfect2(limit):
    results = []
    for p in genera_primi():
        if len(results) == limit:
            break
        n = (1 << p) - 1
        n <<= p - 1
        if is_perfect(n):
            results.append(n)
    return results


def main():
    t = time.time()
    res = find_perfect(8)
    t = time.time() - t
    print(t, res)

    t = time.time()
    res = find_perfect2(8)
    t = time.time() - t
    print(t, res)


if __name__ == "__main__":
    main()