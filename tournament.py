#!/usr/bin/env python

import os
from core import Game,Strategy

from strategies.human_play import HumanPlay

def is_strategy_file(f):
    if not os.path.isfile(os.path.join(pages_dir, f)):
        return False
    if "pyc" in f:
        return False
    if "__" in f:
        return False
    return True

pages_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "strategies")
strategy_files = [f for f in os.listdir(pages_dir) if is_strategy_file(f)]

strategies = []

for file in strategy_files:
    file_no_ext = os.path.splitext(file)[0]
    module = getattr(__import__("strategies", fromlist=[file_no_ext]),
                     file_no_ext)
    reload(module)
    for object in dir(module):
        obj = getattr(module, object)
        try:
            try_me = obj()
            if issubclass(obj, Strategy) and obj.__name__!=Strategy.__name__ and obj.__name__!=HumanPlay.__name__:
                strategies.append(try_me)
        except:
            pass

points = [0]*len(strategies)

max_len = 2
max_a_len = 2


for i1,s1 in enumerate(strategies):
    max_len = max(max_len,len(s1.__class__.__name__)+2)
    max_a_len = max(max_a_len,len(s1.author)+2)
    for i2,s2 in enumerate(strategies):
        if i1!=i2:
            game = Game(s1,s2)
            game.repeated_play(10,0)
            if game.r_winner==0:
                points[i1]+=1
                points[i2]+=1
            if game.r_winner==1:
                points[i1]+=3
            if game.r_winner==2:
                points[i2]+=3

for i,p in enumerate(points):
    nom = strategies[i].__class__.__name__
    aut = strategies[i].author
    print nom + " "*(max_len-len(nom)) + aut + " "*(max_a_len-len(aut)) + str(p)
