import nim

__author__ = 'Davide'


def main():
    misere = True
    the_board = nim.board.Board.random_board(5)
    the_board.show_board()

    pl1 = nim.players.CPUPlayer(the_board, misere)
    pl2 = nim.players.CPUPlayer(the_board, misere)

    playerIndex = 1
    cur = pl1

    while not the_board.end:
        index, val = cur.turn()
        print("Il giocatore {} ha tolto {} elementi dall'heap {}".format(
            playerIndex, val, index))
        the_board.show_board()
        cur = pl2 if cur == pl1 else pl1
        playerIndex = 3 - playerIndex

    name = "1" if cur == pl1 else "2"
    if misere:
        print("Il giocatore {} ha vinto!".format(name))
    else:
        print("Il giocatore {} ha perso!".format(name))


if __name__ == "__main__":
    main()
