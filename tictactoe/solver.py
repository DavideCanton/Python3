__author__ = 'davide'

import random
import sys

SORT_KEY = {(0, 0): 1,
            (0, 1): 2,
            (0, 2): 1,
            (1, 0): 2,
            (1, 1): 0,
            (1, 2): 2,
            (2, 0): 1,
            (2, 1): 2,
            (2, 2): 1}

SIGN = {True: 1, False: -1}
OPPOSITE = dict(zip("XO", "OX"))


class HardCPUPlayer:
    def __init__(self, board, start_player):
        self.start_player = start_player
        self.board = board
        self.best = None

    def solve(self):
        self.negascout(-20, 20, self.start_player, 0)
        return self.best

    def negascout(self, alpha, beta, player, depth):
        winner = self.board.winner()
        if winner:
            return (SIGN[winner == self.start_player] *
                    (9 - depth) *
                    SIGN[depth % 2 == 0])
        if self.board.full():
            return 0

        b = beta
        moves = sorted(self.board.valid_moves(), key=lambda p: SORT_KEY[p])
        opposite = OPPOSITE[player]
        first_move = moves[0]
        for pos in moves:
            self.board.set_player(pos, player)
            score = -self.negascout(-b, -alpha,
                                    opposite, depth + 1)
            if alpha < score < beta and first_move != pos:
                score = -self.negascout(-beta, -alpha,
                                        opposite, depth + 1)
            self.board.clear_player(pos)
            if score > alpha:
                alpha = score
                if depth == 0:
                    self.best = pos
            if alpha >= beta:
                return alpha
            b = alpha + 1
        return alpha


class HumanPlayer:
    def __init__(self, board, start_player, input_stream=sys.stdin):
        self.board = board
        self.start_player = start_player
        self.input_stream = input_stream

    def solve(self):
        while True:
            move = self.input_stream.readline()
            pos = tuple(map(int, move.split()))
            if self.board.is_valid_move(pos):
                return pos


class EasyCPUPlayer:
    def __init__(self, board, start_player, win_prob=0.8, block_prob=0.5):
        self.board = board
        self.start_player = start_player
        self.win_prob = win_prob
        self.block_prob = block_prob

    def _move_good(self, board, move, player):
        board.set_player(move, player)
        res = board.winner() == player
        board.clear_player(move)
        return res

    def solve(self):
        moves = list(self.board.valid_moves())
        opposite_pl = OPPOSITE[self.start_player]
        if random.random() < self.win_prob:
            for move in moves:
                if self._move_good(self.board, move, self.start_player):
                    return move
        if random.random() < self.block_prob:
            for move in moves:
                if self._move_good(self.board, move, opposite_pl):
                    return move
        return random.choice(moves)
