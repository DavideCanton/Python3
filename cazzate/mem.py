__author__ = 'davide'


class Node:
    def __init__(self, key, value, next_=None):
        self.key = key
        self.value = value
        self.next_ = next_


def main_n():
    start = None
    prev = None
    for i in range(10000000):
        n = Node(i, i)
        if not start:
            start = n
        if prev:
            prev.next_ = n
        prev = n

    input()


def main_t():
    values = {}
    next_ = {}
    nodes = set()
    prev = None

    for i in range(10000000):
        values[i] = i
        if prev is not None:
            next_[prev] = i
        prev = i
        nodes.add(i)

    input()

if __name__ == "__main__":
    main_t()