CONNECT 4
=========

Introduction
------------
This repository is designed to play games of Connect Four between the bots
saved in the strategies folder.

``play.py`` will play a match between two bots and can be used to test
strategies. The HumanPlay bot can be used to allow you to play against your
bot for testing. If you are using a non-UNIX system, the board may display
incorrectly due to the way colours are displayed. To correct this, change the
first lines of core/board_module.py to ``RED = ""``, ``BLUE = ""`` and
``DEFAULT = ""``.

``tournament.py`` will find all the bots in the strategies folder and play
them against each other.

Making a Strategy
-----------------
To make a strategy, create a new file with a ``.py`` extension in the
strategies folder (eg. ``my_strategy.py``). The file should look as follows:

    from core import Strategy
    
    class NameOfMyStrategy(Strategy):
        def __init__(self):
            self.author = "Your Name"
    
        def play(self,board):
            # Your strategy goes here
            return column_number_to_move_in

Additionally you can add:

        def start(self):
            # This will run when a new game is stared with your strategy.

        def win(self):
            # This will run when your strategy wins.

        def lose(self):
            # This will run when your strategy loses.

        def draw(self):
            # This will run when you strategy draws.

Your strategy class must inherit from ``core.Strategy`` otherwise 
``tournament.py`` will not be able to find it. Your strategy class must 
include the functions ``__init__`` and ``play``:

*   ``__init__(self)`` should be used to set the author (``self.author``) of
    the strategy. This will be used by ``tournament.py`` when the final
    results are displayed.

*   ``play(self,board)`` should return the number of the column you would like
    to play in (0 to 6). ``board`` will be an instance of ``core.Board``, and
    will tell you what the game board currently looks like. Details of the
    ``Board`` class are below.

In your strategy, ``self.turn`` will have a value of either 1 or 2. This will
tell you whether you are player one or player two (respectively).

The ``Board`` Class
-------------------
The ``Board`` class will tell you what the game board currently looks like.
Each cell on the ``Board`` will be set to either 1, 2 or 0 to reflect player
one, player two and nobody having a piece there respectively.

The ``Board`` class has the following functionality:

*   ``Board[a,b]`` will return the piece in row a and column b of the board. The
    rows are numbered from the top and the columns are numbered from the left,
    the same as is usual for numbering matrices.

*   ``Board.all_rows()``, ``Board.all_cols()``, ``Board.all_forward_diags()`` and
    ``Board.all_backward_diags()`` will return a list of all the rows, columns,
    forward diagonals (/) and backward diagonals (\\) of the board
    (respectively).

*   ``Board.row(n)``, ``Board.col(n)``, ``Board.forward_diag(n)`` and
    ``Board.backward_diag(n)`` will return the nth row, column, forward diagonal
    and backward diagonal (respectively).

*   ``Board.copy()`` will return an instance of Board which is a copy of the
    current board but can be changed without changing the current board. This
    could be useful for planning ahead moves.
