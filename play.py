#!/usr/bin/env python

from core import Game

from strategies.random_strategy import RandomStrategy
from strategies.lowest_column import LowestColumnStrategy
from strategies.vertical_search import VerticalSearcher
from strategies.human_play import HumanPlay

random = RandomStrategy()
lowest = LowestColumnStrategy()
human = HumanPlay()
vertical = VerticalSearcher()

game = Game(lowest,vertical)

game.play(2)
#game.repeated_play(10)
