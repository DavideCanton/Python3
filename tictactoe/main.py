__author__ = 'davide'

from solver import HardCPUPlayer, HumanPlayer, EasyCPUPlayer
from board import Board
import random
import time


def main():
    b = Board()
    print(b)
    print("-" * 5)

    s1 = HardCPUPlayer(b, "X")
    s2 = EasyCPUPlayer(b, "O")
    # s2 = HumanPlayer(b, "O")
    players = [s1, s2]
    g = random.choice([s1, s2])
    i = players.index(g)

    while not b.full() and not b.winner():
        # time.sleep(1)
        move = g.solve()
        b.set_player(move, g.start_player)
        print(b)
        print("-" * 5)
        i = 1 - i
        g = players[i]

    winner = b.winner()
    # assert winner != "O"
    if not winner:
        print("Pareggio")
    else:
        print("Ha vinto il giocatore {}".format(winner))


if __name__ == "__main__":
    main()