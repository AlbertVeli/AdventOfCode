#!/usr/bin/env python3

# Remove dead ends in map. Use output from this
# as input to solve.py for about 2x speedup.
#
# Ie: ./nodead.py input.txt > nodead.txt
#     ./solve.py nodead.txt

import numpy as np
import sys
import string

lower = string.ascii_lowercase
upper = string.ascii_uppercase

# Return list of (y, x) positions for tiles with value tile
def get_yx_list(tile):
    res = np.where(board == tile)
    return list(zip(res[0], res[1]))

# Calc inverse dict
def inv(d):
    dd = {}
    for k, v in d.items():
        dd[v] = k
    return dd

# pos = (y, x) tuple
def get_tile_at(pos, keys, doors):
    if pos == player:
        return '@'
    invkeydoor = inv({**keys, **doors})
    if pos in invkeydoor:
        return invkeydoor[pos]
    return board[pos]

# Without player, keys or doors
def dump_raw_board():
    np.savetxt(sys.stdout.buffer, board, fmt='%c', delimiter = '')

# With players, keys and doors
def dump_board(f, keys, doors):
    print(lines[0])
    for y in range(1, heigth - 1):
        row = board[y]
        f.write('#')
        for x in range(1, width - 1):
            pos = (y, x)
            tile = get_tile_at(pos, keys, doors)
            f.write(tile)
        print('#')
    print(lines[0])

# Read input into numpy 2d array (board)
with open(sys.argv[1]) as f:
    lines = f.read().rstrip().split('\n')
width = len(lines[0])
heigth = len(lines)
board = np.array([list(line) for line in lines])

# Save player pos and put . on board
player = get_yx_list('@')[0]
board[player] = '.'

# Initial keys and doors
ikeys = {}
idoors = {}
# Save keys and doors, replace with .
for y in range(1, heigth - 1):
    row = board[y]
    for x in range(1, width - 1):
        c = row[x]
        if c in lower:
            ikeys[c] = (y, x)
            board[ikeys[c]] = '.'
        elif c in upper:
            idoors[c] = (y, x)
            board[idoors[c]] = '.'


# y, x notation for easier access into board from pos
moves = { 'up'  : np.array([-1, 0], dtype = np.int),
        'down'  : np.array([ 1, 0], dtype = np.int),
        'left'  : np.array([ 0,-1], dtype = np.int),
        'right' : np.array([ 0, 1], dtype = np.int) }

turnright = { 'up' : 'right', 'right' : 'down', 'down' : 'left', 'left' : 'up' }
turnleft = { 'up' : 'left', 'left' : 'down', 'down' : 'right', 'right' : 'up' }

dirs = [ 'up', 'down', 'left', 'right' ]

# Get position one step in movedir
def get_move_pos(pos, movedir):
    change = moves[movedir]
    return tuple(np.array(pos, dtype = np.int) + change)

# Return tile value one step from pos in movedir
def get_tile_move(pos, movedir, doors):
    newpos = get_move_pos(pos, movedir)
    return get_tile_at(newpos, ikeys, doors)

def get_neighbours(pos, doors):
    neighbours = []
    for movedir in dirs:
        tile = get_tile_move(pos, movedir, doors)
        neighbours.append(tile)
    return neighbours

# Optimize by filling dead ends with
# wall tiles before walkmagheddon
def no_dead_ends():
    # 1 remove dead ends
    changed = 1
    while changed > 0:
        changed = 0
        # Dead end is . with 3 # around it
        for dead in get_yx_list('.'):
            pos = tuple(dead)
            neighs = get_neighbours(pos, idoors)
            if neighs.count('#') == 3:
                # Dead end
                board[dead] = '#'
                changed += 1
    # 2 remove doors at dead ends (3 # around it)
    doors = dict(idoors)
    for door, deadpos in idoors.items():
        pos = tuple(deadpos)
        neighs = get_neighbours(pos, doors)
        if neighs.count('#') == 3:
            # Dead end
            board[deadpos] = '#'
            del(doors[door])
    # 3 remove dead ends again
    changed = 1
    while changed > 0:
        changed = 0
        # Dead end is . with 3 # around it
        for dead in get_yx_list('.'):
            pos = tuple(dead)
            neighs = get_neighbours(pos, doors)
            if neighs.count('#') == 3:
                # Dead end
                board[dead] = '#'
                changed += 1

no_dead_ends()
dump_board(sys.stdout, ikeys, idoors)
