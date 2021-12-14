#!/usr/bin/env python3

from collections import defaultdict
import sys
sys.path.insert(0,'../')
from aoc_input import *
import re

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

a = input_as_lines(sys.argv[1])

polymer = a[0]
d = dict()
for s in a[2:]:
    v1, v2 = re.findall(r'([A-Z]+) -> ([A-Z]+)', s)[0]
    d[v1] = v2

pairs = defaultdict(int)
for i in range(len(polymer) - 1):
    pair = polymer[i : i + 2]
    pairs[pair] += 1

def step(pairs):
    newpairs = pairs.copy()
    for key, val in pairs.items():
        a = key[0]
        b = key[1]
        newpairs[a + b] -= val
        newpairs[a + d[a+b]] += val
        newpairs[d[a+b] + b] += val

    return newpairs

for i in range(40):
    #print(i)
    pairs = step(pairs)

elements = sorted(list(set(d.values())))
print(elements)
counts = dict()
for e in elements:
    counts[e] = 0
counts[polymer[0]] = 1
for key, val in pairs.items():
    counts[key[1]] += val
print(counts)
print(max(counts.values()) - min(counts.values()))
