from typing import Optional, Union, List, Iterable, Tuple

from loguru import logger

from slowroll import Deck, Card
from slowroll.cards import Cards


class Hand(Cards):

    def __init__(self, two_cards: Union[str, List[str], List[Card]], deck: Optional[Deck] = None):
        """Init a hand of 2 cards by cards"""
        self.deck = deck # save as a reference

        if type(two_cards) is str:
            # check len
            assert len(two_cards) == 4
            a, b = two_cards[:2], two_cards[2:]
            self._cards = [Card(a), Card(b)]
        elif hasattr(two_cards, '__len__'):
            assert len(two_cards) == 2
            if type(two_cards[0]) is str:
                self._cards = [Card(s) for s in two_cards]
            elif type(two_cards[0]) is Card:
                two_cards: Iterable[Card]
                self._cards = [c for c in two_cards] # is it better to not copy?
            else:
                raise NotImplementedError
        else:
            raise NotImplementedError

        self.sort()


    @classmethod
    def draw_from_deck(cls, deck: Deck):
        cards = deck.draw(2)
        return cls(cards, deck=deck)

    def evaluate(self):
        """
        Evaluate an odd of this hand against any other random hands. It considers only the card of this hand.

        This method use pokerstove as a source of data. This method reduces the search space.

        Returns:
             odd: A win probability of this hand range from 0 to 1 as a float.
        """
        # reducing search space, cards has been sorted since init.
        evaluating_card = Cards([])
        if self.is_same_suit():
            generic_suit = 'h'
            evaluating_card._cards = [Card(f'{c.rank}{generic_suit}') for c in self]
        else: #a pair or not the same suit and not the same rank
            generic_suits = ['h', 'd']
            evaluating_card._cards = [Card(f'{c.rank}{suit}') for c, suit in zip(self, generic_suits)]

        from .pokerstove import evaluate

        logger.debug(f"simplfied hand {evaluating_card.string}")
        return evaluate([evaluating_card.string])



    def is_same_suit(self):
        return self._cards[0]._suit == self._cards[1]._suit

    def is_pair(self):
        return self._cards[0]._rank == self._cards[1]._rank
