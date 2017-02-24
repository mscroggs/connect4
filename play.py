#!/usr/bin/env python

from core import Game

from strategies.random_strategy import RandomStrategy
from strategies.human_play import HumanPlay
# from strategies.first_bot import Bot1

random = RandomStrategy()
human = HumanPlay()
# bot1 = Bot1()

game = Game(random,human)
# game = Game(bot1,human)

game.play(1)
