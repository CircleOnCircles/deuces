from slowroll import Card, Deck, Evaluator

def test_create_cards():
    # create a card
    card = Card('Qh')

    # create a board and hole cards
    board = [
        Card('2h'),
        Card('2s'),
        Card('Jc')
    ]
    hand = [
        Card('Qs'),
        Card('Th')
    ]

    # pretty print cards to console
    # Card.print_pretty_cards(board + hand)

    

def test_evaluator():
    # create an evaluator
    evaluator = Evaluator()

    # or for random cards or games, create a deck
    print("Dealing a new hand...")
    deck = Deck()
    board = deck.draw(5)
    player1_hand = deck.draw(2)
    player2_hand = deck.draw(2)

    print("The board:" , board)
    # Card.print_pretty_cards(board)

    print("Player 1's cards:", player1_hand)

    print("Player 2's cards:", player2_hand)

    # and rank your hand
    rank = evaluator.evaluate(board, player1_hand)
    print(rank)

    p1_score = evaluator.evaluate(board, player1_hand)
    p2_score = evaluator.evaluate(board, player2_hand)

    # bin the scores into classes
    p1_class = evaluator.get_rank_class(p1_score)
    p2_class = evaluator.get_rank_class(p2_score)

    # or get a human-friendly string to describe the score
    print(f"Player 1 hand rank = {p1_score} {evaluator.class_to_string(p1_class)}")
    print(f"Player 2 hand rank = {p2_score} {evaluator.class_to_string(p2_class)}")

    # or just a summary of the entire hand
    hands = [player1_hand, player2_hand]
    evaluator.hand_summary(board, hands)
