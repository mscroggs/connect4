from core.errors import MoveError,ResultError

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
        self.rows = rows
        self.cols = cols
        self.s1 = s1
        self.s2 = s2
        self.s1_moves = []
        self.s2_moves = []
        self.s1.my_moves = self.s1_moves
        self.s1.your_moves = self.s2_moves
        self.s1.turn = 1
        self.s1.game = self
        self.s2.my_moves = self.s2_moves
        self.s2.your_moves = self.s1_moves
        self.s2.turn = 2
        self.s2.game = self
        self.turn = 1
        self.reset()

    def reset(self):
        self.board = [[0]*self.cols for i in range(self.rows)]
        self.s1_moves = []
        self.s2_moves = []
        self.turn = 1

    def row(self,i):
        return self.board[i]

    def col(self,i):
        return [row[i] for row in self.board]

    def __str__(self):
        output = "\n".join((" ".join(str(i) for i in row) for row in self.board))
        return output

    def put_in(self,player,column):
        col = self.col(column)
        row = None
        for i,val in enumerate(col):
            if val == 0:
                row = i
            else:
                break
        if row is None:
            raise MoveError("The column you tried to play in is full")
        
        self.board[row][column] = player

    def repeated_play(self,games):
        wins = [0,0,0]
        for i in range(games):
            self.reset()
            wins[self.play(1)] += 1
        print("------------")
        if wins[1] > wins[2]:
            print("Player 1 ("+self.s1.__class__.__name__+") wins")
        elif wins[1] < wins[2]:
            print("Player 2 ("+self.s2.__class__.__name__+") wins")
        else:
            print("It's a draw!")
        print("  Player 1 won {0} games ({1}%).".format(str(wins[1]),100*wins[1]/games))
        print("  Player 2 won {0} games ({1}%).".format(str(wins[2]),100*wins[2]/games))
        print("  There were {0} draws ({1}%).".format(str(wins[0]),100*wins[0]/games))

    def play(self,printing=2):
        while True:
            if self.turn == 1:
                p1 = self.s1.play()
                self.put_in(1,p1)
                self.turn = 2
            else:
                p2 = self.s2.play()
                self.put_in(2,p2)
                self.turn = 1
            if printing>1:
                print(" ")
                print(self)
            winner = self.winner()
            if winner is not None:
                break
        if winner == 0:
            if printing>0: print("Game is a draw")
            return 0
        elif winner == 1:
            if printing>0: print("Player 1 ("+self.s1.__class__.__name__+") wins")
            return 1
        elif winner == 2:
            if printing>0: print("Player 2 ("+self.s2.__class__.__name__+") wins")
            return 2
        else:
            raise ResultError

    def winner(self):
        #is it a draw?
        if 0 not in self.board[0]:
            return 0
        #horizontal
        for row in self.board:
            result = four_in_a_row(row)
            if result is not None:
                return result
        #vertical
        for i in range(self.cols):
            col = self.col(i)
            result = four_in_a_row(col)
            if result is not None:
                return result
        #/ diagonals
        for i in range(3,self.cols):
            diag = []
            n = 0
            while n<self.rows and i-n>=0:
                diag.append(self.board[n][i-n])
                n+=1
            result = four_in_a_row(diag)
            if result is not None:
                return result
        for i in range(1,self.rows-3):
            diag = []
            n = 0
            while i+n<self.rows and n<self.cols:
                diag.append(self.board[i+n][-1-n])
                n+=1
            result = four_in_a_row(diag)
            if result is not None:
                return result
        #\ diagonals
        for i in range(3,self.cols):
            diag = []
            n = 0
            while n<self.rows and i-n>=0:
                diag.append(self.board[-1-n][i-n])
                n+=1
            result = four_in_a_row(diag)
            if result is not None:
                return result
        for i in range(1,self.rows-3):
            diag = []
            n = 0
            while i+n<self.rows and n<self.cols:
                diag.append(self.board[-1-i-n][-1-n])
                n+=1
            result = four_in_a_row(diag)
            if result is not None:
                return result
                
        return None
