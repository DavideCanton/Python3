__author__ = 'davide'

import unittest
from g2048 import Board


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_add_random(self):
        self.assertTrue(self.board.highest_cell() == 0)
        self.board.add_random(2)
        self.assertTrue(self.board.highest_cell() == 2)


if __name__ == '__main__':
    unittest.main()
