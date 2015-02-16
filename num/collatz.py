__author__ = 'davide'

import numpy as np
import matplotlib.pyplot as plt


def ensure_collatz(n):
    remainders = []
    while n > 1:
        remainders.append(n & 0x3)
        if n & 1:
            n = 3 * n + 1
        else:
            n >>= 1
    return remainders


def main():
    l = []

    for n in range(10000):
        r = ensure_collatz(n)
        l.append(len(r))

    lengths = np.array(l, dtype=np.uint32)
    plt.plot(lengths, "bx")
    plt.show()


if __name__ == "__main__":
    main()