from time import sleep

__author__ = 'davide'

import numpy as np
from random import random


class Board:
    def __init__(self, width, height):
        if width & 0x7:
            raise ValueError()
        self.width = width
        self.height = height
        self.board = np.zeros(height * (width >> 3), dtype=np.uint8)

    def _get_index(self, row, column):
        x = (column >> 3) + (self.width >> 3) * row
        y = column & 7
        return x, y

    def __setitem__(self, key, value):
        i, j = self._get_index(*key)
        if bool(value):
            self.board[i] |= 1 << j
        else:
            self.board[i] &= ~(1 << j)

    def __getitem__(self, key):
        i, j = self._get_index(*key)
        return (self.board[i] & (1 << j)) >> j

    def __str__(self):
        rows = []
        for row_index in range(self.height):
            row = []
            for col_index in range(self.width):
                cell = self[row_index, col_index]
                row.append(" " if not cell else "O")
            rows.append("".join(row))
        return "\n".join(rows)

    def like(self):
        return Board(self.width, self.height)


def randomBoard(w, h, p=.5):
    board = Board(w, h)
    for x in range(h):
        for y in range(w):
            board[x, y] = int(random() < p)
    return board


def advance(board):
    board2 = board.like()
    for row in range(board.height):
        for col in range(board.width):
            neighbors = _neigh(board, row, col)
            die = neighbors < 2 or neighbors > 3
            live = neighbors == 3
            if board[row, col] and die:
                board2[row, col] = 0
            elif not board[row, col] and live:
                board2[row, col] = 1
            else:
                board2[row, col] = board[row, col]
    return board2


def _neigh(board, r, c):
    def _fl(v, bound):
        if v < 0:
            v += bound
        elif v >= bound:
            v -= bound
        return v

    n = 0
    for i in range(r - 1, r + 2):
        for j in range(c - 1, c + 2):
            i = _fl(i, board.height)
            j = _fl(j, board.width)
            if (i != r or j != c) and board[i, j]:
                n += 1
    return n


if __name__ == "__main__":
    b = randomBoard(8, 8)
    for _ in range(100):
        print(b)
        b = advance(b)
        sleep(0.1)
        print("-" * 100)