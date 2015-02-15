__author__ = 'davide'

import unittest
from genetic import fitness, attacks


class TestFunctionsGenetic(unittest.TestCase):
    def test_fitness(self):
        self.assertEqual(fitness([1, 2, 6, 3, 7, 4, 4, 1]), 24)
        self.assertEqual(fitness([2, 1, 6, 4, 1, 3, 0, 0]), 23)
        self.assertEqual(fitness([1, 3, 3, 0, 4, 0, 1, 3]), 20)
        self.assertEqual(fitness([2, 1, 4, 3, 2, 1, 0, 2]), 11)

    def test_attacks(self):
        self.assertTrue(attacks((0, 0), (1, 0)))
        self.assertTrue(attacks((0, 0), (0, 1)))
        self.assertTrue(attacks((0, 0), (1, 1)))
        self.assertTrue(attacks((0, 1), (1, 0)))

if __name__ == '__main__':
    unittest.main()
