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
    for i in range(2000):
        n = 2 + int(
            random.random() *
            3872985723985723985729357248933872985723985572935724893387298572398)
        n |= 1
        print("Trying", n, end="-", flush=True)
        a = is_prime(n)
        print("1", end="-", flush=True)
        b = is_prime_mr(n)
        print("2")
        if a != b:
            r.append((n, a, b))
    print(r)


if __name__ == "__main__":
    main()