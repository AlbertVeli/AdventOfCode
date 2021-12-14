#!/usr/bin/env python3

import sys
sys.path.insert(0,'../')
from aoc_input import *
import re

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

a = input_as_lines(sys.argv[1])

polymer = a[0]
d = {}
for s in a[2:]:
    v1, v2 = re.findall(r'([A-Z]+) -> ([A-Z]+)', s)[0]
    d[v1] = v2

def step(polymer):
    npolymer = str(polymer)
    inserts = 1
    for i in range(len(polymer) - 1):
        pair = polymer[i : i + 2]
        if pair in d:
            # insert d[pair] at i + inserts
            ix = i + inserts
            npolymer = npolymer[:ix] +  d[pair] + npolymer[ix:]
            inserts += 1
    return npolymer

elements = sorted(list(set(d.values())))
print(polymer)
for _ in range(10):
    polymer = step(polymer)

print(elements)
l = list(polymer)
counts = dict()
for e in elements:
    counts[e] = l.count(e)
print(counts)
print(max(counts.values()) - min(counts.values()))
