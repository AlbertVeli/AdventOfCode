#!/usr/bin/env python3

import sys
from math import prod
from dataclasses import dataclass
# For Disjoint Set (Union-Find) implementation
# pip install disjoint-set
from disjoint_set import DisjointSet

# NOTE:
# @dataclass is supported from Python 3.7 and later.
# prod is supported from Python 3.8 and later.
# disjoint-set pip package is required, union-find
# could also be implemented manually if needed.

@dataclass(frozen=True)
class Point3D:
    x: int
    y: int
    z: int

def read_points():
    points = []
    with open(sys.argv[1]) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            x, y, z = map(int, line.split(','))
            points.append(Point3D(x, y, z))
    return points

def squared_dist(a, b):
    """ Use squared distance to avoid floating point inaccuracies. """
    dx = a.x - b.x
    dy = a.y - b.y
    dz = a.z - b.z
    return dx * dx + dy * dy + dz * dz

points = read_points()
n = len(points)

# Build all edges with squared distance
edges = []
for i in range(n):
    for j in range(i + 1, n):
        d2 = squared_dist(points[i], points[j])
        edges.append((d2, i, j))

# Sort by distance
edges.sort(key=lambda e: e[0])

# Part 1 stop index (edge index, 0-based):
# - example input (20 lines), stop at edge index 9 (10 edges)
# - real input 1000 lines, stop at edge index 999 (1000 edges)
p1_stop = 999 if n == 1000 else 9

ds = DisjointSet.from_iterable(range(n))
components = n

p1 = None
p2 = None

for idx, (d2, a, b) in enumerate(edges):
    # Use disjoint-set pip library to track connected components
    # Only merge if they are in different circuits
    if ds.find(a) != ds.find(b):
        ds.union(a, b)
        components -= 1
        did_merge = True
    else:
        did_merge = False

    # Part 1: after considering the edge at p1_stop
    if idx == p1_stop and p1 is None:
        comp_sizes = {}
        for v in range(n):
            r = ds.find(v)
            comp_sizes[r] = comp_sizes.get(r, 0) + 1
        sizes = sorted(comp_sizes.values(), reverse=True)
        p1 = prod(sizes[:3])

    # Part 2: when everything is in one circuit,
    # output product of X-coordinates of the last did_merge pair
    if did_merge and components == 1:
        p2 = points[a].x * points[b].x
        break

print('Part 1:', p1)
print('Part 2:', p2)
