#!/usr/bin/env python3

# Break part 2 into separate file
# solve1.py needs to run first to create board.txt

import numpy as np
import sys

# Quit immediately if board.txt not available
try:
    f = open('board.txt', 'r')
except:
    print('run solve1.py to generate board.txt first')
    exit(0)

# Could count lines but we already know dimensions
width = 47
heigth = 65
# New this day. Try out 2d numpy arrays.
# Note to self: access tiles as board[y, x]
# Can skip get_tile and put_tile functions.
board = np.zeros((heigth, width), dtype = np.int)

# Store idx values in board, write tile values when rendering
tile2idx = { '.' : 0, '#' : 1, 'O' : 2, '^' : 3, '>' : 4, 'v' : 5, '<' : 6, '*' : 7 }
idx2tile = { 0 : '.', 1 : '#', 2 : 'O', 3 : '^', 4 : '>', 5 : 'v', 6 : '<', 7 : '*' }
move2tile = { 'up' : 3, 'right' : 4, 'down' : 5, 'left' : 6 }

# Read output from solve1.py from board.txt
y = 0
for line in f:
    line = line.rstrip()
    x = 0
    for c in line:
        i = tile2idx[c]
        board[y, x] = i
        x += 1
    y += 1
f.close()

def clrscr():
    print('\033[2J\033[1;1H')

def goto00():
    print('\033[0;0H')

def render_board():
    for y in range(heigth):
        for x in range(width):
            sys.stdout.write(idx2tile[board[y, x]])
        sys.stdout.write('\n')

moves = { 'up' : np.array([ 0,-1], dtype = np.int),
        'down' : np.array([ 0, 1], dtype = np.int),
        'left' :  np.array([-1, 0], dtype = np.int),
        'right' :  np.array([ 1, 0], dtype = np.int) }

turnright = { 'up' : 'right', 'right' : 'down', 'down' : 'left', 'left' : 'up' }
turnleft = { 'up' : 'left', 'left' : 'down', 'down' : 'right', 'right' : 'up' }

# Got startpos and dir from solve1.py
robot = np.array([38, 28], dtype = np.int)
rdir = 'up'
rsteps = 0

def get_move_pos(pos, movedir):
    change = moves[movedir]
    x, y = pos + change
    if x < 0 or x > width - 1 or y < 0 or y > heigth - 1:
        # Outside board
        return False
    else:
        return np.array([x, y], dtype = np.int)

# Return tile value one position from pos in movedir
def get_tile_move(pos, movedir):
    newpos = get_move_pos(pos, movedir)
    # If bool then it returned False
    if type(newpos) == type(False):
        return False
    return board[newpos[1], newpos[0]]

# Return list of [y, x] positions for tiles with value tile
def get_yx_list(tile):
    lst = list(np.where(x == tile))
    return lst

# Return list of neigbouring scaffold positions
def get_neigh_scaffolds(pos):
    neighbours = []
    for movedir in ['up', 'down', 'left', 'right']:
        tile = get_tile_move(pos, movedir)
        if type(tile) != type(False) and (tile == 1 or tile == 7):
            neighbours.append(movedir)
    return neighbours

lastturn = 'L'
path = []

# Could get movements manually, but let's do it
# programmatically to learn numpy
def move_robot():
    global rsteps, rdir, robot, lastturn, path
    neighs = get_neigh_scaffolds(robot)
    # Set current to visited
    board[robot[1], robot[0]] = 7
    if rdir in neighs:
        # Continue forward
        rsteps += 1
        change = moves[rdir]
        robot += change
        board[robot[1], robot[0]] = move2tile[rdir]
        return True
    if turnleft[rdir] in neighs:
        # Turn left
        if rsteps > 0:
            # Save path movement
            path.append(lastturn + str(rsteps))
        lastturn = 'L'
        rsteps = 1
        rdir = turnleft[rdir]
        change = moves[rdir]
        robot += change
        board[robot[1], robot[0]] = move2tile[rdir]
        return True
    if turnright[rdir] in neighs:
        # Turn right
        if rsteps > 0:
            # Save path movement
            path.append(lastturn + str(rsteps))
        lastturn = 'R'
        rsteps = 1
        rdir = turnright[rdir]
        change = moves[rdir]
        robot += change
        board[robot[1], robot[0]] = move2tile[rdir]
        return True

    # Reached end, append last
    path.append(lastturn + str(rsteps))
    return False

while move_robot():
    #render_board()
    #input('')
    pass
render_board()

print('Organize output from line below into three groups and put it into solve2b.py')
print(path)
