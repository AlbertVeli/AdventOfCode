#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

d = {
    'A X' : 1 + 3,
    'A Y' : 2 + 6,
    'A Z' : 3 + 0,
    'B X' : 1 + 0,
    'B Y' : 2 + 3,
    'B Z' : 3 + 6,
    'C X' : 1 + 6,
    'C Y' : 2 + 0,
    'C Z' : 3 + 3
}

d2 = {
    'A X' : 'A Z',
    'A Y' : 'A X',
    'A Z' : 'A Y',
    'B X' : 'B X',
    'B Y' : 'B Y',
    'B Z' : 'B Z',
    'C X' : 'C Y',
    'C Y' : 'C Z',
    'C Z' : 'C X'
}

a = open(sys.argv[1]).read().rstrip().split('\n')
score1 = 0
score2 = 0
for line in a:
    score1 += d[line]
    score2 += d[d2[line]]

print('Part 1:', score1)
print('Part 2:', score2)
