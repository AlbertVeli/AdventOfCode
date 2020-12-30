#!/usr/bin/env python3

import sys
import re
import numpy as np

moves = { 'e': (2, 0), 'se': (1, 2), 'sw': (-1, 2), 'w': (-2, 0), 'nw': (-1, -2), 'ne': (1, -2) }

# Save (x, y): True/False in tiles. True = black, False = white.
tiles = {}

for line in open(sys.argv[1]).read().splitlines():
    pos = np.array((0, 0))
    for d in re.findall(r'e|se|sw|w|nw|ne', line):
        pos += moves[d]
    t = tuple(pos)
    if t in tiles:
        tiles[t] = not tiles[t]
    else:
        tiles[t] = True

# Part 1
print('black:', sum(val == True for val in tiles.values()))

# -- Part 2 --

# take a chance on how wide it needs to be
width = 300
heigth = 300
board = np.zeros(width * heigth, dtype=np.int8)
board = board.reshape(heigth, width)

# Fill in tiles, move to center
for key, value in tiles.items():
    x, y = key
    x += width // 2
    y += heigth // 2
    board[y][x] = value

def black_neighbours(y, x, b):
    num = 0
    for m in moves.values():
        num += b[(y + m[1], x + m[0])]
    return num

def game():
    board_copy = np.copy(board)
    w, h = board.shape
    # Don't do outer edge (to avoid special cases)
    for y in range(2, h - 2):
        for x in range(2, w - 2):
            tile = board_copy[(y, x)]
            n = black_neighbours(y, x, board_copy)
            if tile:
                # black
                if n == 0 or n > 2:
                    board[(y, x)] = False
            else:
                # white
                if n == 2:
                    board[(y, x)] = True

# TODO: Start with a smaller grid and expand when necessary
for day in range(1, 101):
    game()
    print('Day %d: %d' % (day, len(np.where(board == True)[0])))

ys, xs = np.where(board)
print(min(ys), max(ys), min(xs), max(xs))
