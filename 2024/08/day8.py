#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc
from collections import defaultdict
from itertools import combinations

def calc_antinodes(coord1, coord2):
    """
    Calculate the two antinode coordinates given two antenna coordinates.
    """
    x1, y1 = coord1
    x2, y2 = coord2

    # Difference vector
    dx, dy = x2 - x1, y2 - y1

    # Calculate antinodes
    antinode_1 = (x1 - dx, y1 - dy)
    antinode_2 = (x2 + dx, y2 + dy)

    return (antinode_1, antinode_2)


def within_grid(coord):
    """
    Check if the coordinate (y, x) is within the grid bounds.
    """
    y, x = coord
    return 0 <= y < rows and 0 <= x < cols

def calc_all_antinodes(coord1, coord2):
    """
    Calculate all integer grid points on the line between two coordinates.
    """
    y1, x1 = coord1
    y2, x2 = coord2
    dy = y2 - y1
    dx = x2 - x1

    antinodes = []

    # Add points in one direction
    y, x = y1, x1
    while within_grid((y, x)):
        antinodes.append((y, x))
        y -= dy
        x -= dx

    # Add points in the other direction
    y, x = y2, x2
    while within_grid((y, x)):
        antinodes.append((y, x))
        y += dy
        x += dx

    return antinodes

# Main

# Parse input into a dictionary of antennas
a = aoc.char_matrix(sys.argv[1])
rows, cols = len(a), len(a[0])
antennas = defaultdict(list)
for y in range(rows):
    for x in range(cols):
        c = a[y][x]
        if c != '.':
            # Store in radcol format (row, column)
            antennas[c].append((y, x))

# Part 1
antinode_locations = set()

for antenna, coords in antennas.items():
    #print(antenna, coords)
    pairs = list(combinations(coords, 2))
    for pair in pairs:
        a1, a2 = calc_antinodes(*pair)
        # Add if within grid. We don't need to check if the
        # antinode is already added since we are using a set.
        if within_grid(a1):
            antinode_locations.add(a1)
        if within_grid(a2):
            antinode_locations.add(a2)

print('Part 1:', len(antinode_locations))

# Part 2
antinode_locations = set()

for antenna, coords in antennas.items():
    pairs = list(combinations(coords, 2))
    for pair in pairs:
        for a in calc_all_antinodes(*pair):
            # calc_all_antinodes already checks if
            # the antinode is within the grid
            antinode_locations.add(a)

print('Part 2:', len(antinode_locations))
