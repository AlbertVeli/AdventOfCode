#!/usr/bin/env python3

# This needs cleanup. Anyway, run
# solve1.py and solve2a.py. Then
# manually analyze output from solve2a.py
# and put result into beginning of solve2b.py.
# See groups.txt which have been manually organized.

import numpy as np
from collections import deque
# Use intmachine from ../common
import sys
sys.path.insert(0,'../common')
from intmachine import Intmachine

# Read program from input.txt
with open('input.txt') as f:
    line = f.readline()
prog = []
for i in map(int, line.split(',')):
    prog.append(i)

# Create queues
queues = []
for _ in range(2):
    dq = deque()
    queues.append(dq)

# Create and connect machines
m = Intmachine('d17', prog, queues[0], queues[1])
m.reset()
while m.do_op():
    pass

# get output data
output = ''
while len(m.oq) > 0:
    output += chr(m.pop())

# Dimensions = 47 x 65
width = 47
heigth = 65
board = np.array([0] * width * heigth, dtype = np.int)
ytab = np.array([0] * heigth, dtype = np.int)

moves = { 'up' : np.array([ 0,-1], dtype = np.int),
        'down' : np.array([ 0, 1], dtype = np.int),
        'left' :  np.array([-1, 0], dtype = np.int),
        'right' :  np.array([ 1, 0], dtype = np.int) }

# Store idx values in board
tile2idx = { '.' : 0, '#' : 1, 'O' : 2, '^' : 3, '>' : 4, 'v' : 5, '<' : 6 }
idx2tile = { 0 : '.', 1 : '#', 2 : 'O', 3 : '^', 4 : '>', 5 : 'v', 6 : '<' }

def put_tile(x, y, tile):
    board[ytab[y] + x] = tile

def get_tile(x, y):
    return board[ytab[y] + x]

def index_to_xy(i):
    x = i % width
    y = i // width
    return np.array([x, y], dtype = np.int16)

def get_tile_move(pos, movedir):
    change = moves[movedir]
    x, y = pos + change
    return get_tile(x, y)

def clrscr():
    print('\033[2J\033[1;1H')

def goto00():
    print('\033[0;0H')

def render_board(outfile = False):
    if outfile:
        f = open(outfile, 'w')
    else:
        f = sys.stdout
    for y in range(heigth):
        for x in range(width):
            f.write(idx2tile[get_tile(x, y)])
        f.write('\n')
    if outfile:
        f.close()

# Fill board
lines = output.split('\n')
y = 0
for line in lines:
    if len(line) > 0:
        ytab[y] = y * width
        x = 0
        for c in line:
            if not c in tile2idx:
                print(c, 'not in found')
            put_tile(x, y, tile2idx[c])
            x += 1
        y += 1

def is_intersection(x, y):
    # No intersection can be on border
    if x > width - 2 or y > heigth - 2 or x < 1 or y < 1:
        return False
    pos = np.array([x, y], dtype = int)
    for m in ['up', 'down', 'left', 'right']:
        tile = get_tile_move(pos, m)
        if tile != 1:
            return False
    return True

# Return list of [x, y] positions for tiles with value tile
def get_xy_list(tile):
    lst = list(map(index_to_xy, np.where(board == tile)[0]))
    return lst

# This is needed by solve2a.py
render_board(outfile = 'board.txt')

# Put 2s at every scaffold intersection
scaffolds = get_xy_list(1)
for x, y in scaffolds:
    if is_intersection(x, y):
        put_tile(x, y, 2)

clrscr()
render_board()

isections = get_xy_list(2)
ans = 0
for x, y in isections:
    ans += x * y
print(ans)
robot = get_xy_list(tile2idx['^'])
rx = robot[0][0]
ry = robot[0][1]
print('robot is at: %d, %d facing up' % (rx, ry))
