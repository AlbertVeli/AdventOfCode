#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc
import copy

mtrx = aoc.char_matrix(sys.argv[1])

# unexpected twist
# use movie quotes as docstrings
# instead of useful explanations

def get_pipe(xy_tuple):
    """ the mind makes it real """
    x, y = xy_tuple
    return mtrx[y][x]

def new_pos(pos, dir):
    """
    it is not the spoon that bends
    it's only yourself
    """
    return tuple(a + b for a, b in zip(pos, dir))

# reach for the red pill
for y, line in enumerate(mtrx):
    if 'S' in line:
        x = line.index('S')
        break

# - he told me you killed him
# - no, I am your father

start_pos = (x, y)

# you ever dance with the devil in the pale moonlight?
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# current previous move
# |       DOWN     DOWN
# |       UP       UP
# ...
moves = {
    ('|', DOWN): DOWN,
    ('|', UP): UP,
    ('-', RIGHT): RIGHT,
    ('-', LEFT): LEFT,
    ('L', LEFT): UP,
    ('L', DOWN): RIGHT,
    ('J', RIGHT): UP,
    ('J', DOWN): LEFT,
    ('7', RIGHT): DOWN,
    ('7', UP): LEFT,
    ('F', LEFT): DOWN,
    ('F', UP): RIGHT
}

# In example.txt S is 'F', if moving
# "clockwise" previous move was UP.
# Enter this manually. In my input S is
# '|' and prev is UP (DOWN also works).
#cur = 'F'
cur = '|'
dir = UP
posses = [start_pos]

# Toto, I have a feeling we're not in Kansas anymore

pos = start_pos

while True:
    dir = moves[(cur, dir)]
    pos = new_pos(pos, dir)
    if pos == start_pos:
        break
    cur = get_pipe(pos)
    posses.append(pos)

print('Part 1:', len(posses) // 2)
