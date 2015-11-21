import random
import sys
import itertools as it
from reverse.searching import *
from reverse.utils import compare_on
from collections import defaultdict

__author__ = 'Davide'


@compare_on("board")
class Board:
    def __init__(self, r, c):
        self.r = r
        self.c = c
        self.board = 0

    def __hash__(self):
        return self.board

    @staticmethod
    def random(r, c):
        b = Board(r, c)
        for _ in range(r * c):
            i = random.randint(0, r - 1)
            j = random.randint(0, c - 1)
            b.flip(i, j)
        return b

    @property
    def end(self):
        return self.board == 0

    def get_val(self, r, c):
        mask = 1 << self._linearize_index(r, c)
        return (self.board & mask) != 0

    def set_val(self, r, c, val):
        mask = 1 << self._linearize_index(r, c)
        if val:
            self.board |= mask
        else:
            self.board &= ~mask

    def _linearize_index(self, r, c):
        return self.c * r + c

    def flip_val(self, r, c):
        old_val = self.get_val(r, c)
        self.set_val(r, c, not old_val)

    def flip(self, r, c):
        max_v = (1 << (self.r * self.c)) - 1
        mask = 0
        lower = max(0, r - 1)
        upper = min(r + 2, self.r)
        for i in range(lower, upper):
            ind = self._linearize_index(i, c)
            mask += ((1 << ind) +
                     (1 << (ind + 1) if c < self.c - 1 else 0) +
                     (1 << (ind - 1) if c > 0 else 0))
        val = (~(self.board & mask)) & mask
        self.board = ((self.board & ~mask) | val) & max_v

    def ones(self):
        n = 0
        m = self.board
        while m:
            if m & 1:
                n += 1
            m >>= 1
        return n

    def ones_surr(self, r, c):
        n = 0
        for i in range(r - 1, r + 2):
            for j in range(c - 1, c + 2):
                if self._valid_index(i, j) and self.get_val(i, j):
                    n += 1
        return n

    def zeros_surr(self, r, c):
        n = 0
        for i in range(r - 1, r + 2):
            for j in range(c - 1, c + 2):
                if self._valid_index(i, j) and not self.get_val(i, j):
                    n += 1
        return n

    def _valid_index(self, i, j):
        return 0 <= i < self.r and 0 <= j < self.c

    def __str__(self):
        s = "\n".join("|".join(" *"[self.get_val(i, j)] for j in range(self.c))
                      for i in range(self.r))
        return s

    def __repr__(self):
        n = self.ones()
        return "Board with {} filled: {}".format(n, self.board)

    @staticmethod
    def from_number(r, c, num):
        b = Board(r, c)
        b.board = num
        return b

    def copy(self):
        return Board.from_number(self.r, self.c, self.board)


def heuristic(t):
    board = t[1]
    n = 0
    for i in range(board.r):
        for j in range(board.c):
            tl = [i - 1, j - 1]
            br = [i + 1, j + 1]

            tl[0] = max(tl[0], 0)
            tl[1] = max(tl[1], 0)
            br[0] = min(br[0], board.r - 1)
            br[1] = min(br[1], board.c - 1)
            r = br[0] - tl[0] + 1
            c = br[1] - tl[1] + 1

            n += board.ones_surr(i, j) / (r * c)
    return n * 3


class MoveGen:
    def __init__(self):
        self.cache = defaultdict(int)

    def __call__(self, t, p=None, d=0):
        _, board = t
        if p:
            m, _ = p
        else:
            m = None
        nums = list(it.product(range(board.r), range(board.c)))
        random.shuffle(nums)
        if m is not None:
            nums.remove(m)

        self.cache[d] += 1

        for (r, c) in nums[:3]:
            b = board.copy()
            b.flip(r, c)
            yield (r, c), b


def add_weight(f, v):
    def wrapped(*a, **kw):
        for val in f(*a, **kw):
            yield val, v

    return wrapped


def wr():
    with open("heur.txt", "w") as f:
        for x in range(3, 5):
            r = x
            c = x
            print(r, "x", c, file=f)

            for i in range(1 << (r * c)):
                b = Board(r, c)
                b.board = i

                def goal(t):
                    return t[1].end

                start = None, b

                gen = MoveGen()
                sol = a_star(start, goal, heuristic, add_weight(gen, 1))

                if sol:
                    print(b.board, len(sol[0]), file=f, flush=True)
                else:
                    print(b.board, None, file=f, flush=True)


def main():
    # r, c = map(int, sys.argv[1:])
    r, c = 5, 5
    print(r, "x", c)

    # b = Board.random(r, c)
    b = Board(r, c)
    b.set_val(2, 0, True)
    print(b.board)
    print(b)

    def goal(t):
        return t[1].end

    start = None, b

    gen = MoveGen()
    sol = a_star(start, goal, heuristic, add_weight(gen, 1))
    # for k, v in gen.cache.items():
    #    print(k, v)

    if sol:
        for v in sol[0]:
            print(v, heuristic(v))
            # print(v[1])
        print("Length of solution:", len(sol[0]))
    else:
        print(b.board, None)


if __name__ == "__main__":
    main()
