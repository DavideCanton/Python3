__author__ = 'Davide'

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


def main():
    s = 0
    for a in range(1, 10000):
        b = sum_divisors(a)
        if b > a:
            c = sum_divisors(b)
            if c == a:
                print(a, b, "amicabili")
                s += a + b
    print(s)


if __name__ == "__main__":
    main()