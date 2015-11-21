__author__ = 'Davide'

import random


class Board:
    def __init__(self, heaps):
        self._heaps = heaps[:]

    @property
    def size(self):
        return len(self._heaps)

    @staticmethod
    def random_board(size, max_val=10):
        heaps = [random.randint(1, max_val) for _ in range(size)]
        return Board(heaps)

    def take_from(self, heap_index, cnt):
        self._heaps[heap_index] -= cnt

    def heap_cnt(self, heap_index):
        return self._heaps[heap_index]

    @property
    def heaps(self):
        return self._heaps[:]

    @property
    def end(self):
        return all(heap == 0 for heap in self.heaps)

    def show_board(self, bars=True):
        for heap_index, heap_cnt in enumerate(self.heaps):
            if bars:
                print("{}> {}".format(heap_index, "*" * heap_cnt))
            else:
                print("{}> {}".format(heap_index, heap_cnt))


if __name__ == "__main__":
    b = Board.random_board(3)
    b.show_board()
