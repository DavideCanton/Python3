import math
import multiprocessing
import multiprocessing.pool
import random

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

    rand = random.random

    for _ in range(k):
        a = int(2 + rand() * (n - 3))
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for __ in range(s - 1):
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

    floor = math.floor

    for i in range(3, floor(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False

    return True


def main():
    with multiprocessing.pool.Pool(2) as pool:
        r = []

        for i in range(200):
            n = 2 + int(random.random() * 3872985725535634)
            n |= 1
            print("Trying", n, end="-", flush=True)
            f1 = pool.apply_async(is_prime, (n,))
            print("1", end="-", flush=True)
            f2 = pool.apply_async(is_prime_mr, (n,))
            print("2")
            a, b = f1.get(), f2.get()
            if a != b:
                r.append((n, a, b))
        print(r)


if __name__ == "__main__":
    main()
