__author__ = 'Davide'

import random
from collatz import collatz_len

def main():
    R = [random.randint(10 ** 0, 10 ** 10) for _ in range(1000000)]
    lenghts = [(x, collatz_len(x)) for x in R]
    lenghts.sort(key=lambda x: x[1])

    for (x, c) in lenghts[-10:]:
        print(c, x)

if __name__ == "__main__":
    main()