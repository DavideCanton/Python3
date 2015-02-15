__author__ = 'Davide'


def sum_digits(n):
    c = 0
    while n:
        c += n % 10
        n //= 10
    return c


def fact(n):
    v = 1
    for i in range(1, n + 1):
        v *= i
    return v


if __name__ == "__main__":
    print(sum_digits(fact(100)))