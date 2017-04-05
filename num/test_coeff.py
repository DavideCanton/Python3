import math

import matplotlib.pyplot as plt
import numpy as np


def f(n):
    def g(k):
        return math.factorial(n) / math.factorial(k) / math.factorial(n - k)

    return g


if __name__ == "__main__":
    n = 10
    x = np.arange(n + 1)
    y = np.frompyfunc(f(n), 1, 1)(x)
    y = np.cumsum(y)
    z = (n ** x) / np.fromiter(map(math.factorial, x), dtype=np.uint32)
    z = np.cumsum(z)
    print(x)
    print(y)
    print(z)

    plt.plot(x, y)
    plt.plot(x, z)
    plt.show()
