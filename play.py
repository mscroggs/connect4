#!/usr/bin/env python

from core import Game

from strategies.random_strategy import RandomStrategy
from strategies.human_play import HumanPlay

random = RandomStrategy()
human = HumanPlay()

game = Game(random,human)
game.play(1)
