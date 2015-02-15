__author__ = 'davide'

from contextlib import redirect_stdout
import itertools as it
import numpy as np
import random


UP = np.array([-1, 0])
DOWN = np.array([1, 0])
LEFT = np.array([0, -1])
RIGHT = np.array([0, 1])
MOVES = [UP, DOWN, LEFT, RIGHT]
STR_TO_MOVE = dict(zip("udlr", MOVES))


class Board:
    def __init__(self):
        self.board = np.zeros((4, 4), dtype=int)

    def move(self, direction):
        def get_range(comp):
            if comp == 1:
                return range(3, -1, -1)
            return range(0, 4)

        moved = False
        merged = []

        for pos in it.product(*map(get_range, direction)):
            if self[pos] == 0:
                continue
            pos = np.array(pos)
            cur = pos.copy()
            next_ = pos + direction
            while self.valid_position(next_) and self[next_] == 0:
                cur = next_.copy()
                next_ += direction
            if self.valid_position(next_):
                already_merged = any(np.array_equal(a, next_) for a in merged)
                if self._can_merge(pos, next_) and not already_merged:
                    self[next_] *= 2
                    self[pos] = 0
                    moved = True
                    merged.append(next_)
                elif not np.array_equal(cur, pos):
                    self[cur] = self[pos]
                    self[pos] = 0
                    moved = True
            elif not np.array_equal(cur, pos):
                self[cur] = self[pos]
                self[pos] = 0
                moved = True

        return moved

    def highest_cell(self):
        return self.board.max()

    def no_more_moves(self):
        if np.any(self.board == 0):
            return False
        for pos in it.product(range(4), repeat=2):
            for pos2 in self.neighbors(pos):
                if self._can_merge(pos, pos2):
                    return False
        return True

    def valid_position(self, pos):
        return all(0 <= pos[i] <= 3 for i in (0, 1))

    def neighbors(self, pos):
        for direction in MOVES:
            next_ = pos + direction
            if self.valid_position(next_):
                yield next_

    def _can_merge(self, pos1, pos2):
        return self[pos1] == self[pos2]

    def add_random(self):
        if self.no_more_moves():
            raise Exception()
        while True:
            pos = np.random.random_integers(0, 3, 2)
            if self[pos] == 0:
                self[pos] = 2 if random.random() < 0.9 else 4
                return pos

    def __getitem__(self, item):
        return self.board[tuple(item)]

    def __setitem__(self, item, val):
        self.board[tuple(item)] = val

    def print_board(self):
        for i in range(4):
            print("|", end="")
            for j in range(4):
                s = self[i, j]
                print("{:>4}".format(s if s else ""), end="")
                print("|", end="")
            print()


def main():
    b = Board()
    b.add_random()
    b.add_random()
    b.print_board()

    def move_one(b, direction):
        val = b.move(direction)
        if val:
            b.add_random()
        b.print_board()
        print()
        return val

    while not b.no_more_moves():
        v1 = move_one(b, UP)
        v2 = move_one(b, LEFT)
        if not v1 and not v2:
            move_one(b, RIGHT)
            move_one(b, LEFT)

    return b.highest_cell() >= 2048


def main2():
    with open("log.txt", "w") as f:
        for _ in range(1000):
            with redirect_stdout(f):
                res = main()
            if res:
                print("OK")
                break
            else:
                print("RESET")


if __name__ == "__main__":
    main()