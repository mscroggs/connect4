from core.errors import MoveError,ResultError,Alarm
from core.board_module import Board
import signal

def alarm_handler(signum,frame):
    raise Alarm

def four_in_a_row(row):
    run = 0
    for j,val in enumerate(row):
        if j==0:
            run += 1
        elif val == row[j-1] and val!=0:
            run += 1
        else:
            run = 1
        if run == 4 and val!=0:
            return val
    return None

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
        self.r_winner = 0
        self.board = Board(self.row_num,self.col_num)
        self.turn = 1

    def __str__(self):
        return self.board.__str__()

    def put_in(self,player,column):
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
        while True:
            signal.signal(signal.SIGALRM,alarm_handler)
            signal.alarm(5)
            fake_board = Board(self.row_num,self.col_num)
            fake_board.board = self.board.rows()
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
            return 0
        elif winner == 1:
            if printing>0: print("Player 1 ("+self.s1.__class__.__name__+", by "+self.s1.author+") wins")
            return 1
        elif winner == 2:
            if printing>0: print("Player 2 ("+self.s2.__class__.__name__+", by "+self.s2.author+") wins")
            return 2
        else:
            raise ResultError

    def winner(self):
        #is it a draw?
        if 0 not in self.board[0]:
            return 0
        #horizontal
        for row in self.board.rows():
            result = four_in_a_row(row)
            if result is not None:
                return result
        #vertical
        for col in self.board.cols():
            result = four_in_a_row(col)
            if result is not None:
                return result

        #/ diagonals
        for diag in self.board.forward_diags():
            result = four_in_a_row(diag)
            if result is not None:
                return result

        #\ diagonals
        for diag in self.board.backward_diags():
            result = four_in_a_row(diag)
            if result is not None:
                return result
            
        return None
