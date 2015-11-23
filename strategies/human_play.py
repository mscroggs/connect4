from core import Strategy
from core.board_module import pieces_list

class HumanPlay(Strategy):
    def __init__(self):
        self.author = "Matthew Scroggs"

    def play(self,board):
        global input
        print("\n\nThe board looks like this:")
        print(board)
        print("\nYou are playing as "+pieces_list[self.turn]+".")
        try:
            input = raw_input
        except NameError:
            pass

        ready = False
        while not ready:
            try:
                pl = int(input("Please enter the column you would like to play in then press Enter:"))
                if board[0][pl]==0:
                    ready = True
                else:
                    print("Column full. Try again...")
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except:
                pass
        return pl
