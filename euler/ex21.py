__author__ = 'Davide'


def divisors(n):
    for i in range(1, n // 2 + 1):
        if n % i == 0:
            yield i


def sum_divisors(n):
    return sum(divisors(n))


def amicable(a, b):
    if a > b:
        a, b = b, a
    return sum_divisors(a) == b and sum_divisors(b) == a


if __name__ == "__main__":
    s = 0
    for i in range(1, 10000):
        for j in range(i + 1, 10000):
            if amicable(i, j):
                s += i
    print(s)