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
l = [1] *len(cards)
for i, matches in enumerate(cards):
    mul = l[i]
    for n in range(i + 1, i + matches + 1):
            l[n] += mul

print('Part 2:', sum(l))