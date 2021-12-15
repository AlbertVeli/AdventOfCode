#!/usr/bin/env python3

import sys
import numpy as np
import networkx as nx

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

a = []
for s in open(sys.argv[1]).readlines():
    a.append(list(map(int, list(s.rstrip()))))
sy = len(a)
sx = len(a[0])
a = np.array(a)

# Build graph from a
G = nx.DiGraph()
for y in range(sy):
    for x in range(sx):
        for d in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
            yy, xx = d
            if (yy >= 0) and (xx >= 0) and (yy < sy) and (xx < sx):
                G.add_edge((y, x), (yy, xx), weight = a[yy][xx])

best_path = nx.shortest_path_length(G, (0, 0), (sy-1, sx-1), 'weight', 'dijkstra')
print(best_path)
