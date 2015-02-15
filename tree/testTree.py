import unittest
from random import *
from tree.tree import BinaryTree


class Test(unittest.TestCase):

    def setUp(self):
        rg = Random()
        self.N = 1000
        self.l = [rg.randint(0, self.N) for _ in range(self.N)]
        self.tree = BinaryTree.buildTree(*self.l)

    def testVisit(self):
        v = list(self.tree.depth_first())
        return all(i <= j for i, j in zip(v, v[1:]))

    def test_BF_VS_DF(self):
        bf = list(self.tree.breadth_first())
        df = list(self.tree.depth_first())
        bf.sort()
        df.sort()
        return bf == df

    def test_height(self):
        leaves = dict(self.tree.leaves())
        return max(leaves.values()) == self.tree.height

    def test_in_not(self):
        for el in range(self.N):
            if el in self.l and el not in self.tree:
                return False
            elif el not in self.l and el in self.tree:
                return False
        return True


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
