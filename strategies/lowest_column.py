from core import Strategy

class LowestColumnStrategy(Strategy):
    """The strategy plays in the lowest numbered non-full column"""
    def __init__(self):
        self.author = "Matthew Scroggs"

    def play(self,board):
        play_here = 0
        while board[0][play_here] != 0:
            play_here += 1
        return play_here
