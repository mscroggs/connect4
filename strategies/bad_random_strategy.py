from core import Strategy
from random import choice

class BadRandomStrategy(Strategy):
    """This strategy plays in an badly chosen random column."""
    def __init__(self):
        self.author = "Matthew Scroggs"

    def play(self, board):
        column_for_play = choice([0]*6+[1]*4+[2,3,4]+[5]*4+[6]*6)
        return column_for_play
