#!/usr/bin/env python3

import sys
import fileinput
import numpy as np
import networkx as nx

# b = python 2d-array of grid
b = []
y = 0
# Read from given file or stdin if no file given
for line in map(str.rstrip, fileinput.input(sys.argv[1:])):
    a = list(line)
    if 'S' in a:
        start = a.index('S')
        a[start] = 'a'
        start = (y, start)
    if 'E' in a:
        end = a.index('E')
        a[end] = 'z'
        end = (y, end)
    a = list(map(lambda c: ord(c) - ord('a'), a))
    b.append(a)
    y += 1

sx = len(b[0])
sy = len(b)
# Convert b to np array (faster)
grid = np.array(b)

# Use nx.DiGraph to find shortest path
G = nx.DiGraph()

# Add edges for down, up, right, left
def add_neighs(x, y):
    poss = [(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)]
    for p in poss:
        # add edge if p is inside grid and elevation < 2
        # negative elevation is also allowed
        if p[0] >= 0 and p[0] < sy and p[1] >= 0 and p[1] < sx:
            if grid[p] - grid[(y, x)] < 2:
                G.add_edge((y, x), p)

# Add edges to G
for y in range(sy):
    for x in range(sx):
        add_neighs(x, y)

# Part 1, given start position
best_path = int(nx.shortest_path_length(G, start, end))
print('Part 1', best_path)

# Part 2, all start positions where grid is 0
ys, xs = np.where(grid == 0)
for i in range(len(ys)):
    y = ys[i]
    x = xs[i]
    try:
        path =  int(nx.shortest_path_length(G, (y, x), end))
    except:
        continue
    if path < best_path:
        best_path = path

print('Part 2:', best_path)
