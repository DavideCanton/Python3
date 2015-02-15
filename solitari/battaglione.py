import random
from collections import deque
import time


class Decks:
    def __init__(self, deck_size=40):
        deck = list(range(1, deck_size // 4 + 1)) * 4
        random.shuffle(deck)
        self.decks = [deque(deck[:deck_size // 2]),
                      deque(deck[deck_size // 2:])]

    def more_cards(self):
        return self.decks[0] and self.decks[1]

    def pop_two_cards(self):
        return [self.pop_one_card(i) for i in (0, 1)]

    def pop_one_card(self, index):
        return deque.popleft(self.decks[index])

    def deck_len(self, index):
        return len(self.decks[index])

    def extend_deck(self, index, card_list):
        self.decks[index].extend(card_list)

    def get_nonempty_deck(self):
        for i in (0, 1):
            if self.decks[i]:
                return self.decks[i]


if __name__ == '__main__':
    deck_size = 40
    decks = Decks(deck_size)
    on_table = []

    while decks.more_cards():
        print("*" * 100)

        print("G1 ha {} carte, G2 ha {} carte.".format(decks.deck_len(0),
                                                       decks.deck_len(1)))
        card_1, card_2 = decks.pop_two_cards()

        print("Uscite: d1 {}, d2 {}, residuo {}".format(card_1, card_2,
                                                        on_table))

        if card_1 > card_2:
            decks.extend_deck(0, on_table + [card_1, card_2])
            print("Vince g1")
            on_table = []
        elif card_1 < card_2:
            decks.extend_deck(1, on_table + [card_1, card_2])
            print("Vince g2")
            on_table = []
        else:
            print("Battaglione")
            on_table.append(card_1)
            on_table.append(card_2)
            if not decks.more_cards():
                break
            on_table.extend(decks.pop_two_cards())
            print("Coperte:", on_table[-2:])

    decks.get_nonempty_deck().extend(on_table)

    assert (decks.deck_len(0) == deck_size and decks.deck_len(1) == 0 or
            decks.deck_len(1) == deck_size and decks.deck_len(0) == 0)