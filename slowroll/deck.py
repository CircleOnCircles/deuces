from random import shuffle as rshuffle
from loguru import logger

from slowroll.cards import Cards
from .card import Card


class Deck(Cards):
    """
    Class representing a deck. The first time we create, we seed the static 
    deck with the list of unique card integers. Each object instantiated simply
    makes a copy of this object and shuffles it. 
    """
    _FULL_DECK = []

    def __init__(self):
        self.shuffle()
        self.drawn_cards = []

    def shuffle(self):
        # and then shuffle
        self._cards = Deck.GetFullDeck()
        rshuffle(self._cards)

    def draw(self, n=1):
        cards = []
        for i in range(n):
            cards.append(self._cards.pop(0))

        logger.info(f'{n} card(s) are drawn. This deck has {len(self.cards)} card(s) remains.')
        self.drawn_cards.extend(cards)
        return cards

    def __repr__(self):
        return repr(self._cards)

    @staticmethod
    def GetFullDeck():
        if Deck._FULL_DECK:
            return list(Deck._FULL_DECK)

        # create the standard 52 card deck
        for rank in Card.RANKS:
            for suit in Card.SUITS:
                Deck._FULL_DECK.append(Card(rank + suit))

        return Deck._FULL_DECK.copy()

    __slots__ = ['_cards', 'drawn_cards']
