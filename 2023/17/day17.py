#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc
# Could use either heapq or PriorityQueue here
from heapq import heappop, heappush

grid = aoc.char_matrix(sys.argv[1])
height = len(grid)
width = len(grid[0])
# right, down, left, up
dirs = ((1, 0), (0, 1), (-1, 0), (0, -1))

def add_pos_dir(pos, dir):
    return tuple(map(sum, zip(pos, dir)))

# min_steps = minimum steps before turn
# max_steps = maximum steps before turn
def find_path(min_steps, max_steps):
    start = (0, 0)
    end = (height - 1, width - 1)

    # (pos, dir, steps)
    visited = set()
    # (dist, pos, prev_dir, steps_in_dir)
    # Start with prev_dir = right
    q = [(0, start, None, 0)]
    while q:
        dist, pos, prev_dir, steps = heappop(q)
        if pos == end:
            return dist

        allowed_dirs = []

        if prev_dir == None:
            # Special case, first step, no prev_dir, try right and down
            allowed_dirs.append(0)
            allowed_dirs.append(1)
        else:
            # Normal case
            if steps < max_steps:
                allowed_dirs.append(prev_dir)
            if steps >= min_steps:
                allowed_dirs.append((prev_dir + 1) % 4)
                allowed_dirs.append((prev_dir - 1) % 4)

        for dir in allowed_dirs:
            x, y = add_pos_dir(pos, dirs[dir])
            if x < 0 or x >= width or y < 0 or y >= height:
                continue

            weight = int(grid[y][x])
            neighbour = (x, y)
            new_dist = dist + weight

            if dir != prev_dir:
                new_steps = 1
            else:
                new_steps = steps + 1

            if (neighbour, dir, new_steps) in visited:
                continue
            visited.add((neighbour, dir, new_steps))
        
            heappush(q, (new_dist, neighbour, dir, new_steps))

# Strangely, this doesn't work for example2.txt
# but it works for example1.txt and my input.
print('Part 1:', find_path(0, 3))
print('Part 2:', find_path(4, 10))