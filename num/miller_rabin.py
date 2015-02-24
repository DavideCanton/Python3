import random
from math import floor

__author__ = 'davide'


def is_prime_mr(n, k=100):
    if n < 2:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    s = 0
    d = n - 1
    while d & 1 == 0:
        s += 1
        d >>= 1

    for _ in range(k):
        a = int(2 + random.random() * (n - 3))
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = (x * x) % n
            if x == 1:
                return False
            if x == n - 1:
                break
        else:
            return False

    return True


def is_prime(n):
    if n < 2:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    for i in range(3, floor(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False

    return True


def main():
    r = []
    for i in range(2, 200000):
        a = is_prime(i)
        b = is_prime_mr(i)
        if a != b:
            r.append((i, a, b))
    print(r)


if __name__ == "__main__":
    main()