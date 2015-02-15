__author__ = 'Davide'

# cella: -2 dama nera, -1 pedina nera, 0 nulla, 1 pedina bianca, 2 dama bianca


class Board:
    def __init__(self):
        self.board = [[0] * min(j, 16 - j) for j in range(1, 16)]

        for j in range(1, 8, 2):
            # collocazione pedine bianche
            self[7, j] = 1
            self[6, j - 1] = 1
            self[5, j] = 1

            # collocazione pedine nere
            self[0, j - 1] = -1
            self[1, j] = -1
            self[2, j - 1] = -1

    def _convert(self, i, j):
        r = i + j
        c = j if r < 8 else 7 - i
        return r, c

    def __getitem__(self, item):
        i, j = self._convert(*item)
        return self.board[i][j]

    def __setitem__(self, key, value):
        i, j = self._convert(*key)
        self.board[i][j] = value

    def __str__(self):
        s = []
        for i in range(8):
            c = "|" + "|".join("Nn bB"[self[i, j] + 2] for j in range(8)) + "|"
            s.append(c)
        return "\n".join(s)


if __name__ == "__main__":
    board = Board()
    print(board)