#!/usr/bin/env python3

import sys
import networkx as nx

# Global variables
G = nx.DiGraph()
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def build_graph(grid):
    rows, cols = len(grid), len(grid[0])

    for y in range(rows):
        for x in range(cols):
            # Explore neighbors
            for dy, dx in DIRECTIONS:
                ny, nx = y + dy, x + dx
                if 0 <= ny < rows and 0 <= nx < cols and grid[ny][nx] == grid[y][x] + 1:
                    G.add_edge((y, x), (ny, nx))

def find_trailheads(grid, value = 0):
    trailheads = []
    rows, cols = len(grid), len(grid[0])
    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == value:
                trailheads.append((y, x))
    return trailheads

def count_paths(G, trailheads, goals):
    """
    Count paths from trailheads to goals.
    """
    paths = 0
    for trailhead in trailheads:
        for goal in goals:
            if nx.has_path(G, trailhead, goal):
                paths += 1
    return paths

def count_paths_2(G, trailheads, goals):
    """
    Find all paths from trailheads to goals.
    """
    paths = 0
    for trailhead in trailheads:
        for goal in goals:
            if nx.has_path(G, trailhead, goal):
                for path in nx.all_simple_paths(G, trailhead, goal):
                    paths += 1
    return paths

# Main

grid = []
with open(sys.argv[1]) as f:
    for line in f:
        row = [int(char) for char in line.strip()]
        grid.append(row)
rows, cols = len(grid), len(grid[0])

build_graph(grid)

trailheads = find_trailheads(grid)
goals = find_trailheads(grid, 9)
#print(f"Trailheads: {trailheads}, Goals: {goals}")

print('Part 1:', count_paths(G, trailheads, goals))
print('Part 2:', count_paths_2(G, trailheads, goals))
