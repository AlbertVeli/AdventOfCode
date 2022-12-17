#!/usr/bin/env python3

import sys

# globals
grid = set()
grid_w = 7
jets = [1 if x=='>' else -1 for x in list(open(sys.argv[1]).read().rstrip())]
jetlen = len(jets)
pruned_rows = 0
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

def prune_grid():
    global pruned_rows, grid

    rows_to_prune = []
    prune_y = 0

    cols = [[] for _ in range(grid_w)]
    for x, y in grid:
        cols[x].append(y)

    # find lowest row a tile can reach
    prune_y = max([min(col) if len(col) > 0 else 0 for col in cols])
    if prune_y < 0:
        new_grid = set()
        for x, y in grid:
            if y < prune_y:
                # move down prune_y rows (prune_y is negative)
                new_grid.add((x, y - prune_y))
        grid = new_grid
        # pruned_rows is positive
        pruned_rows += abs(prune_y)

def visualize_grid():
    for y in range(-35, 0):
        row = ''
        for x in range(grid_w):
            if (x, y) in grid:
                row += '#'
            else:
                row += '.'
        print(row)

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

ints = []
nints = 0

def find_cycle():
    '''
    search for cycle using the following strategy:
     - at some point the list ints starts repeating
     - at twice that point the first half and second
       half of ints are equal
     - by definition nints must be even when this happens
    '''
    cycle = False
    if nints >= 2 * jetlen and (nints & 1) == 0:
        half = nints >> 1
        for i in range(half):
            if ints[i] != ints[half + i]:
                return False
        # If we get here the cycle begins repeating at index half
        cycle = half
        print(cycle)
    return cycle

# detect pattern of length m, repeated k or more times
# (thanks google)
def find_pattern(arr, m, k):
    L = len(arr)
    cnt = 0
    threshold = m * (k - 1)
    for i in range(L - m):
        if arr[i] == arr[i + m]:
            if cnt == 0:
                start_i = i
            cnt += 1
        else:
            cnt = 0
            start_i = -1
        if cnt == threshold:
            # Repeats at least k times
            print(f'repeating pattern of length {m} starts at index {start_i}')
            return start_i
    return False 

# increase this if 'repeating pattern...' is not printed
for _ in range(40000):
    old_top = grid_top()
    t = Tile(n_tiles % shapeslen)
    t.move_to_rest()
    new_top = grid_top()
    added_h = old_top - new_top
    #print(nints, added_h)
    ints.append(added_h)
    nints += 1
    prune_grid()
    #visualize_grid()
    #input()
    n_tiles += 1

# Search for offset where pattern starts
# and length of pattern
for len_p in range(1000, 30 * jetlen):
    i = find_pattern(ints, len_p, 5)
    if i:
        len_pattern = len_p
        len_prefix = i
        break
#repeating pattern of length 1735 starts at index 530
#repeating pattern of length 3470 starts at index 530
# ...
#repeating pattern of length 10410 starts at index 530
#repeating pattern of length 12145 starts at index 530
#repeating pattern of length 13880 starts at index 530
#repeating pattern of length 15615 starts at index 530
#repeating pattern of length 17350 starts at index 530
#repeating pattern of length 19085 starts at index 530
#repeating pattern of length 20820 starts at index 530
#repeating pattern of length 22555 starts at index 530
#repeating pattern of length 24290 starts at index 530
#repeating pattern of length 26025 starts at index 530
#repeating pattern of length 27760 starts at index 530
#repeating pattern of length 29495 starts at index 530
#repeating pattern of length 31230 starts at index 530
#repeating pattern of length 32965 starts at index 530
#repeating pattern of length 34700 starts at index 530
#repeating pattern of length 36435 starts at index 530
#repeating pattern of length 38170 starts at index 530

# TODO: This gives the correct answer for the given example
#       but not for the actual input. The answer in slightly
#       off. The cycle must depend on something more so the
#       correct cycle must be longer than the numbers above.

prefix = ints[:len_prefix]
pattern = ints[len_prefix : len_prefix + len_pattern]

sum_prefix = sum(prefix)
sum_pattern = sum(pattern)
loops = 1000000000000
num_complete_patterns = (loops - len_prefix) // len_pattern
# Number of elements into last pattern
num_last = (loops - len_prefix) % len_pattern
answer = sum_prefix + num_complete_patterns * sum_pattern + sum(pattern[:num_last])
print(answer)
