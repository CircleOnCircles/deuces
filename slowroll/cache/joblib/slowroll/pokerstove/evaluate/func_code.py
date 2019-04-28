# first line: 76
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
