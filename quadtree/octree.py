__author__ = 'davide'

from collections import namedtuple, deque
from random import randint
import sys
import itertools as it


class Cube(namedtuple("_Rect", "x, y, z, w, h, d")):
    def __contains__(self, point):
        """
        Checks if point is inside the rect.
        @type point: tuple
        @param point
        @return: bool
        """
        x, y, z = point
        if not self.x <= x <= self.x + self.w:
            return False
        if not self.y <= y <= self.y + self.h:
            return False
        if not self.z <= z <= self.z + self.d:
            return False
        return True

    def split(self):
        """
        Splits the rectangle.
        @return: List of splits.
        """
        w2, h2, d2 = self.w / 2, self.h / 2, self.d / 2
        return [Cube(self.x + w_r, self.y + h_r, self.z + d_r, w2, h2, d2)
                for (h_r, w_r, d_r) in it.product([0, h2], [0, w2], [0, d2])]

    def __str__(self):
        return str([self.x, self.y, self.z, self.w, self.h, self.d])


SONS = ["nw0", "ne0", "sw0", "se0", "nw1", "ne1", "sw1", "se1"]


class Node:
    __slots__ = tuple(SONS) + ("val", "bounds")

    def __init__(self, nw0=None, ne0=None, sw0=None, se0=None,
                 nw1=None, ne1=None, sw1=None, se1=None, val=None,
                 bounds=None):
        """
        Creates a node.
        @param val: the node content
        @param bounds: the node bound
        @type bounds: Cube
        """
        self.nw0, self.ne0, self.sw0, self.se0 = nw0, ne0, sw0, se0
        self.nw1, self.ne1, self.sw1, self.se1 = nw1, ne1, sw1, se1
        self.val = val
        self.bounds = bounds

    def __str__(self):
        return "<{}, {}>".format(self.val, self.bounds)

    @property
    def sons(self):
        """
        @return: tuple of sons (nw,ne,sw,se)
        """
        return tuple(getattr(self, name) for name in SONS)

    @property
    def leaf(self):
        """
        @return: True if not any(self.sons)
        """
        return not any(self.sons)

    def __iter__(self):
        yield self
        for n in filter(None, self.sons):
            yield from n


class OcTree:
    def __init__(self, data, width, height, depth):
        """
        Creates an OT.
        @param data: sequence of contents.
        @type data: iterable
        @param width: The width of the area covered by the OT.
        @type width: float
        @param height: The height of the area covered by the OT.
        @type height: float
        @param depth: The depth of the area covered by the OT.
        @type depth: float
        @return:
        """
        cube = Cube(0, 0, 0, width, height, depth)
        self.size = 0
        self.root = Node(val=data, bounds=cube)
        if data:
            self._split(self.root)

    def add_node(self, val):
        """
        Adds a node containing val to the OT.
        @param val: the value to be added.
        @return: None
        """
        node = self.search(val)
        node.val.append(val)
        self._split(node)
        self.size += 1

    def _split(self, root):
        """
        @type node: Node
        """
        node_list = deque([root])
        while node_list:
            node = node_list.popleft()
            if len(node.val) <= 1:
                continue
            if node.leaf:
                cubes = node.bounds.split()
                for son, bounds_cube in zip(SONS, cubes):
                    setattr(node, son, Node(val=[], bounds=bounds_cube))
            for val in node.val:
                for son in node.sons:
                    if val in son.bounds:
                        son.val.append(val)
                        break
            node.val.clear()
            node_list.extend(node.sons)

    def search(self, val):
        """
        Searches the value val in the QT.
        @param val: the value to be searched
        @return: the node containing the value, else None.
        """
        if val in self.root.bounds:
            node = self.root
            while not node.leaf:
                for son_s in SONS:
                    son = getattr(node, son_s)
                    if val in son.bounds:
                        node = son
                        break
            return node

    def __iter__(self):
        yield from self.root

    def assert_correct(self):
        for node in self:
            if node.val:
                assert (node.val[0] in node.bounds)


def main():
    data = [(randint(0, 128), randint(0, 128), randint(0, 128))
            for _ in range(10)]
    # data = [(30, 90, 100)]
    ot = OcTree([], 128.0, 128.0, 128.0)

    for i, d in enumerate(data, start=1):
        print("Aggiungo", d)
        ot.add_node(d)
        ot.assert_correct()
        for node in ot:
            print(node)
        assert i == ot.size


if __name__ == "__main__":
    main()