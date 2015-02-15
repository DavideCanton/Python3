__author__ = 'davide'

import numpy as np
import operator
from collections import defaultdict


class Board:
    GT = operator.gt
    LT = operator.lt

    def __init__(self, n):
        self.n = n
        self.num_constr = 0
        self.matrix = np.zeros((n, n), dtype=np.int)
        self.constraints = {}
        self.fixed = set()

    def set_constraint(self, start, end, sign):
        if sign not in [Board.GT, Board.LT]:
            raise ValueError("Sign invalid")

        def opposite(s):
            return Board.LT if s == Board.GT else Board.GT

        old = self.constraints.get((start, end))
        if old and old != sign:
            raise ValueError("Sign invalid")
        self.constraints[start, end] = sign
        self.constraints[end, start] = opposite(sign)
        self.num_constr += 2

    def __setitem__(self, key, value):
        if value < 0 or value > self.n:
            raise ValueError("{} is not a valid value".format(value))
        self.matrix[key] = value

    def set_fixed(self, key, value=True):
        if value:
            self.fixed.add(tuple(key))
        else:
            self.fixed.remove(tuple(key))

    def __getitem__(self, item):
        return self.matrix[item]

    def is_filled(self):
        return np.all(self.matrix != 0)

    def is_valid(self):
        return self._validate_constraints() and self._validate_numbers()

    def _validate_constraints(self):
        return self.valid_constraints() == self.num_constr

    def valid_constraints(self):
        val = 0
        for (pos, sign_func) in self.constraints.items():
            start, end = pos
            if sign_func(self.matrix[start], self.matrix[end]):
                val += 1
        return val

    def _validate_numbers(self):
        def check_all(arr):
            freq = np.bincount(arr)
            freq[0] = 0
            return np.all(freq <= 1)

        for i in range(self.n):
            if (not check_all(self.matrix[:, i]) or
                not check_all(self.matrix[i, :])):
                return False
        return True

    def print_board(self):
        def to_str(func):
            if func is None:
                return None
            return ">" if func == Board.GT else "<"

        tr = str.maketrans("<>", "^V")
        for i in range(self.n):
            for j in range(self.n):
                pos = (i, j)
                el = self.matrix[pos]
                print(el or " ", end=" ")
                pos2 = (i, j + 1)
                constr = self.constraints.get((pos, pos2))
                constr = to_str(constr)
                print(constr or " ", end=" ")
            print()
            if i < self.n - 1:
                for j in range(self.n):
                    pos = (i, j)
                    pos2 = (i + 1, j)
                    constr = self.constraints.get((pos, pos2))
                    constr = to_str(constr)
                    if constr is not None:
                        constr = constr.translate(tr)
                    print(constr or " ", end="   ")
            print()


if __name__ == "__main__":
    b = Board(3)
    b[0, 0] = 1
    b[0, 1] = 2
    b[0, 2] = 3
    b[1, 0] = 3
    b[1, 1] = 1
    b[1, 2] = 2
    b[2, 0] = 2
    b[2, 1] = 3
    b[2, 2] = 1
    b.set_constraint((0, 0), (0, 1), Board.LT)
    b.set_constraint((0, 0), (1, 0), Board.LT)
    b.set_constraint((1, 0), (2, 0), Board.GT)
    b.set_constraint((1, 1), (1, 2), Board.LT)
    b.set_constraint((1, 1), (2, 1), Board.LT)

    b.print_board()
    print(b.is_filled())
    print(b.is_valid())
