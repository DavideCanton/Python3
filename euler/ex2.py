"""
Calcolare la somma dei numeri pari di Fibonacci inferiori a 4E6.
"""

__author__ = 'davide'


def ex2_1(n=4E6):
    n1, n2 = 1, 1
    s = 0
    while n2 <= n:
        if n2 % 2 == 0:
            s += n2
        n1, n2 = n2, n1 + n2
    return s


def ex2_2(n=4E6):
    n1, n2, n3 = 1, 1, 2
    s = 0
    while n3 <= n:
        s += n3
        n1 = n2 + n3
        n2 = n3 + n1
        n3 = n1 + n2
    return s


def ex2_3(n=4E6):
    n1, n2 = 0, 2
    s = 0
    while n2 <= n:
        s += n2
        n1, n2 = n2, 4 * n2 + n1
    return s


if __name__ == "__main__":
    print(ex2_3(35))
