__author__ = 'Kami'

import itertools as it
import random
from collections import defaultdict
from multiprocessing.pool import Pool


class Table:
    def __init__(self):
        self.table = defaultdict(list)
        self.size = 0

    def add(self, card):
        if card[0] <= 7:
            self.table[card[0]].append(card)
        else:
            self.table[card[1]].append(card)
        self.size += 1

    def prune(self):
        for i in range(1, 5):
            a, b = self.table[i], self.table[8 - i]
            if i != 4:
                if a and b:
                    m = min(len(a), len(b))
                    self.table[i] = self.table[i][m:]
                    self.table[8 - i] = self.table[8 - i][m:]
                    self.size -= m * 2
            else:
                m = len(a)
                if m >= 2:
                    self.table[i] = self.table[i][m:]
                    self.size -= m

        for c in "bcds":
            if len(self.table[c]) == 3:
                self.table[c] = []
                self.size -= 3

    def __str__(self):
        l = []
        for i in range(1, 8):
            l.extend("{}{}".format(*t) for t in self.table[i])
        for i in "bcds":
            l.extend("{}{}".format(*t) for t in self.table[i])
        return "{}, Size: {}".format(l, self.size)


def execute(verbose=False):
    deck = list(it.product(range(1, 11), "bcds"))
    random.shuffle(deck)
    table = Table()

    while deck:
        card = deck.pop()
        if verbose:
            print("Pescata", card)
        table.add(card)
        table.prune()
        if verbose:
            print("Stato del tavolo:", table)
        if table.size >= 9:
            break

    return not deck


def pmain():
    num = [0, 0]  # 0 is false, 1 is true
    p = Pool(16)

    tasks = []
    for _ in range(100000):
        task = p.apply_async(func=execute)
        tasks.append(task)

    for task in tasks:
        res = task.get()
        num[int(res)] += 1

    print(num)
    print(num[1] / sum(num))


def main():
    execute(verbose=True)


if __name__ == "__main__":
    main()