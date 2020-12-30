#!/usr/bin/env python3

import numpy as np
from math import ceil
from collections import deque
import sys
sys.path.insert(0,'../common')
from intmachine import Intmachine
from statistics import mean, median

def dump_board():
    np.savetxt(sys.stdout.buffer, board, fmt='%d', delimiter = '')

# Return list of (y, x) positions for tiles with value tile
def get_yx_list(tile):
    res = np.where(board == tile)
    return list(zip(res[0], res[1]))

# Get value at x, y
def get_xy(x, y):
    m.reset()
    m.push(x)
    m.push(y)
    while m.do_op():
        pass
    return m.pop()

# Get min and max y values for beam at x
# k1, k2 = approximation of slope for beam lines
def get_y1y2(x):
    global k1, k2
    y1 = int(k1 * x)
    y2 = int(k2 * x)
    v = get_xy(x, y1)
    while v == 1:
        y1 -= 1
        v = get_xy(x, y1)
    while v == 0:
        y1 += 1
        v = get_xy(x, y1)

    v = get_xy(x, y2)
    while v == 1:
        y2 += 1
        v = get_xy(x, y2)
    while v == 0:
        y2 -= 1
        v = get_xy(x, y2)
    return(y1, y2)

def get_rect_heigth(x, side):
    y1, y2 = get_y1y2(x)
    x2 = x + side - 1
    y3, y4 = get_y1y2(x2)
    return (y2, y2 - y3 + 1)

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

# Dimensions = 50 x 50
width = 50
heigth = 50
board = np.zeros((heigth, width), dtype = np.int)

# Create and connect machines
m = Intmachine('d19', prog, queues[0], queues[1])
# Fill board and count ones
for y in range(heigth):
    for x in range(width):
        board[(y, x)] = get_xy(x, y)
dump_board()
print('part 1:', len(get_yx_list(1)))
# Get approximation of slopes around x = 1000
x = 1000
k1 = 0.4
k2 = 0.7
lasty1, lasty2 = get_y1y2(x)
k1 = lasty1 / x
k2 = lasty2 / x
# Adjust range until it works
for x in range(1000, 1020):
    y, side = get_rect_heigth(x, 100)
    if side == 100:
        print(x, y, side)
        print(x * 10000 + (y - 100 + 1))
        break
    #print(x, get_rect_heigth(x, 100))
