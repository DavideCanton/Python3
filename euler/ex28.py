__author__ = 'Davide'


def sum_d(x):
    s = 1
    n = 1
    for i in range(2, x, 2):
        s += 4 * n + 10 * i
        n += 4 * i
    return s


if __name__ == "__main__":
    print(sum_d(1001))
