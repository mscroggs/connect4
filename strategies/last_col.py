from core import Strategy
from random import randrange

class LastCol(Strategy):
    """This strategy plays in the first available column."""
    def __init__(self):
        self.author = "Matthew Scroggs"

    def play(self, board):
        for i in range(7):
            if board[0,6-i]==0:
                return 6-i
