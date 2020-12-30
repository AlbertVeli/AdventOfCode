#!/usr/bin/env python3

# pip3 install --user networkx
# https://networkx.github.io/documentation/stable/
import networkx as nx
import sys

DG = nx.DiGraph()

for line in sys.stdin:
    a, b = line.rstrip().split(')')
    DG.add_edge(a, b)

# There's probably some smarter way to count predecessors than this
def num_predecessors(DG, edge, num):
    l = list(DG.predecessors(edge))
    if len(l) == 0:
        return num
    else:
        return num_predecessors(DG, l[0], num + 1)

tot = 0
for e in DG:
    print(e, num_predecessors(DG, e, 0))
    tot += num_predecessors(DG, e, 0)

print(tot)
