from core.errors import MoveError,ResultError,Alarm
from core.board_module import Board
import signal

def alarm_handler(signum,frame):
    raise Alarm

class Game:
    def __init__(self,s1,s2,rows=6,cols=7):
        self.row_num = rows
        self.col_num = cols
        self.s1 = s1
        self.s2 = s2
        self.s1.turn = 1
        self.s2.turn = 2
        self.turn = 1
        self.reset()

    def reset(self):
        """Resets the game."""
        self.r_winner = 0
        self.board = Board(self.row_num,self.col_num)
        self.turn = 1
        self.s1.start()
        self.s2.start()

    def __str__(self):
        return self.board.__str__()

    def put_in(self,player,column):
        """Game.put_in(player,column) puts player's piece in column."""
        col = self.board.col(column)
        row = None
        for i,val in enumerate(col):
            if val == 0:
                row = i
            else:
                break
        if row is None:
            raise MoveError("The column you tried to play in is full")
        
        self.board[row][column] = player

    def repeated_play(self,games,printing=1):
        """Game.repeated_play(games) plays games games.
        The second optional parameter printing controls how much information should be printed."""
        wins = [0,0,0]
        for i in range(games):
            self.reset()
            wins[self.play(printing)] += 1
            if max(wins[1],wins[2]) > (games-wins[0])/2:
                break
        if printing>0: print("------------")
        if wins[1] > wins[2]:
            self.r_winner = 1
            if printing>0: print("Player 1 ("+self.s1.__class__.__name__+") wins")
        elif wins[1] < wins[2]:
            self.r_winner = 2
            if printing>0: print("Player 2 ("+self.s2.__class__.__name__+") wins")
        else:
            self.r_winner = 0
            if printing>0: print("It's a draw!")
        if printing>0:
            print("  Player 1 won {0} games ({1}%).".format(str(wins[1]),100*wins[1]/games))
            print("  Player 2 won {0} games ({1}%).".format(str(wins[2]),100*wins[2]/games))
            print("  There were {0} draws ({1}%).".format(str(wins[0]),100*wins[0]/games))

    def play(self,printing=2):
        """Plays one game.
        The second optional parameter printing controls how much information should be printed."""
        while True:
            signal.signal(signal.SIGALRM,alarm_handler)
            signal.alarm(5)
            fake_board = self.board.copy()
            if self.turn == 1:
                while True:
                    try:
                        p1 = self.s1.play(fake_board)
                        self.put_in(1,p1)
                        self.turn = 2
                        break
                    except MoveError:
                        pass
            else:
                while True:
                    try:
                        p2 = self.s2.play(fake_board)
                        self.put_in(2,p2)
                        self.turn = 1
                        break
                    except MoveError:
                        pass
            if printing>1:
                print(" ")
                print(self)
            winner = self.winner()
            if winner is not None:
                break
            signal.alarm(0)
        if winner == 0:
            if printing>0: print("Game is a draw")
            self.s1.draw()
            self.s2.draw()
            return 0
        elif winner == 1:
            if printing>0: print("Player 1 ("+self.s1.__class__.__name__+", by "+self.s1.author+") wins")
            self.s1.win()
            self.s2.lose()
            return 1
        elif winner == 2:
            if printing>0: print("Player 2 ("+self.s2.__class__.__name__+", by "+self.s2.author+") wins")
            self.s2.win()
            self.s1.lose()
            return 2
        else:
            raise ResultError

    def winner(self):
        """Tests to see if someone has won.
        Returns number of winning player or None."""
        return self.board.winner()
