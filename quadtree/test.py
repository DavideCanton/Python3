__author__ = 'davide'

import unittest
import quadtree


class MyTestCase(unittest.TestCase):
    def testConstr(self):
        data = [(100, 100), (300, 300)]
        qt = quadtree.QuadTree(data, 500, 500)
        for node in qt:
            if node:
                self.assertTrue(len(node.val) <= 1)
                if len(node.val) > 0:
                    self.assertIn(node.val[0], node.bounds)


if __name__ == '__main__':
    unittest.main()
