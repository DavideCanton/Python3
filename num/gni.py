__author__ = 'davide'

import numpy as np

if __name__ == "__main__":
    a = np.array([0, 2, 5, 3, 1, 4, 6, 7])
    print(np.sort(a))
    for i in range(5):
        q = np.percentile(a, 25 * i, interpolation='lower')
        print(i, "quartile=", q, a[a <= q])