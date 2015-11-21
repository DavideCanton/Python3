__author__ = 'Kami'

import numpy as np
import matplotlib.pyplot as plt


def ema(s, alpha):
    m = np.zeros_like(s)
    m[0] = s[0]
    for t in range(1, len(s)):
        m[t] = alpha * s[t] + (1 - alpha) * m[t - 1]
    return m


if __name__ == "__main__":
    N = 100
    s = np.random.random_integers(0, 10, N)
    # s[np.random.random_integers(0, len(s) - 1, N // 10)] += 10

    plt.plot(s, label="orig")
    for a in [0.2, 0.5, 0.8]:
        plt.plot(ema(s, a), label=str(a))
    plt.legend()
    plt.show()