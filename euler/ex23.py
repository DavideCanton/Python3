from functools import lru_cache

__author__ = 'davide'

from math import floor


def sum_divisors(n):
    s = 1
    l = floor(n ** 0.5) + 1
    for i in range(2, l):
        if n % i == 0:
            s += i
            if i != n // i:
                s += n // i
    return s


@lru_cache(None)
def is_abundant(x):
    return sum_divisors(x) > x


def get_ab_sum(n):
    for i in range(1, n // 2 + 1):
        if is_abundant(i) and is_abundant(n - i):
            return i, n - i
    return None


def main():
    s = 0
    for i in range(1, 28124):
        res = get_ab_sum(i)
        if not res:
            # print(i, "ok")
            s += i
        else:
            # print(i, res)
            pass
    print(s)


if __name__ == "__main__":
    main()