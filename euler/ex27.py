from functools import lru_cache
from math import ceil

__author__ = 'Davide'


@lru_cache(None)
def is_prime(n):
    if n != 2 and n % 2 == 0:
        return False
    for i in range(2, ceil(n ** 0.5)):
        if n % i == 0:
            return False
    return True


def prime_count(a, b):
    for n in range(0, 1000):
        v = n * (n + a) + b
        if v < 0:
            return 0
        if not is_prime(v):
            return n
    return None


def main():
    nmax = 0
    ma, mb = -1, -1
    for a in range(-1000, 1001):
        for b in range(-1000, 1001):
            n = prime_count(a, b)
            if n > nmax:
                nmax = n
                ma, mb = a, b
    print(ma, mb, ma * mb)


if __name__ == "__main__":
    main()
    print(is_prime.cache_info())