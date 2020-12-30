#!/usr/bin/env python3

# TODO: restore this. I happened to delete the file...
# right now it's not working

import numpy as np
import sys
from collections import deque
# Use intmachine from ../common
sys.path.insert(0,'../common')
from intmachine import Intmachine

# Read program from input.txt
prog = []
with open('input.txt') as f:
    line = f.readline().rstrip()
for i in map(int, line.split(',')):
    prog.append(i)

# 0 for input, 1 for output
queues = []
for _ in range(2):
    dq = deque()
    queues.append(dq)

# Create and connect machine
m = Intmachine('d15', prog, queues[0], queues[1])

# Guess dimensions, init with 3 (not visited)
width = 41
heigth = 41
board = np.array([3] * width * heigth, dtype = np.int16)
# Place droid in middle of board
startpos = np.array([21, 21], dtype = np.int16)
droid = startpos.copy()
lastmove = 1
# oxygen tank position
oxygen = np.array([0, 0], dtype = np.int16)

# Use ytab for faster index-into-board calculation
ytab = np.array([0] * heigth, dtype = np.int16)
for y in range(heigth):
    ytab[y] = y * width

def put_tile(x, y, tile):
    board[ytab[y] + x] = tile

def get_tile(x, y):
    return board[ytab[y] + x]

# Wall, visited, oxygen tank, not visited
tiles = ['#', '.', 'O', ' ']
def render_board(show_droid = True):
    # move to 0,0
    print('\033[0;0H')
    for y in range(heigth):
        for x in range(width):
            tile = get_tile(x, y)
            if not show_droid:
                sys.stdout.write(tiles[tile])
            else:
                if x == droid[0] and y == droid[1]:
                    sys.stdout.write('D')
                elif x == startpos[0] and y == startpos[1]:
                    sys.stdout.write('S')
                else:
                    sys.stdout.write(tiles[tile])
        print('')

# up, down, left, right
moves = [ np.array([ 0,-1], dtype = np.int16),
        np.array([ 0, 1], dtype = np.int16),
        np.array([-1, 0], dtype = np.int16),
        np.array([ 1, 0], dtype = np.int16) ]
# index is move - 1
def get_move(move):
    return moves[move - 1]

# lefthand[move] = left hand when moving in move dir
lefthand = [3, 4, 2, 1]
righthand = [4, 3, 1, 2]
backmove = [2, 1, 4, 3]

def do_game(move, status):
    global droid, oxygen, lastmove
    # Numpy only used to make operation + work in line below
    trypos = droid + get_move(move)
    tx = trypos[0]
    ty = trypos[1]
    if status == 0:
        # hit a wall, droid pos unchanged
        put_tile(tx, ty, status)
    elif status == 1:
        # Move successful
        put_tile(tx, ty, status)
        droid = trypos.copy()
        lastmove = move
    elif status == 2:
        # Moved. Oxygen is now in next position.
        droid = trypos.copy()
        oxygen = droid + get_move(move)
        put_tile(tx, ty, 1)
        put_tile(oxygen[0], oxygen[1], 2)
        lastmove = move
    else:
        print('Error: got status %d, expected 0-2' % (status))
        exit(0)

# read input from keyboard
# these are for dvorak, change to
# 'w', 's', 'a', 'd' for qwerty
keys = ('.', 'e', 'o', 'u', 'q')
def get_keyboard_input():
    c = False
    # repeat until valid key pressed
    while not c in keys:
        c = input('')
        if c in keys:
            if c == 'q':
                # quit
                exit(0)
            move = keys.index(c) + 1
    return move

def get_tile_move(move):
    change = get_move(move)
    x, y = droid + change
    tile = get_tile(x, y)
    return tile

def can_move(move):
    tile = get_tile_move(move)
    if tile == 0 or tile == 2:
        return False
    return True

# Follow wall on left or right hand side
def some_hand_path(hand1, hand2):
    # check if wall on left side
    leftmove = hand1[lastmove - 1]
    if not can_move(leftmove):
        # wall on left, check if wall straight
        if not can_move(lastmove):
            rightmove = hand2[lastmove - 1]
            # Right hand move, check if wall right
            if not can_move(rightmove):
                # Wall right, move back
                return backmove[lastmove - 1]
            # Move right
            return rightmove
        # Straight
        return lastmove
    # Left hand
    return leftmove

def left_hand_path():
    return some_hand_path(lefthand, righthand)

def right_hand_path():
    return some_hand_path(righthand, lefthand)

def move_droid(move):
    global m
    while len(m.oq) < 1:
        if m.would_stall():
            m.push(move)
        m.do_op()
    # Got status code
    status = m.pop()
    do_game(move, status)
    return status

def index_to_xy(i):
    x = i % width
    y = i // width
    return np.array([x, y], dtype = np.int16)

def fill_board():
    global board, m, droid, lastmove, oxygen
    m.reset()
    board = np.array([3] * width * heigth, dtype = np.int16)
    # Set walls to 0
    for x in range(width):
        put_tile(x, 0, 0)
        put_tile(x, heigth - 1, 0)
    for y in range(heigth):
        put_tile(0, y, 0)
        put_tile(width - 1, y, 0)
    # 0, 0 is guaranteed to be wall, init oxygen to wall pos
    oxygen = np.array([0, 0], dtype = np.int16)
    droid = startpos.copy()
    put_tile(droid[0], droid[1], 1)
    # Found manually that first move is north.
    # Set lastmove to 1 to think we already started north.
    lastmove = 1

    # clear screen once
    print('\033[2J\033[1;1H')

    frame = 0
    while True:
        # Do some left moves until
        # board is filled.
        move = left_hand_path()
        move_droid(move)
        frame += 1
        if frame > 3000:
            render_board(True)
            # There might be a few unreachable spots.
            # It doesn't matter. Oxygen will not reach them.
            print('Empty spots:', list(map(index_to_xy, np.where(board == 3)[0])))
            input('')
            return True
    # Should not get here
    return False

def fill_neigbours(pos, b):
    global frame
    for move in [1, 2, 3, 4]:
        change = get_move(move)
        checkpos = pos + change
        x = checkpos[0]
        y = checkpos[1]
        tile = b[ytab[y] + x]
        if tile == 1:
            put_tile(x, y, 2)
            if x == startpos[0] and y == startpos[1]:
                print('shortest path:', frame + 1)

def fill_oxygen():
    global board
    boardcopy = board.copy()
    # Loop through all oxygen tiles
    for i in np.where(boardcopy == 2)[0]:
        pos = index_to_xy(i)
        # mark neighbouring tiles as oxygenated
        fill_neigbours(pos, boardcopy)

fill_board()
print('\033[2J\033[1;1H')
frame = 0
while len(np.where(board == 1)[0]) > 0:
    fill_oxygen()
    frame += 1
    render_board(False)
    print(frame)
    input('')
print(frame)
