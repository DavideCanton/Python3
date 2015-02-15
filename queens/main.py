__author__ = 'Kami'

from cqueens_csp import min_conflicts as cmin_conflicts
from cqueens_csp import print_board
#from queens_csp import min_conflicts, print_board
import numpy as np
import random


def main():
    random.seed(1000)
    solution, iters = cmin_conflicts(100, -1, -1)
    if solution is not None:
        print("Trovata!")
        print_board(solution)
        print("Iterazioni:", iters)
    else:
        print("Timeout")


if __name__ == "__main__":
    main()