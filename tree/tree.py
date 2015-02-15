from sys import stdout
from collections import deque

class TreeNode:
    def __init__(self, val=None, left=None, right=None, depth=0):
        self.val = val
        self.left = left
        self.right = right
        self.depth = depth

    @property
    def is_leaf(self):
        return not (self.left or self.right)

    def __repr__(self):
        return "TreeNode: {}".format(self.val)


class BinaryTree:
    def __init__(self):
        self._root = None
        self._size = 0
        self._height = 0

    def children(self, val):
        node = self._search(self._root, val)
        for child in (node.left, node.right):
            if child:
                yield child.val

    def __contains__(self, val):
        node = self._search(self._root, val)
        return node is not None

    def search(self, val, default=None):
        node = self._search(self._root, val)
        return node.val if node else default

    def _search(self, node, val):
        if node.val == val:
            return node
        elif node.val > val and node.left:
            return self._search(node.left, val)
        elif node.right:
            return self._search(node.right, val)
        else:
            return None

    def searchKey(self, val, default=None, key=None, use=False):
        if key is None:
            key = lambda x: x
        if use:
            val = key(val)
        node = self._searchKey(self._root, val, key)
        return node.val if node else default

    def _searchKey(self, node, val, key):
        v = key(node.val)
        if v == val:
            return node
        elif v > val and node.left:
            return self._searchKey(node.left, val, key)
        elif node.right:
            return self._searchKey(node.right, val, key)
        else:
            return None

    def add(self, val):
        self._root = self._add(self._root, val, 0)
        self._size += 1

    @property
    def size(self):
        return self._size

    def _add(self, node, val, depth):
        if not node:
            node = TreeNode(val, depth=depth)
            self._height = max(self._height, depth)
        elif node.val > val:
            node.left = self._add(node.left, val, depth + 1)
        elif node.val < val:
            node.right = self._add(node.right, val, depth + 1)
        return node

    @classmethod
    def buildTree(cls, *iterable):
        new_tree = BinaryTree()
        for element in iterable:
            new_tree.add(element)
        return new_tree

    def printTree(self, out=stdout):
        self._printTree(self._root, out, 0)

    def _printTree(self, node, out, indent):
        if node.right:
            self._printTree(node.right, out, indent + 4)
        print(" " * indent + "({})".format(node.val), file=out)
        if node.left:
            self._printTree(node.left, out, indent + 4)

    @property
    def root(self):
        if self._size == 0:
            raise TreeError("Empty tree")
        return self._root.val

    @property
    def height(self):
        return self._height

    def leaves(self):
        """Yields leaf and depth"""
        if not self._root:
            raise TreeError("Empty tree")
        yield from self._leaves(self._root)

    def _leaves(self, node):
        if node.is_leaf:
            yield (node.val, node.depth)
        if node.left:
            yield from self._leaves(node.left)
        if node.right:
            yield from self._leaves(node.right)

    @property
    def min(self):
        if self._size == 0:
            raise TreeError("Empty tree")
        node = self._root
        while node.left:
            node = node.left
        return node.val

    @property
    def max(self):
        if self._size == 0:
            raise TreeError("Empty tree")
        node = self._root
        while node.right:
            node = node.right
        return node.val

    def breadth_first(self):
        queue = deque([self._root])
        while queue:
            node = queue.popleft()
            yield node.val
            for child in (node.left, node.right):
                if child:
                    queue.append(child)

    def depth_first(self):
        queue = deque([self._root])
        while queue:
            node = queue.pop()
            yield node.val
            for child in (node.right, node.left):
                if child:
                    queue.append(child)
