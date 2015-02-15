__author__ = 'davide'


def ex6(n):
    f1 = (n * (n + 1) / 2) ** 2
    f2 = sum(i ** 2 for i in range(n + 1))
    return f1 - f2


if __name__ == "__main__":
    print(ex6(100))