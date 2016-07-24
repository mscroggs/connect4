#!/usr/bin/env python

import os
from core import Game,Strategy,Board
from core.errors import ResultError,Alarm
from time import sleep
from strategies.human_play import HumanPlay
from random import randrange
from math import floor

def is_strategy_file(f):
    if not os.path.isfile(os.path.join(pages_dir, f)):
        return False
    if "pyc" in f:
        return False
    if "__" in f:
        return False
    if ".py" not in f:
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
wins = [0]*len(strategies)
tot_wins = [0]*len(strategies)

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
                tot_wins[i1] += game.w1
                tot_wins[i2] += game.w2
                if game.r_winner==0:
                    points[i1]+=1
                    points[i2]+=1
                    print("  It's a draw!")
                if game.r_winner==1:
                    points[i1]+=3
                    wins[i1]+=1
                    print("  "+s1.__class__.__name__+" wins!")
                if game.r_winner==2:
                    points[i2]+=3
                    wins[i2]+=1
                    print("  "+s2.__class__.__name__+" wins!")

            except Alarm:
                if game.turn == 1:
                    print("  "+game.s1.__class__.__name__+" took too long to move")
                if game.turn == 2:
                    print("  "+game.s2.__class__.__name__+" took too long to move")

            except ResultError:
                print("  ResultError. Continuing tournament.")

            print("")

print("    Name" + " "*(max_len-4) + "Programmer" + " "*(max_a_len-10) + "Points")

leaderboard = [(strategies[i].__class__.__name__,strategies[i].author,p,wins[i],tot_wins[i],i) for i,p in enumerate(points)]
leaderboard = sorted(leaderboard,key=lambda item:(-item[2],-item[3],-item[4]))

html_output = """<html>
<head>
<style type='text/css'>
table,td {border:1px solid #444444;border-collapse:collapse}
tr.out td {border-top:3px solid black}
td {padding:3px;text-align:center}
thead td {font-weight:bold}
</style>
</head>

<body>

<table>
<thead><td>#</td><td>Name of Bot</td><td>Programmer</td><td>Points</td><td>Wins</td><td>Draws</td><td>Loses</td><td>Total Games Won</td></thead>
"""

prev_p = -1
c_n = 0
done = False

for i,item in enumerate(leaderboard):
    if item[2] != prev_p: c_n = i+1
    print("   "+item[0] + " "*(max_len-len(item[0])) + item[1] + " "*(max_a_len-len(item[1])) + str(item[2]))
    html_output += "<tr"
    if i==4: html_output += " class='out'"
    html_output += ">"
    html_output += "<td>" + str(c_n) + "</td>"
    html_output += "<td>" + item[0] + "</td>"
    html_output += "<td>" + item[1] + "</td>"
    html_output += "<td><b>" + str(item[2]) + "</b></td>"
    html_output += "<td>" + str(item[3]) + "</td>"
    html_output += "<td>" + str(item[2]-item[3]*3) + "</td>"
    html_output += "<td>" + str(len(leaderboard)*2-2-item[2]+item[3]*2) + "</td>"
    html_output += "<td>" + str(item[4]) + "</td>"
    html_output += "</tr>\n"
    tr = "tr"
    prev_p = item[2]

html_output += "</table>\n\n</body>\n</html>"

with open("results.html","w") as f:
    f.write(html_output)

final_round = [strategies[item[5]] for item in leaderboard[:4]]

print("   Preparing final round...")

def match(st1,st2):

    game1 = Game(st1,st2)
    game2 = Game(st2,st1)
    game1.repeated_play(50,0)
    game2.repeated_play(50,0)

    if game1.w1+game2.w2 >= 50:
        return (1,st1)
    else:
        return (2,st2)

i1,win1 = match(final_round[0],final_round[3])
i2,win2 = match(final_round[1],final_round[2])
i3,win3 = match(win1,win2)

def get_moves_to_show(st1,st2,win):
    game = Game(st1,st2)
    game.play(0)
    if game.winner() == win:
        return (st1,st2,game.get_all_moves(),win)
    else:
        return get_moves_to_show(st2,st1,3-win)
matches = [
           get_moves_to_show(final_round[0],final_round[3],i1),
           get_moves_to_show(final_round[1],final_round[2],i2),
           get_moves_to_show(win1,win2,i3)
          ]
print("   Final round ready")

raw_input("Press Enter to start the final round...")
RED   = "\033[41m \033[0m"
BLUE  = "\033[44m \033[0m"
WHITE = "\033[107m \033[0m"

pieces = [WHITE,RED,BLUE]

match_names = ["Semi Final 1","Semi Final 2","The Final"]

for i,match in enumerate(matches):
    match_details = match_names[i]
    match_details += "\n"
    width1 = max(len(match[0].__class__.__name__),len(match[0].author))
    width2 = max(len(match[1].__class__.__name__),len(match[1].author))
    match_details += "   "+pieces[1]*(4+width1) + "    " + pieces[2]*(4+width2)
    match_details += "\n"
    match_details += "   "+pieces[1]+" "+match[0].__class__.__name__+(" "*(width1-len(match[0].__class__.__name__)))+" "+pieces[1]
    match_details += " vs "
    match_details += pieces[2]+" "+(" "*(width2-len(match[1].__class__.__name__)))+match[1].__class__.__name__+" "+pieces[2]
    match_details += "\n"
    match_details += "   "+pieces[1]+" "+match[0].author+(" "*(width1-len(match[0].author)))+" "+pieces[1]
    match_details += "    "
    match_details += pieces[2]+" "+(" "*(width2-len(match[1].author)))+match[1].author+" "+pieces[2]
    match_details += "\n"
    match_details += "   "+pieces[1]*(4+width1) + "    " + pieces[2]*(4+width2)
    match_details += "\n"

    print("\n"*3 + match_details)
    raw_input("Press Enter to begin...")
    board = [[0 for j in range(7)] for k in range(6)]
    turn = 1
    for go_num,go in enumerate(match[2]):
        for j,row in enumerate(board):
            if row[go]!=0:
                j -= 1
                break
        board[j][go] = turn
        turn = 3-turn
        all_lines = []
        for row in board:
            next_lines = [" "*3]*4
            for piece in row:
                for j in range(3):
                    next_lines[j] += pieces[piece]*4+" "
            all_lines.append("\n".join(next_lines))
        print("\n"*20)
        print(match_details)
        print("\n"*5)
        print("\n".join(all_lines))
        if go_num < len(match[2]) - 1:
            raw_input("")
        else:
            sleep(1)
            w = match[3]
            if i == 2:
                print(pieces[w]+match[w-1].__class__.__name__ + " by " + match[w-1].author + pieces[w] + " has won!")
                sleep(1)
                print("\nThe End\n")
            else:
                print(pieces[w]+match[w-1].__class__.__name__ + " by " + match[w-1].author + pieces[w] + " goes through to the next round!")
                raw_input("Press Enter to continue...")

