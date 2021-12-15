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

# Increase a by 1, change 10 to 1
def next_a(a):
    b = a + 1
    b[np.where(b == 10)] = 1
    return b

# Expand a to a 5 * 5 grid

# First expand original a 4 times to the right
aa = [a.copy()]
for i in range(1, 5):
    a = next_a(a)
    aa.append(a.copy())

# Then expand row0 4 times down
row0 = np.concatenate(aa, axis = 1)
rows = [row0]
for i in range(1, 5):
    row0 = next_a(row0)
    rows.append(row0)
a = np.concatenate(rows, axis = 0)

sy = sy * 5
sx = sx * 5
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
