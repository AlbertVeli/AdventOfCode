#!/usr/bin/env python3

import sys
from itertools import combinations

# parse input
scanners = []
scanner = []
for line in open(sys.argv[1]):
    line = line.rstrip()
    if '--- scanner' in line:
        # not first line
        if scanner and len(scanner) > 0:
            scanners.append(scanner)
        scanner = []
    elif len(line) > 0:
        x, y, z = map(int, line.split(','))
        scanner.append((x, y, z))
scanners.append(scanner)

distances = []

# --- ok, I didn't figure out the orientation stuff, so
# I peeked at my son's solution. Sorry. But it is allowed
# to peek after a large number of hours of trying.

def sub(a, b):
    l = []
    for x, y in zip(a, b):
        l.append(x - y)
    return tuple(l)

def add(a, b):
    l = []
    for x, y in zip(a, b):
        l.append(x + y)
    return tuple(l)

# return dict of all differences for all coords
def diffs(coords):
    d = dict()
    for p in coords:
        l = list()
        for q in coords:
            l.append(sub(p, q))
        d[p] = l
    return d

# return one of 24 possible orientations
def orientexpress(p, i):
    x, y, z = p
    return (
        (+x, +y, +z), (+y, +z, +x), (+z, +x, + y), (+z, +y, -x), (+y, +x, -z), (+x, +z, -y),
        (+x, -y, -z), (+y, -z, -x), (+z, -x, - y), (+z, -y, +x), (+y, -x, +z), (+x, -z, +y),
        (-x, +y, -z), (-y, +z, -x), (-z, +x, - y), (-z, +y, +x), (-y, +x, +z), (-x, +z, +y),
        (-x, -y, +z), (-y, -z, +x), (-z, -x, + y), (-z, -y, -x), (-y, -x, -z), (-x, -z, -y)
    )[i]

# return list of lists of all orientations
def all_orientations(points):
    ao = []
    for i in range(24):
        ol = []
        for x in points:
            ol.append(orientexpress(x, i))
        ao.append(ol)
    return ao

def find_offset(coords0, coords2):
    diff1 = diffs(coords0)
    for orientation in all_orientations(coords2):
        diff2 = diffs(orientation)
        # k1: diffs of all points from k1
        for k1, v1 in diff1.items():
            # k2: diffs of all points from k2
            for k2, v2 in diff2.items():
                if len(set(v1) & set(v2)) >= 12:
                    return (sub(k1, k2), orientation)
    return False

def new_absolute(absolute, coords):
    diff, coords2 = find_offset(absolute, coords)
    for p in coords2:
        np = add(p, diff)
        # no duplicates
        if not np in absolute:
            absolute.append(np)
    return absolute


# Convert all points to relative scanner 0
def relative_scanner0(absolute, remaining):
    global distances

    while True:
        # This takes time, print progress
        print(len(remaining))

        if len(remaining) == 0:
            # done, all converted to absolute
            return absolute

        for r in remaining:
            offset = find_offset(absolute, r)
            if offset:
                distances.append(offset[0])
                absolute = new_absolute(absolute, r)
                remaining.remove(r)
                break

# main

absolute = scanners[0]
remaining = scanners[1:]

l = relative_scanner0(absolute, remaining)

# Sort, to compare with task example output
#l = sorted(l)
#print(l)
print('part 1:', len(l))

def manhattan(o1, o2):
    l = []
    for x1, x2 in zip(o1, o2):
        l.append(abs(x1 - x2))
    #print(o1, o2, sum(l))
    return sum(l)

manhattans = []
for o1, o2 in combinations(distances, 2):
    manhattans.append(manhattan(o1, o2))
print('part 2:', max(manhattans))
