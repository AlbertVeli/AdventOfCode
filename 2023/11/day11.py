#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc
from itertools import combinations

space_mtrx = aoc.char_matrix(sys.argv[1])

width = len(space_mtrx[0])
heigth = len(space_mtrx)

# expand rows
x_rows = []
for i, row in enumerate(space_mtrx):
    if all (c == '.' for c in row):
        x_rows.append(i)

x_cols = []
for i in range(width):
    col = [row[i] for row in space_mtrx]
    if all (c == '.' for c in col):
        x_cols.append(i)

galaxies = []
for y, row in enumerate(space_mtrx):
    for x, c in enumerate(row):
        if c == '#':
            galaxies.append((x, y))

def get_dist(g1, g2, mul):
    """
    Return manhattan distance between g1 and g2
    Expanded rows and columns are in x_rows, x_cols
    Multiply each crossed x_row/x_col by mul
    """
    x1, x2 = sorted([g1[0], g2[0]])
    y1, y2 = sorted([g1[1], g2[1]])
    # Range does neither include x1 nor x2
    # only empty cows/cols can be expanded
    xs = range(x1 + 1, x2)
    ys = range(y1 + 1, y2)
    num_xs = sum(x in x_cols for x in xs)
    num_ys = sum(y in x_rows for y in ys)
    # Crossed rows/cols are already counted once
    # multiply by mul - 1
    return (x2 - x1) + (y2 - y1) + (num_xs + num_ys) * (mul - 1)

combs = list(combinations(galaxies, 2))
lens = []
for g1, g2 in combs:
    # Part 1, count crossed rows/cols 2 times
    lens.append(get_dist(g1, g2, 2))
print('Part 1:', sum(lens))

lens = []
for g1, g2 in combs:
    # Part 2, a million times
    lens.append(get_dist(g1, g2, 1000000))
print('Part 2:', sum(lens))