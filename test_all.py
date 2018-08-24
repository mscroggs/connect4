#!/usr/bin/env python

import os
from core import Game,Strategy,Board
from core.errors import ResultError
from time import sleep
from strategies.random_strategy import RandomStrategy
from strategies.human_play import HumanPlay
from random import randrange
from math import floor

number_of_games = 1

def is_strategy_file(f):
    if not os.path.isfile(os.path.join(pages_dir, f)):
        return False
    if "pyc" in f:
        return False
    if "__" in f:
        return False
    if ".py" not in f:
        return False
    if ".swp" in f:
        return False
    return True

pages_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "strategies")
strategy_files = [f for f in os.listdir(pages_dir) if is_strategy_file(f)]

strategies = []

for file in strategy_files:
    file_no_ext = os.path.splitext(file)[0]
    module = getattr(__import__("strategies", fromlist=[file_no_ext]),
                     file_no_ext)
    for object in dir(module):
        obj = getattr(module, object)
        try:
            try_me = obj()
            if issubclass(obj, Strategy) and obj.__name__!=Strategy.__name__ and obj.__name__!=HumanPlay.__name__:
                strategies.append(try_me)
        except:
            pass

random = RandomStrategy()

for i1,s1 in enumerate(strategies):
    print("Testing "+s1.__class__.__name__)
    game = Game(s1, random)
    game.repeated_play(number_of_games,0)

