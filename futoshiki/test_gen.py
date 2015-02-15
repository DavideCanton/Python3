__author__ = 'Kami'

from genetic import find_solution, array_to_board
from board import Board
from random import shuffle


def get_instance_5():
    global N
    N = 5

    b = Board(5)
    b[1, 0] = 3
    b.set_fixed((1, 0))
    b[2, 0] = 4
    b.set_fixed((2, 0))
    b[3, 3] = 1
    b.set_fixed((3, 3))
    b[4, 3] = 2
    b.set_fixed((4, 3))
    b[4, 4] = 4
    b.set_fixed((4, 4))
    b.set_constraint((1, 0), (0, 0), Board.GT)
    b.set_constraint((1, 1), (0, 1), Board.GT)
    b.set_constraint((1, 1), (2, 1), Board.GT)
    b.set_constraint((3, 0), (3, 1), Board.GT)
    b.set_constraint((3, 2), (2, 2), Board.GT)
    b.set_constraint((3, 4), (2, 4), Board.GT)
    b.set_constraint((4, 1), (4, 2), Board.LT)
    return b


def get_instance_4():
    # sol: 3 1 2 4 1 4 3 2 4 2 1 3 2 3 4 1
    global N
    N = 4

    b = Board(4)
    b[0, 0] = 3
    b.set_fixed((0, 0))
    b[3, 1] = 3
    b.set_fixed((3, 1))
    b[3, 3] = 1
    b.set_fixed((3, 3))
    b.set_constraint((0, 1), (0, 2), Board.LT)
    b.set_constraint((0, 2), (0, 3), Board.LT)
    b.set_constraint((1, 1), (2, 1), Board.GT)
    return b


def get_instance_3():
    # sol: 1 2 3 3 1 2 2 3 1
    global N
    N = 3

    b = Board(3)
    b[0, 0] = 1
    b.set_fixed((0, 0))
    b[2, 0] = 2
    b.set_fixed((2, 0))
    b.set_constraint((0, 0), (0, 1), Board.LT)
    b.set_constraint((0, 0), (1, 0), Board.LT)
    b.set_constraint((1, 1), (2, 1), Board.LT)
    return b


def random_pos(board):
    b = []
    for i in range(N):
        row = set(board[i, :]) - {0}
        nums = list(set(range(1, N + 1)) - row)
        shuffle(nums)
        row = list(board[i, :])
        j = 0
        for k in range(N):
            if row[k] == 0:
                row[k] = nums[j]
                j += 1
        b.extend(row)
    return tuple(b)


def random_pos2(board):
    b = list(board.matrix.flatten())
    for p in range(N * N):
        if divmod(p, N) not in board.fixed:
            b[p] = randint(1, N)
    return tuple(b)


if __name__ == "__main__":
    b = get_instance_4()
    population = [random_pos(b) for _ in range(1000)]
    solution, iters = find_solution(population, b, 4)
    print("Trovata!" if iters >= 0 else "Terminato timeout")
    sol = array_to_board(solution, b)
    sol.print_board()
    print(iters)