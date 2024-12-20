#!/usr/bin/env python3

import sys
import networkx as nx
from collections import defaultdict

# Global variables
G = nx.Graph()
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def build_graph(grid):
    rows, cols = len(grid), len(grid[0])
    for y in range(rows):
        for x in range(cols):
            if grid[y][x] != '.':
                continue
            for dx, dy in DIRECTIONS:
                nx, ny = x + dx, y + dy
                if 0 <= ny < rows and 0 <= nx < cols and grid[ny][nx] != '#':
                    G.add_edge((x, y), (nx, ny))

def get_start(grid, char):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == char:
                return (x, y)

def find_teleport_points(h, w, x, y, max_jump):
    """Find all points reachable within a given Manhattan distance."""
    points = set()
    for dx in range(-max_jump, max_jump + 1):
        for dy in range(-max_jump, max_jump + 1):
            if abs(dx) + abs(dy) <= max_jump:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h:
                    points.add((nx, ny))
    return points

def cheats_grouped(grid, start, end, max_jump, min_saving=0):
    """Generalized for both Part 1 and Part 2 """
    rows, cols = len(grid), len(grid[0])
    points = {(x, y) for y, row in enumerate(grid) for x, cell in enumerate(row) if cell != '#'}

    # Precompute shortest path distances
    distances_start = nx.single_source_shortest_path_length(G, source=start)
    distances_end = nx.single_source_shortest_path_length(G, source=end)
    baseline_length = distances_start[end]

    savings_dict = defaultdict(int)
    unique_cheats = set()

    for point in points:
        # Check all possible teleport destinations for the given point
        x, y = point
        teleports = find_teleport_points(rows, cols, x, y, max_jump)

        for point2 in teleports:
            if point2 not in points:
                continue
            x2, y2 = point2
            jump_length = abs(x - x2) + abs(y - y2)

            # Calculate the new distance using the teleport
            new_distance = distances_start[point] + jump_length + distances_end[point2]
            savings = baseline_length - new_distance

            # Only consider valid cheats
            if savings > 0 and savings >= min_saving:
                cheat = tuple(sorted([point, point2]))
                if cheat not in unique_cheats:
                    unique_cheats.add(cheat)
                    savings_dict[savings] += 1
                    #print(f"Valid cheat found: {point} -> {point2} with savings: {savings}")

    return savings_dict

# Main

grid = []
with open(sys.argv[1]) as f:
    for line in f:
        grid.append(list(line.strip()))

start = get_start(grid, 'S')
end = get_start(grid, 'E')

# Replace start and end points with walkable cells
grid[start[1]][start[0]] = '.'
grid[end[1]][end[0]] = '.'

build_graph(grid)

# Solve Part 1
savings = cheats_grouped(grid, start, end, max_jump=2, min_saving=100)
result = 0
for saving, count in sorted(savings.items()):
    if saving >= 100:
        result += count
    #print(f"{count} cheat(s) save {saving} picoseconds")
print('Part 1:', result)

# Solve Part 2
savings = cheats_grouped(grid, start, end, max_jump=20, min_saving=100)
result = 0
for saving, count in sorted(savings.items()):
    if saving >= 100:
        result += count
    #print(f"{count} cheat(s) save {saving} picoseconds")
print('Part 2:', result)
