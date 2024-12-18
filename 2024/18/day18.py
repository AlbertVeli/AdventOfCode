#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc
from collections import deque

def visualize(grid, path):
    marked_grid = [row.copy() for row in grid]
    for x, y in path:
        marked_grid[y][x] = 'O'
    for row in marked_grid:
        print(''.join(row))

def bfs(grid, start, end):
    queue = deque([start])
    visited = set([start])
    path = {start: None}

    while queue:
        pos = queue.popleft()
        if pos == end:
            p = []
            while pos:
                p.append(pos)
                pos = path[pos]
            return p[::-1]

        x, y = pos
        moves = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

        for move in moves:
            x, y = move
            if 0 <= x < len(grid[0]) and 0 <= y < len(grid) and move not in visited:
                if grid[y][x] == '.':
                    queue.append(move)
                    visited.add(move)
                    path[move] = pos

    # no path from start to end
    return None

data = aoc.lines_of_ints(sys.argv[1])

# 7, 7, 12 for the example input
# 71, 71, 1024 for the puzzle input
#rows, cols, fallen = 7, 7, 12
rows, cols, fallen = 71, 71, 1024
start = (0, 0)
end = (rows - 1, cols - 1)
pos = start
grid = [['.' for _ in range(cols)] for _ in range(rows)]

# Start by marking fallen memory cells corrupted
for x, y in data[:fallen]:
    grid[y][x] = '#'

# Part 1
path = bfs(grid, start, end)
print('Part 1:', len(path) - 1 if path else "No path found")

# Part 2
# Continue corrupting the grid one coordinate at a time
for i in range(fallen, len(data)):
    x, y = data[i]
    grid[y][x] = '#'

    # Check if there is still a path from start to end
    path = bfs(grid, start, end)

    if path is None:
        print(f'Part 2: {x},{y}')
        break
