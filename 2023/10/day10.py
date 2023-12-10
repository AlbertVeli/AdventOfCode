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

def dump_matrix(morpheus):
    """ the matrix is a system, neo """
    for line in morpheus:
        print(''.join(line).replace('.', ' '))

# reach for the red pill
for y, line in enumerate(mtrx):
    if 'S' in line:
        x = line.index('S')
        break

# - he told me you killed him
# - no, I am your father

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

# In example1.txt S is 'F', if moving
# "clockwise" previous move was UP.
# Enter this manually. In my input S is
# '|' and prev is UP (DOWN also works).
# In example2.txt S is also 'F'.

start_pos = (x, y)

# You should probably change the 2 lines below
start_pipe = '|'
start_dir = DOWN

cur = start_pipe
dir = start_dir
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


# Part 2

# First replace S with the appropriate pipe
mtrx[start_pos[1]][start_pos[0]] = start_pipe
#dump_matrix(mtrx)
insiders = []

# Neo, sooner or later you're going to realize that there's
# a difference between knowing the path and walking the path
for y in range(len(mtrx)):
    for x in range(len(mtrx[0])):
        if not (x, y) in posses:
            mtrx[y][x] = '.'

# After cleaning up the matrix, use this algorithm
# https://gamedev.stackexchange.com/questions/141460/how-can-i-fill-the-interior-of-a-closed-loop-on-a-tile-map

# Corruption spreads like a virus within the Matrix
for y, line in enumerate(mtrx):
    in_simulated_reality = False
    for x, c in enumerate(line):
        # - flip simulated reality at |, J and L
        if c == '|' or c == 'J' or c == 'L':
            in_simulated_reality = not in_simulated_reality
        elif c == '.' and in_simulated_reality:
            mtrx[y][x] = 'I'
            insiders.append((x, y))

dump_matrix(mtrx)

print('Part 2:', len(insiders))