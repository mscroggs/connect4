from core import Strategy
from random import randrange

class RandomStrategy(Strategy):
    """This strategy plays in an random column."""
    def __init__(self):
        self.author = "Matthew Scroggs"

    def play(self, board):
        return randrange(7)
