from core import Strategy

class LowestColumnStrategy(Strategy):
    def play(self):
        pl = 0
        while self.game.board[0][pl]!=0:
            pl += 1
        return pl
