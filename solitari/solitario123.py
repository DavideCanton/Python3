import sys
import numpy as np


def simula(num):
    num = np.random.permutation(num)
    for i in [1, 2, 3]:
        mask = num[(i - 1)::3] == i
        if np.any(mask):
            return False
    return True


if __name__ == '__main__':
    max_t = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    usciti = 0
    num = np.tile(np.arange(1, 11), 4)

    for _ in range(max_t):
        if simula(num):
            usciti += 1

    print("Uscito", usciti, "volte su", max_t)
