from core import Strategy
import json
import random
import matplotlib.pylab as plt

class COFFIN(Strategy):
    """COnnect Four Fighting INstrument"""
    def __init__(self):
        self.author = "Matthew Scroggs"
        try:
            with open("data.json") as f:
                self.data = json.load(f)
        except:
            self.data = {}
        try:
            with open("plot.json") as f:
                self.plot = json.load(f)
        except:
            self.plot = [0]
        self.n = 0

    def make_board_string(self, board):
        b1 = "".join(["".join([str(i) for i in row]) for row in board.all_rows()])
        b2 = "".join(["".join([str(i) for i in row[::-1]]) for row in board.all_rows()])
        return max(b1,b2)

    def start(self):
        self.used = []

    def play(self, board):
        for piece in [self.turn,3-self.turn]:
            for c in range(7):
                fake = board.copy()
                for r in range(6):
                    if board[r,c] == 0 and (r == 5 or board[r+1,c]!=0):
                        fake[r,c] = self.turn
                if fake.winner() is not None:
                    return c
        b_string = self.make_board_string(board)
        if b_string not in self.data:
            self.data[b_string] = [1 if board[0,i]==0 else 0 for i in range(7)]
        r = random.uniform(0,sum(self.data[b_string]))
        for c in range(7):
            if r <= sum(self.data[b_string][:c+1]):
                self.used.append((b_string,c))
                return c

    def win(self):
        for b,c in self.used:
            self.data[b][c] *= 2
        self.plot.append(self.plot[-1]+3)
        self.save_state()

    def draw(self):
        for b,c in self.used:
            self.data[b][c] *= 1.3
        self.plot.append(self.plot[-1]+1)
        self.save_state()

    def lose(self):
        for b,c in self.used:
            self.data[b][c] /= 2
        self.plot.append(self.plot[-1]-1)
        self.save_state()

    def save_state(self):
        self.n += 1
        if self.n >= 100:
            self.n = 0
            with open("data.json","w") as f:
                json.dump(self.data,f)
            with open("plot.json","w") as f:
                json.dump(self.plot,f)
            plt.plot(self.plot)
            plt.xlabel("Games")
            plt.ylabel("3×wins + 1×draws - 1×losses")
            plt.savefig("learning.png")
            plt.clf()
