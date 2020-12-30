#!/usr/bin/env python3

# pip3 install --user networkx
# https://networkx.github.io/documentation/stable/
import networkx as nx
import sys

G = nx.Graph()

for line in sys.stdin:
    a, b = line.rstrip().split(')')
    G.add_edge(a, b)

sp = nx.shortest_path(G, 'YOU', 'SAN')

print('DBG:', sp)
# See README, don't count YOU or SAN. Don't count first orbit
# point either because you are already there, so len(sp) - 3
print(len(sp) - 3)
