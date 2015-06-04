from core import Strategy
from random import randrange

class VerticalSearcher(Strategy):
    """This strategy will find three-in-a-rows made vertically and either win
       or block them."""
    def __init__(self):
        self.author = "Matthew Scroggs"

    def play(self,board):
        for col_number,col in enumerate(board.all_cols()):
            # Remove leading zeros from column
            while col[0]==0:
                col = col[1:]
            # If there are three tokens in column and first three tokens are equal
            if len(col)>=3 and col[0]==col[1] and col[1]==col[2]:
                return col_number

        # If no three found, play randomly
        return randrange(board.col_num)
