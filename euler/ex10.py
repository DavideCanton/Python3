__author__ = 'Kami'

from heapq import *


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


if __name__ == "__main__":
    limit = 2E6
    s = 0
    for prime in genera_primi():
        if prime >= limit:
            break
        s += prime
    print(s)