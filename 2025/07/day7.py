#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc

grid = aoc.char_matrix(sys.argv[1])
h = len(grid)
w = len(grid[0])

def visualize():
    for y in range(h):
        for x in range(w):
            sys.stdout.write(grid[y][x])
        sys.stdout.write('\n')
    sys.stdout.write('\n')

def find_start(grid):
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == 'S':
                return x, y
    raise ValueError("No S in grid")


def count_splits(grid):
    h = len(grid)
    w = len(grid[0])

    sx, sy = find_start(grid)

    # First beam starts just below S
    active = {(sx, sy + 1)}
    splits = 0

    while active:
        next_active = set()

        for x, y in active:
            # Out of bounds => beam disappears
            if not (0 <= x < w and 0 <= y < h):
                continue

            cell = grid[y][x]

            if cell == '^':
                splits += 1
                ny = y + 1
                if ny < h:
                    if x - 1 >= 0:
                        next_active.add((x - 1, ny))
                    if x + 1 < w:
                        next_active.add((x + 1, ny))

            else:
                # Empty (or S, but that only happens at the start) -> go down
                ny = y + 1
                if ny < h:
                    next_active.add((x, ny))

        # Beams that land on the same cell are merged by the set
        active = next_active

    return splits

def count_timelines(grid):

    sx, sy = find_start(grid)

    # ways[y][x] = number of timelines reaching (x, y)
    ways = [[0] * w for _ in range(h)]
    ways[sy][sx] = 1

    for y in range(sy, h):
        for x in range(w):
            k = ways[y][x]
            if k == 0:
                continue

            cell = grid[y][x]

            if cell == '^':
                ny = y + 1
                if ny < h:
                    if x - 1 >= 0:
                        ways[ny][x - 1] += k
                    if x + 1 < w:
                        ways[ny][x + 1] += k
            else:  # '.' or 'S'
                ny = y + 1
                if ny < h:
                    ways[ny][x] += k

    # timelines on the last row will fall out below the grid
    return sum(ways[h - 1])

sx, sy = find_start(grid)
#visualize()
print('Part 1:', count_splits(grid))
print('Part 2:', count_timelines(grid))
