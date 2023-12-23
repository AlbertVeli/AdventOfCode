#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc
from collections import deque
import networkx as nx

lines = aoc.lines(sys.argv[1])
height, width = len(lines), len(lines[0])

# south, west, up, east
dirs = ((0, 1), (-1, 0), (0, -1), (1, 0))

def add_pos_dir(pos, dir):
    return tuple(map(sum, zip(pos, dir)))

# use dict instead of list of rows
# dict is faster (hashtable lookup)
# numpy array might be even faster
# since each element is the same size.
# In C you could define a lookup-table
# with the start offset for each row,
# that would be as fast as numpy.
grid = dict()
for y, row in enumerate(lines):
    for x, c in enumerate(row):
        pos = (x, y)
        # Replace hills with . for part 2
        if c == '<' or c == '>' or c == 'v' or c == '^':
            c = '.'
        grid[pos] = c

start_pos = (lines[0].index('.'), 0)
end_pos = (lines[-1].index('.'), height - 1)

visited = {start_pos}
# stack of (pos, dir) to try
# init with next possible step(s)
stack = deque([])
for i_dir, i_start_dir in enumerate(dirs):
    pos = add_pos_dir(start_pos, i_start_dir)
    if pos in grid and grid[pos] == '.':
        stack.append((start_pos, i_dir))
graph = nx.Graph()

# TODO: cleanup the following part, building up
# the nx.Graph edges, until ---
while len(stack) > 0:
    st_pos, i_start_dir = stack.pop()
    prev_pos = st_pos
    cur_pos = add_pos_dir(st_pos, dirs[i_start_dir])
    length = 1
    visited.add(cur_pos)
    new_dirs = []

    for i_dir, dir in enumerate(dirs):
        new_pos = add_pos_dir(cur_pos, dir)
        c = grid[new_pos]
        if new_pos in grid and c != '#':
            new_dirs.append((i_dir, new_pos in visited))

    while len(new_dirs) == 2:
        for dir, _ in new_dirs:
            if prev_pos != add_pos_dir(cur_pos, dirs[dir]):
                i_start_dir = dir
                break
        prev_pos = cur_pos
        cur_pos = add_pos_dir(cur_pos, dirs[i_start_dir])
        length += 1
        visited.add(cur_pos)

        new_dirs = []
        for i_dir, dir in enumerate(dirs):
            new_pos = add_pos_dir(cur_pos, dir)
            if new_pos in visited:
                new_dirs.append((i_dir, True))
            elif new_pos in grid and grid[new_pos] != '#':
                new_dirs.append((i_dir, False))

    graph.add_edge(st_pos, cur_pos, cost = length)

    dirs_to_visit = []
    for dir, is_visited in new_dirs:
        if not is_visited:
            dirs_to_visit.append(dir)
        for dir2 in dirs_to_visit:
            stack.append((cur_pos, dir2))

# ---

# phew, the hard part is done, building the graph
# now just use nx to get all_simple_paths
# from start to end and select the longest one
max_length = 0
for path in nx.all_simple_paths(graph, start_pos, end_pos):
    length = nx.path_weight(graph, path, 'cost')
    if length > max_length:
        max_length = length

print('Part 2:', max_length)