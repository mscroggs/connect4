from core import Game

from strategies.random_strategy import RandomStrategy
from strategies.lowest_column import LowestColumnStrategy

random = RandomStrategy()
lowest = LowestColumnStrategy()

game = Game(random,lowest)

game.play()

game.repeated_play(10)
