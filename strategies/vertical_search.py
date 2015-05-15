from core import Strategy
from random import randrange

class VerticalSearcher(Strategy):
    def __init__(self):
        self.author = "Matthew Scroggs"

    def play(self):
        pl = None
        for col_number in range(self.game.cols):
            col = self.game.col(col_number)
            streak = 0
            player = 0
            for i in col:
                if i!=0:
                    player = i
                if player != 0:
                    if player!=i:
                        break
                    streak +=1
            if streak == 3:
                pl = col_number
                break
            
        if pl is None:
            pl = randrange(self.game.cols)
            while self.game.board[0][pl]!=0:
                pl = randrange(self.game.cols)

        return pl
