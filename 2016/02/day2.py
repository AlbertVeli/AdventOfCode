#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc

lines = aoc.lines(sys.argv[1])

numpad_1 = [
    ('0','0','0','0','0'),
    ('0','1','2','3','0'),
    ('0','4','5','6','0'),
    ('0','7','8','9','0'),
    ('0','0','0','0','0')
]
numpad_2 = [
    ('0','0','0','0','0','0','0'),
    ('0','0','0','1','0','0','0'),
    ('0','0','2','3','4','0','0'),
    ('0','5','6','7','8','9','0'),
    ('0','0','A','B','C','0','0'),
    ('0','0','0','D','0','0','0'),
    ('0','0','0','0','0','0','0')
]

pos_1 = (2, 2)
pos_2 = (3, 1)

def get_pos(p):
    return numpad[p[0]][p[1]]

def move(direction):
    global pos
    row, col = pos
    dy, dx = direction
    newpos = (row + dy, col + dx)
    if get_pos(newpos) != '0':
        pos = newpos

def move_up():
    move((-1, 0))

def move_down():
    move((1, 0))

def move_left():
    move((0, -1))

def move_right():
    move((0, 1))

moves = {
    'U': move_up,
    'D': move_down,
    'L': move_left,
    'R': move_right
}

# part 1
numpad = numpad_1
pos = pos_1
sys.stdout.write('part 1: ')
for line in lines:
    for direction in line.rstrip():
        moves[direction]()
    sys.stdout.write(str(numpad[pos[0]][pos[1]]))
sys.stdout.write('\n')

# part 2
numpad = numpad_2
pos = pos_2
sys.stdout.write('part 2: ')
for line in lines:
    for direction in line.rstrip():
        moves[direction]()
    sys.stdout.write(str(numpad[pos[0]][pos[1]]))
sys.stdout.write('\n')