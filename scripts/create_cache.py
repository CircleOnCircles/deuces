from itertools import combinations

from loguru import logger

from slowroll import Deck
from slowroll import Hand


def create_cache():
    deck = Deck()
    _52cards = deck._FULL_DECK.copy()

    # all possible hand
    for hand in combinations(_52cards, 2):
        hand = Hand(list(hand))
        logger.info(f'creating cache for hand: {hand.string}')
        print(hand.evaluate())

if __name__ == '__main__':
    create_cache()