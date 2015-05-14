from core import Strategy

class HumanPlay(Strategy):
    def play(self):
        print("\n\nThe board looks like this:")
        print(self.game)
        print("\nYou are playing as "+[".","o","x"][self.turn]+".")

        ready = False
        while not ready:
            try:
                pl = int(raw_input("Please enter the column you would like to play in the press Enter:"))
                if self.game.board[0][pl]==0:
                    ready = True
                else:
                    print("Column full. Try again...")
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except:
                pass
        return pl
