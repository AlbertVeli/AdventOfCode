#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

# All possible combinations
score = {
    'A X' : 1 + 3, # rock - rock
    'A Y' : 2 + 6, # rock - paper
    'A Z' : 3 + 0, # rock - scissors
    'B X' : 1 + 0, # paper - rock
    'B Y' : 2 + 3, # paper - paper
    'B Z' : 3 + 6, # paper - scissors
    'C X' : 1 + 6, # scissors - rock
    'C Y' : 2 + 0, # scissors - paper
    'C Z' : 3 + 3  # scissors - scissors
}

# All combinations of what to pick to lose, draw, win
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

score1 = 0
score2 = 0
for line in map(str.rstrip, open(sys.argv[1])):
    score1 += score[line]
    score2 += score[d2[line]]

print('Part 1:', score1)
print('Part 2:', score2)
