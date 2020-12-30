#!/usr/bin/env python3

import sys

# Direction letter -> direction dx, dy tuple
d2t = { 'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0) }
dirs = ['N', 'E', 'S', 'W']

class Ship:

    def __init__(self, direction, x = 0, y = 0, wx = 10, wy = -1):
        self.dir = direction
        self.x = x
        self.y = y
        self.wx = wx
        self.wy = wy

    def __str__(self):
        return 'pos, waypoint: (' + str(self.x) + ', ' + str(self.y) +')' + ', (' + str(self.wx) + ', ' + str(self.wy) +')'

    def rot_right(self, amount):
        times = (amount // 90) % 4
        for i in range(times):
            old_wx = self.wx
            self.wx = -self.wy
            self.wy = old_wx

    def rot_left(self, amount):
        self.rot_right(360 - amount)

    def move_forward(self, amount):
        self.x += self.wx * amount
        self.y += self.wy * amount

    def move_direction(self, direction, amount):
        dx, dy = d2t[direction]
        self.wx += dx * amount
        self.wy += dy * amount

    def do_instruction(self, t):
        instr, amount = t
        if instr in dirs:
            self.move_direction(instr, amount)
        elif instr == 'L':
            self.rot_left(amount)
        elif instr == 'R':
            self.rot_right(amount)
        elif instr == 'F':
            self.move_forward(amount)
        else:
            print('Unknown instruction:', instr)
            sys.exit(0)

def dir_amount(line):
    return (line[0], int(line[1:]))

def read_input(fname):
    return list(map(dir_amount, open(fname).read().splitlines()))

a = read_input(sys.argv[1])
ship = Ship('E')
print(ship)
for t in a:
    ship.do_instruction(t)
    print(ship)

print(abs(ship.x) + abs(ship.y))
