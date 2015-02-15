__author__ = 'davide'

import numpy as np


class Board:
    VALUES = np.array([4, 9, 2, 3, 5, 7, 8, 1, 6],
                      dtype=np.int8).reshape((3, 3))

    def __init__(self):
        self.board = np.zeros((3, 3), dtype=np.int8)
        self.cache = None

    def set_player(self, pos, player):
        if not player or player == " ":
            self.clear_player(pos)
        else:
            sign = "X O".index(player) - 1
            self.board[pos] = Board.VALUES[pos] * sign
        self.cache = None

    def clear_player(self, pos):
        self.board[pos] = 0
        self.cache = None

    def get_player(self, pos):
        val = self.board[pos]
        if val > 0:
            return "O"
        elif val < 0:
            return "X"
        else:
            return None

    def valid_moves(self):
        for move in np.transpose(np.nonzero(self.board == 0)):
            yield tuple(move)

    def is_valid_move(self, move):
        return self.get_player(move) is None

    def winner(self):
        if self.cache is not None:
            return self.cache
        s_c = np.sum(self.board, axis=0)
        s_r = np.sum(self.board, axis=1)
        s_d = np.trace(self.board)
        s_rd = np.trace(np.fliplr(self.board))
        self.cache = ""
        for s in [s_c, s_r, s_d, s_rd]:
            if s.max() == 15:
                self.cache = "O"
                break
            elif s.min() == -15:
                self.cache = "X"
                break
        return self.cache

    def copy(self):
        board_copy = Board()
        board_copy.board = self.board.copy()
        return board_copy

    def full(self):
        return np.all(self.board != 0)

    def __str__(self):
        s = np.sign(self.board).reshape(9) + 1
        s = np.choose(s, list("X O"))
        return "{}|{}|{}\n{}|{}|{}\n{}|{}|{}".format(*s)


if __name__ == "__main__":
    b = Board()
    b.set_player((0, 0), "X")
    b.set_player((0, 1), "X")
    b.set_player((0, 2), "X")
    b.set_player((1, 1), "O")
    print(b)
    print(b.winner())
    print(list(b.valid_moves()))