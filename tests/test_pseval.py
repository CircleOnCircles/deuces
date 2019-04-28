from slowroll.pokerstove import lookup_twohand
from slowroll import Card

def test_lookup_twohand():
    lookup_twohand([Card('Ac'), Card('As')])
