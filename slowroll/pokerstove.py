import subprocess
from shutil import which
from typing import List
import os
import pathlib

from loguru import logger
from parse import parse, search, findall
import joblib
from .card import Card

library = pathlib.Path(__file__).absolute().parent
cache = joblib.Memory(str( library / "cache"))
logger.debug(f"Cache Path: {cache.location}")

def cmd_ps_eval(*args):
    """
    Raw Interface to pokerstove `ps-eval`

    ~/cmake/programs$ ./programs/ps-eval/ps-eval
    Allowed options:
      -? [ --help ]          produce help message
      -g [ --game ] arg (=h) game to use for evaluation
      -b [ --board ] arg     community cards for he/o/o8
      -h [ --hand ] arg      a hand for evaluation
      -q [ --quiet ]         produce no output

   For the --game option, one of the follwing games may be
   specified.
     h     hold'em
     o     omaha/8
     O     omaha high
     r     razz
     s     stud
     e     stud/8
     q     stud high/low no qualifier
     d     draw high
     l     lowball (A-5)
     k     Kansas City lowball (2-7)
     t     triple draw lowball (2-7)
     T     triple draw lowball (A-5)
     b     badugi
     3     three-card poker

   examples:
       ps-eval acas
       ps-eval AcAs Kh4d --board 5c8s9h
       ps-eval AcAs Kh4d --board 5c8s9h
       ps-eval --game l 7c5c4c3c2c
       ps-eval --game k 7c5c4c3c2c
       ps-eval --game kansas-city-lowball 7c5c4c3c2c

    Args:
        *args: any valid arguments to the ps-eval

    Returns:
        stdout: a string return
    """
    # check if ps-eval exist
    if which('ps-eval') is None:
        logger.error("""Make sure that `ps-eval` is availiable in your path.
        for macOS,
            `brew install circleoncircles/homebrew-tap/pokerstove`
        else compile yourself 
            visit https://github.com/andrewprock/pokerstove for more info
        """)
        raise FileNotFoundError("`ps-eval` is unavailable in your path")

    # change from tuple to list
    args = [e for e in args]

    ran_process = subprocess.run(['ps-eval'] + args, capture_output=True)

    return ran_process.stdout.decode()

@cache.cache
def evaluate(hands, board=None, game='h'):
    """
    A Pythonic Function for Pokerstove Evaluation `ps-eval`

    Currently support only hold'em.

    Args:
        hands: a list of hand string for evaluation e.g. ['acas', 'kh4d', '7c4c']
        board: Community cards like '5c8s9h'
        game: A game to use for evaluation. default to hold'em

    Returns:
        equities: A hand-corresponding list of percentage value of expected equity in of hand. If 1 hand is given,
            the 2nd hand return is any random hand against it.
        [(wins, ties, equity, equity2), ...]: A hand-corresponding list of tuple of 4 integers.
    """
    args = [
        '--game', game,
    ]

    if board:
        args.append('--board')
        args.append(board)

    for hand in hands:
        args.append('--hand')
        if type(hand) is Card:
            hand = hand.string
        args.append(hand)

    logger.debug(f'Args: {args}')

    output = cmd_ps_eval(*args)

    logger.debug("Here is the full output")
    logger.debug(output)

    import re
    halfs = [re.split('has', line)[1] for line in output.splitlines()]
    result = [re.findall('[\d\.]+', half) for half in halfs]

    logger.debug("Here is the full result")
    logger.debug(result)

    return result



