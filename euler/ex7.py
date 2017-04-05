__author__ = 'davide'

import itertools as it

from euler._utils import genera_primi


if __name__ == "__main__":
    n = it.islice(genera_primi(), 10000, 8359265)
    print(next(n))