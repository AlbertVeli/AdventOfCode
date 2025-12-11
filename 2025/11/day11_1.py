#!/usr/bin/env python3

import sys
import networkx as nx

def parse_graph():
    G = nx.DiGraph()
    with open(sys.argv[1], 'r') as f:
        lines = f.readlines()
    for line in lines:
        name, rhs = line.strip().split(':')
        name = name.strip()
        targets = rhs.strip().split()
        #print(f'{name} -> {targets}')
        for t in targets:
            G.add_edge(name, t)
    return G

def count_paths(G, start='you', end='out'):
    """
    Use convenient NetworkX function
    all_simple_paths to count ... all simple paths.
    """
    paths = nx.all_simple_paths(G, start, end)
    return len(list(paths))

G = parse_graph()
print('Part 1:', count_paths(G, 'you', 'out'))
