from core import Strategy

class PlayInOrder(Strategy):
    """The strategy will play in the columns in order."""
    def __init__(self):
        self.author = "Matthew Scroggs"
        self.previous_move = 6

    def play(self,board):
        self.previous_move += 1
        self.previous_move %= board.col_num
        return self.previous_move
