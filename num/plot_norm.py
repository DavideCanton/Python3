__author__ = 'Kami'

import matplotlib.pyplot as plt
import numpy as np
from numba import jit


@jit("f8(f8[:],f8)")
def p_norm(x, p):
    if p == 0:
        return np.abs(x).max()
    return (np.abs(x) ** p).sum() ** (1 / p)


if __name__ == "__main__":
    v = np.random.uniform(0, 10, 50)

    l = [(i, p_norm(v, i)) for i in range(1, 100)]
    oo_norm = p_norm(v, 0)
    x, y = zip(*l)
    plt.plot(x, y, "b-")
    plt.plot(x, [oo_norm] * len(x), "r-")
    plt.show()