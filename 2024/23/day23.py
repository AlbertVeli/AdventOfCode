#!/usr/bin/env python3

import networkx as nx
from itertools import combinations
import sys

# Find sets of three interconnected computers (triangles)
def find_triangles(graph):
    triangles = set()
    for node in graph:
        neighbors = set(graph[node])
        for n1, n2 in combinations(neighbors, 2):
            if graph.has_edge(n1, n2):
                triangles.add(tuple(sorted([node, n1, n2])))
    return triangles

# Find the largest connected set of computers
def find_largest_connected_set(graph):
    cliques = list(nx.find_cliques(graph))
    largest_clique = max(cliques, key=len)
    return sorted(largest_clique)

# Main

with open(sys.argv[1], 'r') as f:
    data = f.read().strip().splitlines()

# Create a graph
graph = nx.Graph()

# Add edges to the graph
for line in data:
    a, b = line.split('-')
    graph.add_edge(a, b)

# Find triangles
triangles = find_triangles(graph)

# Count triangles with a node beginning with 't'
result = 0
for triangle in sorted(triangles):
    if any(node[0] == 't' for node in triangle):
        result += 1
        print('-'.join(triangle))
print('Part 1:', result)

# Find the largest connected set
print('Part 2:', ','.join(find_largest_connected_set(graph)))
