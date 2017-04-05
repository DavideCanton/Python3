from functools import reduce

__author__ = 'Davide'

COINS = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2]

MAX = [int(2 / i) for i in COINS]


def incr(n, MAX):
    i = -1
    while i >= -len(n) and n[i] == MAX[i]:
        n[i] = 0
        i -= 1
    n[i] += 1


if __name__ == "__main__":
    p = reduce(lambda a, b: a * b, MAX, 1)
    n = [0] * len(COINS)
    count = 0
    for i in range(p):
        s = sum(a * b for a, b in zip(n, COINS))
        if s == 2:
            count += 1
        incr(n, MAX)
        #print(n)
    print(count)