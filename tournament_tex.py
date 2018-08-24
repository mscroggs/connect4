#!/usr/bin/env python

import os
from core import Game,Strategy,Board
from core.errors import ResultError,Alarm
from time import sleep
from strategies.human_play import HumanPlay
from random import randrange
from math import floor

number_of_games = 100

try:
    import thread
except ImportError:
    import _thread as thread

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
                game.repeated_play(number_of_games,0)
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

tex_output = """\\documentclass{article}
\\usepackage{tikz}
\\usepackage{geometry}
\\geometry{
    papersize={200mm,150mm},
    top=5mm,left=5mm,right=5mm,bottom=5mm
    }
\\begin{document}
\\begin{tabular}{|l|l|c|c|c|c|c|c|}
\\hline
\\#&Name of Bot&Programmer&Points&Wins&Draws&Loses&Total Games Won\\\\
\\hline
\\hline
"""

prev_p = -1
c_n = 0
done = False

def strc(t):
    t = str(t)
    return "\\_".join(t.split("_"))

for i,item in enumerate(leaderboard):
    if item[2] != prev_p: c_n = i+1
    print("   "+item[0] + " "*(max_len-len(item[0])) + item[1] + " "*(max_a_len-len(item[1])) + str(item[2]))
    tex_output += strc(c_n) + "&"
    if i<4:
        tex_output += "\\textbf{"
    tex_output += strc(item[0])
    if i<4:
        tex_output += "}"
    tex_output += "&"
    if i<4:
        tex_output += "\\textbf{"
    tex_output += strc(item[1])
    if i<4:
        tex_output += "}"
    tex_output += "&"
    tex_output += "\\textbf{" + strc(item[2]) + "}&"
    tex_output += strc(item[3]) + "&"
    tex_output += strc(item[2]-item[3]*3) + "&"
    tex_output += strc(len(leaderboard)*2-2-item[2]+item[3]*2) + "&"
    tex_output += strc(item[4])
    tex_output += "\\\\\\hline"
    prev_p = item[2]

tex_output += "\\end{tabular}\n\n"
tex_output += "\\newpage"

final_round = [strategies[item[5]] for item in leaderboard[:4]]

print("   Preparing final round...")

def match(st1,st2):

    game1 = Game(st1,st2)
    game2 = Game(st2,st1)
    game1.repeated_play(number_of_games,0)
    game2.repeated_play(number_of_games,0)

    if game1.w1+game2.w2 >= 50:
        return (1,st1)
    else:
        return (2,st2)

i1,win1 = match(final_round[0],final_round[3])
i2,win2 = match(final_round[1],final_round[2])
i3,win3 = match(win1,win2)

def get_moves_to_show(st1,st2,win):
    game = Game(st1,st2)
    done = False
    while not done:
        try:
            game.play(0)
            done = True
        except Alarm:
            done = False
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

WHITE=""
RED=""
BLUE=""

pieces = [WHITE,RED,BLUE]

match_names = ["Semi Final 1","Semi Final 2","The Final"]

for i,match in enumerate(matches):

    title_page = "\\begin{center}\\Huge{\\textbf{"+ match_names[i] +"}}\\end{center}\n\n"

    for i in range(2):
        title_page += "\\begin{minipage}{.4\\textwidth}\n"
        title_page += "\\begin{center}\n"
        title_page += strc(match[i].__class__.__name__) + "\\\\"
        title_page += strc(match[i].author) + "\\\\"
        title_page += "\\begin{tikzpicture}\n"
        if i==0:
            title_page += "\\filldraw[fill=red] (0mm,0mm) circle (7mm);\n"
        if i==1:
            title_page += "\\filldraw[fill=yellow] (0mm,0mm) circle (7mm);\n"
        title_page += "\\end{tikzpicture}\n"
        title_page += "\\end{center}\n"
        title_page += "\\end{minipage}"
        if i==0:
            title_page += "\\hfill"
        if i==1:
            title_page += "\n"

    tex_output += title_page+"\\newpage"

    board = [[0 for j in range(7)] for k in range(6)]
    turn = 1
    for go_num,go in enumerate(match[2]):
        for j,row in enumerate(board):
            if row[go]!=0:
                j -= 1
                break
        board[j][go] = turn
        turn = 3-turn
        tex_output += title_page
        tex_output += "\\begin{center}\n\\begin{tikzpicture}\n"
        tex_output += "\\filldraw[fill=cyan] (-8mm,-8mm) rectangle (104mm,88mm);\n"
        for j,row in enumerate(board):
            for i,piece in enumerate(row):
                tex_output += "\\filldraw[fill="
                if piece == 0: tex_output += "white"
                if piece == 1: tex_output += "red"
                if piece == 2: tex_output += "yellow"
                tex_output += "] ("
                tex_output += str(i*16)
                tex_output += "mm,"
                tex_output += str(80-j*16)
                tex_output += "mm) circle (7mm);\n"
        tex_output += "\\end{tikzpicture}\n\\end{center}"
        tex_output += "\\newpage\n\n"
    tex_output += "\\newpage"


tex_output += "\end{document}"

with open("results.tex","w") as f:
    f.write(tex_output)

os.system("pdflatex results.tex")
