from typing import List

from slowroll import Card


class Cards:
    """
    A collectiuon of 2 or more cards
    """
    _cards: List[Card] = []

    def __init__(self, cards: List[Card] = []):
        self._cards = cards

    def __add__(self, other):
        if type(other) is Card:
            self._cards.append(other)
        elif type(other) is Cards:
            self._cards.extend(other)

        return self

    def __getitem__(self, item):
        return self._cards[item]

    def __iter__(self):
        for c in self._cards:
            yield c

    def __len__(self):
        return len(self._cards)

    # def __next__(self):
    #     for c in self._cards:
    #         yield c

    def hasNoDuplicates(self):
        return len(set(self)) == len(self)

    @property
    def string(self):
        self._cards.sort()
        return ''.join([card.string for card in self])

    def sort(self):
        self._cards.sort()

    def __repr__(self):
        return repr(self._cards)