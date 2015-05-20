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
        pieces = [".","o","x"]
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

    def rows(self):
        return self.board

    def row(self,row_n):
        return [[self.board[row][col] for col in range(self.col_num)] for row in range(self.row_num)]

    def cols(self):
        return [[self.board[row][col] for row in range(self.row_num)] for col in range(self.col_num)]

    def col(self,col_n):
        return self.cols()[col_n]

    def forward_diags(self):
        return (
                    [[self.board[i][col-i] for i in range(min(col+1,self.row_num))] for col in range(self.col_num)]
                  + [[self.board[i][row-1-i] for i in range(row,self.row_num)] for row in range(1,self.row_num)]
               )

    def forward_diag(self,d_n):
        return self.forward_diags()[d_n]

    def backward_diags(self):
        return (
                    [[self.board[row+i][i] for i in range(self.row_num-row)] for row in range(self.row_num-1,0,-1)]
                  + [[self.board[i][col+i] for i in range(min(self.col_num-col,self.row_num))] for col in range(self.col_num)]
               )

    def backward_diag(self,d_n):
        return self.backward_diags()[d_n]
