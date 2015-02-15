import numpy as np
from collections import Iterable


class Node:
    def __init__(self, player=None, val=None, children=None):
        self.player = player
        self.val = val
        self.children = children or []

    def __str__(self):
        return ("Node: p={} v={} c={}"
                .format(self.player, self.val, self.children))

    def getPlayer(self, player):
        return [c for c in self.children if c.player == player]


class TreeV:
    def __init__(self, n):
        self.tree = Node()

    @staticmethod
    def _add_node(tree, player, val):
        nodeL = tree.getPlayer(player)
        if not nodeL:
            node = Node(player, val)
            tree.children.append(node)
        else:
            node = nodeL[0]
        return node

    def __setitem__(self, coalition, value):
        if not isinstance(coalition, Iterable):
            coalition = [coalition]
        tree = self.tree
        for el in sorted(coalition):
            tree = self._add_node(tree, el, value)
        return self

    def __getitem__(self, coalition):
        if not isinstance(coalition, Iterable):
            coalition = [coalition]
        if len(coalition) == 0:
            return 0.
        tree = self.tree
        for player in sorted(coalition):
            nodeL = tree.getPlayer(player)
            if len(nodeL) == 0:
                raise KeyError("{} not found".format(coalition))
            tree = nodeL[0]
        return tree.val

    def __contains__(self, coalition):
        if not isinstance(coalition, Iterable):
            coalition = [coalition]
        if len(coalition) == 0:
            return True
        tree = self.tree
        for player in sorted(coalition):
            nodeL = tree.getPlayer(player)
            if len(nodeL) == 0:
                return False
            tree = nodeL[0]
        return True


class ArrayV:
    def __init__(self, n):
        self.array = np.tile(None, 2 ** n)

    @staticmethod
    def _get_index(coalition):
        return sum(2 ** p for p in coalition)

    def __setitem__(self, coalition, value):
        if not isinstance(coalition, Iterable):
            coalition = [coalition]
        p = ArrayV._get_index(coalition)
        self.array[p] = value

    def __getitem__(self, coalition):
        if not isinstance(coalition, Iterable):
            coalition = [coalition]
        if len(coalition) == 0:
            return 0.
        p = self._get_index(coalition)
        v = self.array[p]
        if v is None:
            raise KeyError("{} not found".format(coalition))
        else:
            return v

    def __contains__(self, coalition):
        if not isinstance(coalition, Iterable):
            coalition = [coalition]
        if len(coalition) == 0:
            return True
        p = self._get_index(coalition)
        return self.array[p] is not None


if __name__ == '__main__':
    v = ArrayV(2)
    v[0] = 3.
    v[1] = 4.
    v[0, 1] = 5.
    print(v[{}])
    print(v[0])
    print(v[1])
    print(v[0, 1])
