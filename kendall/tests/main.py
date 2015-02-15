__author__ = 'davide'

import numpy as np
from kendall import kendall_distance


def main():
    dtype = np.uint32

    a = np.arange(0, 20000, dtype=dtype)
    np.random.shuffle(a)
    b = np.array(a, dtype=dtype)
    np.random.shuffle(b)

    print(a)
    print(b)

    print(kendall_distance(a, b))


if __name__ == "__main__":
    main()