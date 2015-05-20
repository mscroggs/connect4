from core import Strategy

class PlayInOrder(Strategy):
    def __init__(self):
        self.author = "Matthew Scroggs"
        self.next = 0

    def play(self,board):
        next = self.next
        self.next += 1
        self.next %= board.col_num
        return next
