#!/usr/bin/env python3

# Part 1. I didn't have time to do part 2.
#
# Algorithm for part 1:
# Convert . to 0 and # to 1. Save all four
# edges and their reverses for each tile.
# That gives all combinations it can be
# connected to a neigbour. Orientation is
# not needed for Part 1. Convert bit strings
# to integers for faster edge comparison.

import sys
import re

tile_re = re.compile(r'Tile ([0-9]+):')
# Each tile is a tuple of (tile_id, [edges])
# where each edge is converted to an integer.
tiles = []

for line in open(sys.argv[1]).read().splitlines():
    if len(line) == 0:
        # Tile finished
        edges = []
        edges.append(int(tile_lines[0], 2))
        edges.append(int(tile_lines[0][::-1], 2))
        edges.append(int(tile_lines[9], 2))
        edges.append(int(tile_lines[9][::-1], 2))
        left = ''
        right = ''
        for i in range(10):
            left += tile_lines[i][0]
            right += tile_lines[i][9]
        edges.append(int(left, 2))
        edges.append(int(left[::-1], 2))
        edges.append(int(right, 2))
        edges.append(int(right[::-1], 2))
        tiles.append((tile_id, edges))
        continue
    num = tile_re.findall(line)
    if num:
        # New tile
        tile_id = num[0]
        tile_lines = []
    else:
        # Tile line
        tile_lines.append(line.replace('.', '0').replace('#', '1'))

# Do tile a and b share an edge?
# Any orientation.
def share_edge(a, b):
    for n in a:
        if n in b:
            return True
    return False

# Count shared edges for each tile
share = []
for i in range(len(tiles)):
    shared = 0
    for j in range(len(tiles)):
        if i != j and share_edge(tiles[i][1], tiles[j][1]):
            shared += 1
    share.append(shared)

# Corner tiles has exactly two shared edges
res = 1
for i in range(len(tiles)):
    if share[i] == 2:
        print(tiles[i][0])
        res *= int(tiles[i][0])
print(res)
