#!/usr/bin/env python3

import sys
from collections import deque
sys.path.append('../..')
import aoc

def flood_fill(m, pos, visited, c):
    """
    return all positions in the coherent
    region of the same plant type
    """
    positions = []
    queue = [pos]

    while queue:
        cur_pos = queue.pop(0)
        if cur_pos in visited:
            continue

        if m[cur_pos] == c:
            visited.add(cur_pos)
            positions.append(cur_pos)
            x, y = cur_pos
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if nx < 0 or nx >= rows or ny < 0 or ny >= cols:
                    continue
                queue.append((nx, ny))

    return positions

def calculate_area_and_sides(region):
    """Calculates the area and number of sides for a region."""
    area = len(region)
    sides = calculate_sides(region)
    return area, sides

def calculate_sides(region):
    """
    Calculates the number of sides (=corners) for a region.
    This algorithm is based on my son's solution.
    """
    corners = 0

    for (x, y) in region:
        for dir_index in range(len(directions)):
            dx, dy = directions[dir_index]
            dx2, dy2 = directions[(dir_index + 1) % 4]
            x2, y2 = x + dx, y + dy
            x3, y3 = x + dx2, y + dy2
            x4, y4 = x + dx + dx2, y + dy + dy2

            if (x2, y2) not in region and (x3, y3) not in region:
                corners += 1
            elif (x2, y2) in region and (x3, y3) in region and (x4, y4) not in region:
                corners += 1

    return corners

def calculate_fencing_cost():
    visited = set()
    total_cost = 0

    for x in range(rows):
        for y in range(cols):
            pos = (x, y)
            if pos not in visited:
                c = grid[pos]
                region = flood_fill(grid, pos, visited, c)
                area, sides = calculate_area_and_sides(region)
                print(f"Plant type: {c}, Area: {area}, Sides: {sides}")
                total_cost += area * sides

    return total_cost

def build_grid(lines):
    m = {}
    for x, line in enumerate(lines):
        for y, char in enumerate(line):
            m[(x, y)] = char
    return m

# --- Main ---

# global variables
lines = aoc.lines(sys.argv[1])
rows, cols = len(lines), len(lines[0])
grid = build_grid(lines)
directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]

print('Part 2:', calculate_fencing_cost())
