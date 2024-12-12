#!/usr/bin/env python3

import sys
from collections import deque
sys.path.append('../..')
import aoc

def get_char(x, y, m):
    return m[y][x]

def put_char(c, val, m):
    x, y = c
    m[y][x] = val

def flood_fill(x, y, plant_type, visited):
    area = 0
    perimeter = 0

    queue = deque([(x, y)])
    put_char((x, y), True, visited)

    while queue:
        x, y = queue.popleft()
        area += 1

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            # Edge of grid or different plant type contributes to perimeter
            if nx < 0 or ny < 0 or nx >= cols or ny >= rows or get_char(nx, ny, grid) != plant_type:
                perimeter += 1
            elif not get_char(nx, ny, visited):
                put_char((nx, ny), True, visited)
                queue.append((nx, ny))

    return area, perimeter

def calculate_fencing_cost():
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    total_cost = 0

    for y in range(rows):
        for x in range(cols):
            if not get_char(x, y, visited):
                plant_type = get_char(x, y, grid)
                area, perimeter = flood_fill(x, y, plant_type, visited)
                total_cost += area * perimeter

    return total_cost

# --- Main ---

# global variables
grid = aoc.char_matrix(sys.argv[1])
rows, cols = len(grid), len(grid[0])
directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

print('Part 1:', calculate_fencing_cost())

