from core import Strategy
from random import randrange

class RandomStrategy(Strategy):
    def __init__(self):
        self.author = "Matthew Scroggs"

    def play(self, board):
        column_for_play = randrange(7)
        return column_for_play
