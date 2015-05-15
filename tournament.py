#!/usr/bin/env python

import os
from core import Game,Strategy
from core.errors import ResultError,Alarm
from time import sleep
from strategies.human_play import HumanPlay

def is_strategy_file(f):
    if not os.path.isfile(os.path.join(pages_dir, f)):
        return False
    # Comment the next two lines out to test with failing strategy
    if "failer" in f:
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

max_len = 6
max_a_len = 12

print("")

for i1,s1 in enumerate(strategies):
    max_len = max(max_len,len(s1.__class__.__name__)+2)
    max_a_len = max(max_a_len,len(s1.author)+2)
    for i2,s2 in enumerate(strategies):
        if i1!=i2:
            #sleep(2)
            print(s1.__class__.__name__+" vs. "+s2.__class__.__name__)
            #sleep(2)
            try:
                game = Game(s1,s2)
                game.repeated_play(100,0)
                if game.r_winner==0:
                    points[i1]+=1
                    points[i2]+=1
                    print("  It's a draw!")
                if game.r_winner==1:
                    points[i1]+=3
                    print("  "+s1.__class__.__name__+" wins!")
                if game.r_winner==2:
                    points[i2]+=3
                    print("  "+s2.__class__.__name__+" wins!")

            except Alarm:
                if game.turn == 1:
                    print("  "+game.s1.__class__.__name__+" took too long to move")
                if game.turn == 2:
                    print("  "+game.s2.__class__.__name__+" took too long to move")

            except ResultError:
                print("  ResultError. Continuing tournament.")

            print("")

print("Name" + " "*(max_len-4) + "Programmer" + " "*(max_a_len-10) + "Points")

leaderboard = [(strategies[i].__class__.__name__,strategies[i].author,p) for i,p in enumerate(points)]
leaderboard = sorted(leaderboard,key=lambda item:-item[2])

for item in leaderboard:
    print(item[0] + " "*(max_len-len(item[0])) + item[1] + " "*(max_a_len-len(item[1])) + str(item[2]))
