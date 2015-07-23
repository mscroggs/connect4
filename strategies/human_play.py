from core import Strategy
from core.board_module import pieces_list

class HumanPlay(Strategy):
    def __init__(self):
        self.author = "Matthew Scroggs"

    def play(self,board):
        print("\n\nThe board looks like this:")
        print(board)
        print("\nYou are playing as "+pieces_list[self.turn]+".")

        ready = False
        while not ready:
            try:
                pl = int(raw_input("Please enter the column you would like to play in then press Enter:"))
                if board[0][pl]==0:
                    ready = True
                else:
                    print("Column full. Try again...")
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except:
                pass
        return pl
