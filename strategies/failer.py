from core import Strategy

class FailStrategy(Strategy):
    def __init__(self):
        self.author = "Matthew Scroggs"

    def play(self,board):
        while True:
            pass
