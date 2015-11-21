import functools
import operator
import random

__author__ = 'Davide'


class HumanPlayer:
    def __init__(self, board, input_provider):
        self.board = board
        self.input_provider = input_provider

    def turn(self):
        index = self.input_provider.get_heap_index(self.board.size)
        val = self.input_provider.get_val(index, self.board.heap_cnt(index))
        self.board.take_from(index, val)
        return index, val


class CPUPlayer:
    def __init__(self, board, misere=True):
        self.board = board
        self.misere = misere

    def turn(self):
        heaps = self.board.heaps

        nim_sum = functools.reduce(operator.xor, heaps)
        chosen_heap = -1
        for heap_index, heap_cnt in enumerate(heaps):
            if heap_cnt ^ nim_sum < heap_cnt:
                chosen_heap = heap_index
                break
        else:
            while True:
                chosen_heap = random.randint(0, self.board.size - 1)
                heap_cnt = self.board.heap_cnt(chosen_heap)
                if heap_cnt == 0:
                    continue
                amount_to_remove = random.randint(1, heap_cnt)
                self.board.take_from(chosen_heap, amount_to_remove)
                return chosen_heap, amount_to_remove

        amount_to_remove = heaps[chosen_heap] - (heaps[chosen_heap] ^ nim_sum)

        heaps_ge2 = False
        for heap_index, heap_cnt in enumerate(heaps):
            if heap_index == chosen_heap:
                n = heap_cnt - amount_to_remove
            else:
                n = heap_cnt
            if n > 1:
                heaps_ge2 = True
                break

        if not heaps_ge2:
            chosen_heap = heaps.index(max(heaps))
            heaps_one = sum(t == 1 for t in heaps)
            coeff = int(heaps_one % 2 != self.misere)
            amount_to_remove = heaps[chosen_heap] - coeff

        self.board.take_from(chosen_heap, amount_to_remove)
        return chosen_heap, amount_to_remove
