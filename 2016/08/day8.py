#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc

if sys.argv[1] == 'example.txt':
    width = 7
    height = 3
else:
    width = 50
    height = 6

screen = [['.' for _ in range(width)] for _ in range(height)]

def dump_screen():
    for row in screen:
        print(''.join(row))

def rect(w, h):
    for y in range(h):
        for x in range(w):
            screen[y][x] = '#'

def rot_row(y, n):
    for _ in range(n):
        last = screen[y][width - 1]
        for x in range(width - 1, 0, -1):
            screen[y][x] = screen[y][x - 1]
        screen[y][0] = last

def rot_col(x, n):
    for _ in range(n):
        last = screen[height - 1][x]
        for y in range(height - 1, 0, -1):
            screen[y][x] = screen[y - 1][x]
        screen[0][x] = last

def lit():
    n = 0
    for row in screen:
        n += row.count('#')
    return n

lines = aoc.lines(sys.argv[1])
for line in lines:
    a = aoc.ints(line)
    if line.startswith('rotate column'):
        #print(f'rot col {a[0]} by {a[1]}')
        rot_col(a[0], a[1])
        #dump_screen()
    elif line.startswith('rotate row'):
        #print(f'rot row {a[0]} by {a[1]}')
        rot_row(a[0], a[1])
        #dump_screen()
    elif line.startswith('rect'):
        #print(f'rect {a[0]} by {a[1]}')
        rect(a[0], a[1])
        #dump_screen()
    else:
        print('unknown', line)

print('Part 1:', lit())
print('Part 2:')
dump_screen()