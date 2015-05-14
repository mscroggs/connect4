#!/usr/bin/env python

from core import Game

from strategies.random_strategy import RandomStrategy
from strategies.lowest_column import LowestColumnStrategy
from strategies.human_play import HumanPlay

random = RandomStrategy()
lowest = LowestColumnStrategy()
human = HumanPlay()

game = Game(human,lowest)

game.play()
#game.repeated_play(10)
