#!/usr/bin/env python3

import sys
sys.path.insert(0,'../')
from aoc_input import *
import networkx as nx

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

a = input_as_lines(sys.argv[1])

G = nx.Graph()

for line in a:
    a, b = re.findall(r'([A-Za-z]+)', line)
    if not a in G:
        G.add_node(a)
    if not b in G:
        G.add_node(b)
    G.add_edge(a, b)

all_the_paths = []

# print all paths from node to goal
# Algorithm from: https://www.geeksforgeeks.org/find-paths-given-source-destination/
def all_paths(node, goal, visited, path, small):

    global all_the_paths

    # Mark the current node as visited and store in path
    visited[node] += 1
    path.append(node)
    #print(node, path)

    if node == goal:
        #print(path)
        if not path in all_the_paths:
            all_the_paths.append(path)
    else:
        # Recurse for all adjacent nodes
        for neigh in nx.all_neighbors(G, node):
            v = visited[neigh]
            if v == 0 or (neigh == small and v == 1 ) or neigh.isupper():
                # Must copy visited and path here
                all_paths(neigh, goal, visited.copy(), path.copy(), small)

        # Remove current vertex from path[] and mark it as unvisited
        path.pop()
        visited[node] -= 1

visited = dict()
smalls = []
for n in G.nodes:
    visited[n] = 0
    if n != 'start' and n != 'end' and n.islower():
        smalls.append(n)

for small in smalls:
    path = []
    all_paths('start', 'end', visited.copy(), path, small)

print(len(all_the_paths))
