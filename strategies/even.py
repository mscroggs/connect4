from core import Strategy
from random import randrange

class I_LOVE_EVEN_NUMBERS(Strategy):
    """This strategy plays in the first available column."""
    def __init__(self):
        self.author = "Matthew Scroggs"

    def play(self, board):
        for i in [2,4,6,0,1,3,5]:
            if board[0,i]==0:
                return i
