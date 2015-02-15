__author__ = 'Davide'

import numpy as np
from numpy.lib.stride_tricks import as_strided


def main():
    a = np.array([1, 2, 3, 4, 5], dtype=np.int8)
    b = np.array([3], dtype=np.int8)
    c = as_strided(b, shape=(5,), strides=(0,))
    print(a + c)


if __name__ == "__main__":
    main()