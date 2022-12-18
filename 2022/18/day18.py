#!/usr/bin/env python3

import sys
import numpy as np

# Add 1 to make sure no coordinate is leaning against the edge of the universe
cubes = [(x + 1, y + 1, z + 1) for x, y, z in list(map(lambda x: tuple(map(int, x.split(','))), open(sys.argv[1]).read().rstrip().split('\n')))]

# The grid universe is represented as a cube here and
# the edge length needs to be at least 9 for the example and 24 for my input
# to find max value, use for instance the line below (add 3 to the max value):
#   cat input.txt | tr ',' '\n' | sort -nu
#
# shellmagheddon:
#   echo $(($(cat input.txt | tr ',' '\n' | sort -nu | tail -1) + 3))
universe_edge = 24
grid = np.zeros((universe_edge, universe_edge, universe_edge), dtype = int)
for x, y, z in cubes:
    # slices, rows, columns
    grid[z, y, x] = 1

def neighbors(xyz):
    x, y, z = xyz
    # probably confusing to store tuples as x, y, z sometimes and z, y, x sometimes
    return [(z, y - 1, x), (z, y + 1, x), (z - 1, y, x), (z + 1, y, x), (z, y, x - 1), (z, y, x + 1)]

# Number of neighbors with val val
def num_neighbors(xyz, val):
    num = 0
    for zyx in neighbors(xyz):
        if grid[zyx] == val:
            num += 1
    return num

neighs = []
for cube in cubes:
    # sides = 6 - number of cube neighbors (value 1 in grid)
    neighs.append(6 - num_neighbors(cube, 1))

part1 = sum(neighs)
print('Part 1:', part1)

def flood_fill(val):
    stack = [(0, 0, 0)]
    while len(stack) > 0:
        x, y, z = stack.pop()
        grid[z, y, x] = val
        # push neighbors on to stack if 0
        for zn, yn, xn in neighbors((x, y, z)):
            if zn >= 0 and zn < universe_edge and yn >= 0 and yn < universe_edge and xn >= 0 and xn < universe_edge:
                # Only fill coords that have not been visited
                # and are not occupied by a cube
                if grid[zn, yn, xn] == 0:
                    stack.append((xn, yn, zn))

# Part 2, flood fill grid with values 2 starting at (0, 0, 0)
flood_fill(2)

neighs = []
for cube in cubes:
    # remove sides of cubes that are neighbors to a zero
    # they must be inside a bubble
    neighs.append(num_neighbors(cube, 0))

part2 = part1 - sum(neighs)
print('Part 2:', part2)
