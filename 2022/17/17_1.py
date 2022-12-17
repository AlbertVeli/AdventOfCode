#!/usr/bin/env python3

import sys

# globals
grid = set()
grid_w = 7
jets = [1 if x=='>' else -1 for x in list(open(sys.argv[1]).read().rstrip())]
jetlen = len(jets)
moves = 0

# coordinates relative upper left
shapes = [
        # ####
        [(0, 0), (1, 0), (2, 0), (3, 0)],
        # .#.
        # ###
        # .#.
        [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
        # ..#
        # ..#
        # ###
        [(2, 0), (2, 1), (0, 2), (1, 2), (2, 2)],
        # #
        # #
        # #
        # #
        [(0, 0), (0, 1), (0, 2), (0, 3)],
        # ##
        # ##
        [(0, 0), (1, 0), (0, 1), (1, 1)]
        ]

n_tiles = 0
shapeslen = len(shapes)

# functions

def get_jet():
    return jets[moves % jetlen]

def grid_top():
    if len(grid) == 0:
        return 0
    return min([y for x, y in grid])


class Tile:
    def __init__(self, shapeno):
        self.shape = shapes[shapeno].copy()
        self.h = self.get_height()
        self.x = 2
        self.y = grid_top() - 3 - self.h
        self.moving = True

    def place_at(self, x, y):
        self.x = x
        self.y = y

    def get_height(self):
        y_values = [y for _, y in self.shape]
        height = max(y_values) - min(y_values) + 1
        return height

    def try_move(self, ox):
        ''' Try to move tile offset ox sideways and one down '''
        new_coords = [(self.x + sx + ox, self.y + sy) for sx, sy in self.shape]
        for x, y in new_coords:
            # wall or hit other tile sideways
            if x < 0 or x >= grid_w or (x, y) in grid:
                # don't move sideways
                ox = 0
                break

        self.x += ox

        # Try to move down
        oy = 1
        new_coords = [(self.x + sx, self.y + sy + oy) for sx, sy in self.shape]
        for x, y in new_coords:
            # floor or hit other tile
            # floor is at y = 0
            if y >= 0 or (x, y) in grid:
                self.moving = False
                oy = 0
                break

        self.y += oy

        if not self.moving:
            # tile is at rest, insert
            # coordinates into grid
            new_coords = [(self.x + sx, self.y + sy) for sx, sy in self.shape]
            for x, y in new_coords:
                grid.add((x, y))

    def move_to_rest(self):
        global moves
        while self.moving:
            jet = get_jet()
            self.try_move(jet)
            moves += 1
            #print(self)

    def __str__(self):
        return f'({self.x}, {self.y}), {self.moving}'

# main

for _ in range(2022):
    t = Tile(n_tiles % shapeslen)
    t.move_to_rest()
    n_tiles += 1

print('Part 1:', abs(grid_top()))
