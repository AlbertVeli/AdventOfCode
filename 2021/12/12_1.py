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

num = 0

# print all paths from node to goal
# Algorithm from https://www.geeksforgeeks.org/find-paths-given-source-destination/
def all_paths(node, goal, visited, path):
    global num
    # Mark the current node as visited and store in path
    visited[node] += 1
    path.append(node)
    #print(node, path)

    if node == goal:
        #print(path)
        num += 1
    else:
        # Recurse for all adjacent nodes
        for neigh in nx.all_neighbors(G, node):
            v = visited[neigh]
            if v == 0 or neigh.isupper():
                # Must copy visited and path here
                all_paths(neigh, goal, visited.copy(), path.copy())

        # Remove current vertex from path[] and mark it as unvisited
        path.pop()
        visited[node] -= 1

visited = dict()
for n in G.nodes:
    visited[n] = 0
path = []
all_paths('start', 'end', visited, path)
print(num)
