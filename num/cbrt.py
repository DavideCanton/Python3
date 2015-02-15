import random

__author__ = 'Davide'


def my_cbrt(x):
    y = x ** (1 / 3)
    y -= (x / (y * y) - y) / 3
    return y


def imbuto_cbrt(x):
    y = x ** (1 / 3)
    y -= (y - x / (y * y)) / 3
    return y


if __name__ == "__main__":
    x = random.random() * 100000000
    print(x)
    v1 = my_cbrt(x) ** 3
    v2 = imbuto_cbrt(x) ** 3
    v3 = (x ** (1 / 3)) ** 3

    print("My:", v1 - x)
    print("imbuto:", v2 - x)
    print("Std:", v3 - x)