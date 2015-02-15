from functools import total_ordering
from random import randint, choice
from pyIA.searching import *
from copy import deepcopy


DIM = 4
LAST = DIM ** 2 - 1


class Move:
    MOVES = (UP, DOWN, LEFT, RIGHT) = ("UP", "DOWN", "LEFT", "RIGHT")


@total_ordering
class Board:
    def __init__(self):
        self.board = []
        for i in range(DIM):
            l = []
            self.board.append(l)
            for j in range(DIM):
                l.append(i * DIM + j + 1)
        self.board[DIM - 1][DIM - 1] = 0
        self.zero = [DIM - 1, DIM - 1]

    def __lt__(self, other):
        return self.board < other.board

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        h = 0
        for n in self.board:
            for el in n:
                h = h * 17 + el
        return h

    def __repr__(self):
        return "Board: {}, Zero: {}".format(self.board, self.zero)

    def __str__(self):
        return "Board: {}, Zero: {}".format(self.board, self.zero)

    def build(self, values):
        self.board = []
        it = iter(values)
        for i in range(DIM):
            l = []
            self.board.append(l)
            for j in range(DIM):
                v = next(it)
                l.append(v)
                if v == 0:
                    self.zero = [i, j]

    @property
    def table(self):
        l = len("|".join("{:3d}".format(s) for s in self.board[0]))
        return ("\n" + "-" * l + "\n").join("|".join("{:3d}".format(s)
                                                     for s in b)
                                            for b in self.board)

    def shuffle(self, limit=10):
        i = 0
        while i < limit:
            try:
                self.move(choice(Move.MOVES))
            except ValueError:
                pass
            else:
                i += 1

    def can_move(self, move):
        if move == Move.LEFT and self.zero[1] > 0:
            return True
        if move == Move.RIGHT and self.zero[1] < DIM - 1:
            return True
        if move == Move.UP and self.zero[0] > 0:
            return True
        if move == Move.DOWN and self.zero[0] < DIM - 1:
            return True
        return False

    def move(self, move):
        if not self.can_move(move):
            raise ValueError("move not valid")
        if move == Move.LEFT:
            i, j = self.zero
            old = self.board[i][j - 1]
            self.board[i][j], self.board[i][j - 1] = old, 0
            self.zero[1] -= 1
        if move == Move.RIGHT:
            i, j = self.zero
            old = self.board[i][j + 1]
            self.board[i][j], self.board[i][j + 1] = old, 0
            self.zero[1] += 1
        if move == Move.UP:
            i, j = self.zero
            old = self.board[i - 1][j]
            self.board[i][j], self.board[i - 1][j] = old, 0
            self.zero[0] -= 1
        if move == Move.DOWN:
            i, j = self.zero
            old = self.board[i + 1][j]
            self.board[i][j], self.board[i + 1][j] = old, 0
            self.zero[0] += 1

    @property
    def solved(self):
        for n in range(LAST):
            i, j = divmod(n, DIM)
            if self.board[i][j] != n:
                return False
        return True

    def copy(self):
        return deepcopy(self)

    def __getitem__(self, index):
        return self.board[index[0]][index[1]]


class MoveGenerator:
    def __call__(self, t, p=None):
        _, board = t
        for m in Move.MOVES:
            if board.can_move(m):
                b = board.copy()
                b.move(m)
                yield (m, b), 1


def heuristic(tup):
    _, board = tup
    h = 0
    for i in range(DIM):
        for j in range(DIM):
            val = board[i, j]
            if val > 0:
                real_pos = divmod(val, DIM)
                h += abs(i - real_pos[0]) + abs(j - real_pos[1])
    return h


def reach_target_distance(board, distance, heuristic):
    while heuristic(board) < distance:
        try:
            board.move(choice(Move.MOVES))
        except ValueError:
            pass


if __name__ == '__main__':
    import time

    f = lambda b: (None, b)
    b = Board()
    reach_target_distance(b, randint(5, 10), lambda b: heuristic(f(b)))
    # b.build([7, 2, 4, 5, 0, 6, 8, 3, 1])
    print(b.table)
    print()
    print(heuristic(f(b)))

    goal = lambda t: t[1].solved
    sol = a_star((None, b), goal, heuristic, MoveGenerator(), callback=None)

    moves = []
    if sol[0]:
        for m, b in sol[0]:
            if m:
                x = str(m).upper()[0]
                print("Ho effettuato la mossa", x,
                      "distanza =", heuristic(f(b)))
                print(b.table)
                print()
                moves.append(x)
                time.sleep(1)
        moves = "".join(moves)
        print(moves)
        print(len(moves))
    else:
        print("Non esiste la soluzione")
