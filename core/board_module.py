# These colours may not work on non-UNIX. If the boards look weird, replace
# each with a blank string (eg. RED = "")
RED = "\033[31m"
BLUE = "\033[34m"
DEFAULT = "\033[0m"

class Board:
    def __init__(self,rows,cols):
        self.col_num = cols
        self.row_num = rows
        self.board = [[0]*cols for row in range(rows)]

    def __getitem__(self,A):
        if isinstance(A,tuple):
            return self.board[A[0]][A[1]]
        else:
            return self.board[A]

    def __setitem__(self,A,c):
        if isinstance(A,tuple):
            self.board[A[0]][A[1]] = c
        else:
            self.board[A] = c

    def __str__(self):
        pieces = [".",RED+"o"+DEFAULT,BLUE+"x"+DEFAULT]
        output = []
        for r,row in enumerate(self.board):
            line = ""
            for piece in row:
                line += pieces[piece]
            if r==0: line += " Player 1 is "+pieces[1]+"."
            if r==1: line += " Player 2 is "+pieces[2]+"."
            output.append(line)
        line = ""
        for i in range(len(row)):
            line += str(i)
        output.append(line)
        return "\n".join(output)

    def all_rows(self):
        """Returns a list of all rows."""
        return [[self.board[row][col] for col in range(self.col_num)] for row in range(self.row_num)]

    def row(self,row_n):
        """Board.row(row_n) returns row number row_n."""
        return self.all_rows()[row_n]

    def all_cols(self):
        """Returns a list of all columns."""
        return [[self.board[row][col] for row in range(self.row_num)] for col in range(self.col_num)]

    def col(self,col_n):
        """Board.col(col_n) returns column number col_n."""
        return self.all_cols()[col_n]

    def all_forward_diags(self):
        """Returns a list of all forward diagonals (/)."""
        return (
                    [[self.board[i][col-i] for i in range(min(col+1,self.row_num))] for col in range(self.col_num)]
                  + [[self.board[i][row-1-i] for i in range(row,self.row_num)] for row in range(1,self.row_num)]
               )

    def forward_diag(self,d_n):
        """Board.forward_diag(d_n) returns forward diagonal (/) number d_n."""
        return self.all_forward_diags()[d_n]

    def all_backward_diags(self):
        """Returns a list of all backward diagonals (\)."""
        return (
                    [[self.board[row+i][i] for i in range(self.row_num-row)] for row in range(self.row_num-1,0,-1)]
                  + [[self.board[i][col+i] for i in range(min(self.col_num-col,self.row_num))] for col in range(self.col_num)]
               )

    def backward_diag(self,d_n):
        """Board.backward_diag(d_n) returns backward diagonal (\) number d_n."""
        return self.all_backward_diags()[d_n]

    def copy(self):
        """Returns a copy of the board.
        This can be used to make a board which can be changed for planning ahead.
        """
        return_me = Board(self.row_num,self.col_num)
        return_me.board = self.all_rows()
        return return_me

    def winner(self):
        """Tests to see if someone has won.
        Returns number of winning player or None."""
        #horizontal
        for row in self.all_rows():
            result = four_in_a_row(row)
            if result is not None:
                return result
        #vertical
        for col in self.all_cols():
            result = four_in_a_row(col)
            if result is not None:
                return result

        #/ diagonals
        for diag in self.all_forward_diags():
            result = four_in_a_row(diag)
            if result is not None:
                return result

        #\ diagonals
        for diag in self.all_backward_diags():
            result = four_in_a_row(diag)
            if result is not None:
                return result

        #is it a draw?
        if 0 not in self[0]:
            return 0
            
        return None

def four_in_a_row(row):
    """Returns 1 if player 1 has won, 2 if player 2 has won, otherwise None."""
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

