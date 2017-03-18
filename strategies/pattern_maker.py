from core import Strategy
from random import randrange,shuffle

class FollowAPattern(Strategy):
    """This strategy plays in the first available column."""
    def __init__(self):
        self.author = "Matthew Scroggs"
        self.order = range(7)
        shuffle(self.order)
        self.i=-1

    def play(self, board):
        self.i+=1
        self.i %= 7
        return self.order[self.i]
