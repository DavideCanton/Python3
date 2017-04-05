__author__ = 'davide'

import sys

if __name__ == "__main__":
    print(sys.float_info)

    eps = 1
    while 1 + eps != 1:
        eps /= 2

    print(eps)
