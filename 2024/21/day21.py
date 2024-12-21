#!/usr/bin/env python3

import sys
import networkx as nx
from functools import cache

# Define keypads
positions1 = {
    (0, 0): '7', (0, 1): '8', (0, 2): '9',
    (1, 0): '4', (1, 1): '5', (1, 2): '6',
    (2, 0): '1', (2, 1): '2', (2, 2): '3',
                 (3, 1): '0', (3, 2): 'A'
}

positions2 = {
                 (0, 1): '^', (0, 2): 'A',
    (1, 0): '<', (1, 1): 'v', (1, 2): '>'
}

# Inverse mappings for graph traversal
positions1_inv = {v: k for k, v in positions1.items()}
positions2_inv = {v: k for k, v in positions2.items()}

# Build graph for a keypad
def build_graph(positions):
    G = nx.Graph()
    for (x, y), key in positions.items():
        neighbors = [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
        for new_x, new_y in neighbors:
            if (new_x, new_y) in positions:
                G.add_edge(key, positions[(new_x, new_y)])
    return G

# Build graphs
G_door = build_graph(positions1)
G_robo = build_graph(positions2)

# Convert a path into robot commands
def robo_moves(path, mapping):
    moves = []
    for start, end in zip(path, path[1:]):
        sx, sy = mapping[start]
        ex, ey = mapping[end]
        if ex > sx:
            moves.append('v')
        elif ex < sx:
            moves.append('^')
        elif ey > sy:
            moves.append('>')
        elif ey < sy:
            moves.append('<')
    moves.append('A')
    return moves

# Find all shortest paths
@cache
def get_possible_moves(G, start, end):
    return list(nx.all_shortest_paths(G, start, end))

# Recursive function to calculate the minimal cost
@cache
def n_moves(start, end, r, max_depth):
    if r == max_depth:  # Last robot
        moves = get_possible_moves(G_robo, start, end)
        mapping = positions2_inv
        min_cost = float('inf')
        for moveset in moves:
            robot_moves = robo_moves(moveset, mapping)
            min_cost = min(len(robot_moves), min_cost)
        return min_cost

    G, mapping = (G_door, positions1_inv) if r == 0 else (G_robo, positions2_inv)
    possible_paths = get_possible_moves(G, start, end)
    min_cost = float('inf')

    for path in possible_paths:
        robot_moves = robo_moves(path, mapping)
        moves_cost = 0
        ends = robot_moves
        starts = 'A' + ''.join(robot_moves[:-1])
        for i in range(len(starts)):
            start = starts[i]
            end = ends[i]
            cost = n_moves(start, end, r + 1, max_depth)
            moves_cost += cost
        min_cost = min(min_cost, moves_cost)

    return min_cost

# Extract the numeric part of a code
def get_numeric_part(code):
    numeric_str = ''.join(filter(str.isdigit, code))
    return int(numeric_str)

# Main calculation function
def conondrum(codes, max_depth):
    total_cost = 0
    for code in codes:
        extended_code = 'A' + code
        code_cost = sum(n_moves(extended_code[i], extended_code[i + 1], 0, max_depth) for i in range(len(extended_code) - 1))
        numeric_part = get_numeric_part(code[:-1])
        total_cost += code_cost * numeric_part
    return total_cost

with open(sys.argv[1], 'r') as f:
    lines = f.read().splitlines()

print('Part 1:', conondrum(lines, 2))
print('Part 2:', conondrum(lines, 25))
