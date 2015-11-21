__author__ = 'davide'

import numpy as np
import matplotlib.pyplot as plt


def f(x):
    x = 3 * x + 1
    while x & 1 == 0:
        x >>= 1
    return x


def f_n(x, n):
    for i in range(n):
        x = f(x)
    return x


def main():
    x = 21
    n = np.arange(1, 100)
    y = np.fromiter((f_n(x, an) for an in n), dtype=np.uint64)
    print(y)

    plt.plot(n, y)
    plt.show()


if __name__ == "__main__":
    main()