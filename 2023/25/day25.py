#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc
# nx does all the heavy lifting here
import networkx as nx

# set to True to visualise
do_draw = False
if do_draw:
    import matplotlib.pyplot as plt

lines = aoc.lines(sys.argv[1])

if do_draw:
    def draw(G):
        plt.figure()
        nx.draw_networkx(G, pos = nx.spring_layout(G))
        plt.title('Merry Christmas!')
        plt.show()
        plt.close()

edges = []

# Parse nodes and edges
for line in lines:
    node, neighbors = line.split(': ')
    neighbors = neighbors.split()
    edges.extend((node, neighbor) for neighbor in neighbors)

G = nx.Graph(edges)

if do_draw:
    draw(G)

three_magi = nx.minimum_edge_cut(G)
#print(three_magi)
G.remove_edges_from(three_magi)

if do_draw:
    draw(G)

n = 1
for cc in nx.connected_components(G):
    n *= len(cc)
print('Part 1:', n)