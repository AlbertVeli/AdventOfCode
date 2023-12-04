#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc

lines = aoc.lines(sys.argv[1])

scratchcard = []
for line in lines:
    a, b = line.split(':')[1].split('|')
    wins = aoc.ints(a)
    mynums = aoc.ints(b)
    scratchcard.append((wins, mynums))

# part 1
sm = 0
cards = []
for wins, mynums in scratchcard:
    common = list(set(wins).intersection(set(mynums)))
    l = len(common)
    if l > 0:
        sm += 2 ** (l - 1)
    # part 2
    cards.append(l)

print('Part 1:', sm)

# part 2
# TODO: refactor this to use a plain list instead
m = {n: 1 for n in range(1, len(cards) + 1)}
for i, matches in enumerate(cards):
    n = i + 1
    mul = m[n]
    for num in range(n + 1, n + matches + 1):
        if num in m:
            m[num] += mul
        else:
            m[num] = mul

print('Part 2:', sum(m.values()))