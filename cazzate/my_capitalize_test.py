__author__ = 'Davide'

import unittest
from cazzate.rename_bb import capitalize_words


class MyTestCase(unittest.TestCase):
    def test_capitalize_words1(self):
        input_phrase = "crazy handful stuff of nothing"
        out_phrase = capitalize_words(input_phrase)

        self.assertEqual("Crazy Handful Stuff Of Nothing", out_phrase)

    def test_capitalize_words2(self):
        input_phrase = "let's go to the mall"
        out_phrase = capitalize_words(input_phrase)

        self.assertEqual("Let's Go To The Mall", out_phrase)

    def test_capitalize_words3(self):
        input_phrase = "a no-go-round trip"
        out_phrase = capitalize_words(input_phrase)

        self.assertEqual("A No-Go-Round Trip", out_phrase)


if __name__ == '__main__':
    unittest.main()
