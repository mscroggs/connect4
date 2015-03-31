from core import Strategy
from random import randrange

class RandomStrategy(Strategy):
    def play(self):
        pl = randrange(self.game.cols)
        while self.game.board[0][pl]!=0:
            pl = randrange(self.game.cols)
        return pl
