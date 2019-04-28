from typing import Union

from loguru import logger
from numba import jit


class Card:
    """
    Class represents a card of a poker deck. No joker included.

    Attributes:
        rank: A single uppercase string indicates the rank of this card.
        suit: A single lowercase string indicates the suit of this card.
    """

    # All possible ranks and suits
    RANKS = '23456789TJQKA'
    SUITS = 'shdc' # spades, hearts, diamonds, clubs
    INT_RANKS = range(13)
    PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]

    def __init__(self, card: str) -> None:
        """Init a card with card"""

        # Converts Card string to binary integer representation of card, inspired by:
        # http://www.suffecool.net/poker/evaluator.html (now, not accessible April 2019)
        # the basics

        # conversion from string => int
        CHAR_RANK_TO_INT_RANK = dict(zip(list(Card.RANKS), Card.INT_RANKS))
        CHAR_SUIT_TO_INT_SUIT = {
            's': 1,  # spades
            'h': 2,  # hearts
            'd': 4,  # diamonds
            'c': 8,  # clubs
        }

        self.rank = rank_char = card[0].upper()
        self.suit = suit_char = card[1].lower()
        self._rank = CHAR_RANK_TO_INT_RANK[rank_char]
        self._suit = CHAR_SUIT_TO_INT_SUIT[suit_char]
        self._rank_prime = Card.PRIMES[self._rank]

    def __int__(self):
        """
        An int representation that handles card calculation algorithms. We represent cards as 32-bit integers.
        Most of the bits are used, and have a specific meaning. See below:

                                        Card:

                              bitrank     suit rank   prime
                        +--------+--------+--------+--------+
                        |xxxbbbbb|bbbbbbbb|cdhsrrrr|xxpppppp|
                        +--------+--------+--------+--------+

            1) p = prime number of rank (deuce=2,trey=3,four=5,...,ace=41)
            2) r = rank of card (deuce=0,trey=1,four=2,five=3,...,ace=12)
            3) cdhs = suit of card (bit turned on based on suit of card)
            4) b = bit turned on depending on rank of card
            5) x = unused

        This representation will allow us to do very important things like:
        - Make a unique prime prodcut for each hand
        - Detect flushes
        - Detect straights

        and is also quite performance.
        """
        bitrank = 1 << self._rank << 16
        suit = self._suit << 12
        rank = self._rank << 8

        return bitrank | suit | rank | self._rank_prime

    def __radd__(self, other):
        return int(self) & int(other)

    def __ror__(self, other):
        return int(self) | int(other)

    def __rlshift__(self, other):
        return int(self) << int(other)

    def __rrshift__(self, other):
        return int(self) >> int(other)

    def __str__(self):
        return repr(self)

    @staticmethod
    def hand_to_binary(card_strs):
        """
        Expects a list of cards as strings and returns a list
        of integers of same length corresponding to those strings.
        """
        bhand = []
        for c in card_strs:
            bhand.append(Card.new(c))
        return bhand

    @staticmethod
    def prime_product_from_hand(card_ints):
        """
        Expects a list of cards in integer form.
        """

        product = 1
        for c in card_ints:
            product *= (c & 0xFF)

        return product

    @staticmethod
    @jit(nopython=True, cache=True)
    def prime_product_from_rankbits(rankbits):
        """
        Returns the prime product using the bitrank (b)
        bits of the hand. Each 1 in the sequence is converted
        to the correct prime and multiplied in.

        Params:
            rankbits = a single 32-bit (only 13-bits set) integer representing
                    the ranks of 5 _different_ ranked cards
                    (5 of 13 bits are set)

        Primarily used for evaulating flushes and straights,
        two occasions where we know the ranks are *ALL* different.

        Assumes that the input is in form (set bits):

                              rankbits
                        +--------+--------+
                        |xxxbbbbb|bbbbbbbb|
                        +--------+--------+

        """
        product = 1
        PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
        # for i in Card.INT_RANKS: numba not allow to refer to class constant
        for i in range(13):
            # if the ith bit is set
            if rankbits & (1 << i):
                product *= PRIMES[i]

        return product

    def int_to_binary(self):
        """
        For debugging purposes. Displays the binary number as a
        human readable string in groups of four digits.
        """
        bstr = bin(int(self))[2:][::-1]  # chop off the 0b and THEN reverse string
        output = list("".join(["0000" + "\t"] * 7) + "0000")

        for i in range(len(bstr)):
            output[i + int(i / 4)] = bstr[i]

        # output the string to console
        output.reverse()
        return "".join(output)

    @property
    def string(self):
        return f"{self.rank}{self.suit}"

    def __repr__(self):
        """
        Represent in a good form of [J♣], [A♣]
        """

        color = False
        try:
            from termcolor import colored
            # for mac, linux: http://pypi.python.org/pypi/termcolor
            # can use for windows: http://pypi.python.org/pypi/colorama
            color = True
        except ImportError:
            pass

        # for pretty printing
        PRETTY_SUITS = {
            1: chr(9824),  # spades
            2: chr(9829),  # hearts
            4: chr(9830),  # diamonds
            8: chr(9827)  # clubs
        }

        # # hearts and diamonds
        # PRETTY_REDS = [2, 4]
        #
        # # if we need to color red
        s = PRETTY_SUITS[self._suit]
        # if color and self._suit in PRETTY_REDS:
        #     s = colored(s, "red")

        return f"[{self.rank}{s}]"


    __slots__ = ['rank', 'suit', '_suit', '_rank', '_rank_prime']

    def __and__(self, other):
        return int(self) & int(other)

    def __hash__(self):
        return hash(self.string)

    def __eq__(self, other):
        return self.string == other.string

    def __lt__(self, other):
        if self.rank != other.rank:
            return self.rank < other.rank
        else:
            return self.suit < other.suit
