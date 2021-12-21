#!/usr/bin/env python3

import sys
import re

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

positions = []
scores = [0, 0]
for s in open(sys.argv[1]).readlines():
    s = s.rstrip()
    pos = int(re.findall(r'Player \d starting position: (\d)', s)[0])
    # keep 0-9 in positions, not 1-10
    positions.append(pos - 1)

# goes from 0 to 99
die = 0
rolls = 0

def roll():
    global die
    global rolls
    l = []
    for _ in range(3):
        # roll values go from 1 to 100, die + 1
        l.append(die + 1)
        die += 1
        die %= 100
    rolls += 3
    return sum(l)

def move(player):
    pos = positions[player]
    score = scores[player]
    # pos goes from 0 - 9
    pos = pos + roll()
    pos %= 10
    positions[player] = pos
    # add 1-10 to score, pos + 1
    score += pos + 1
    scores[player] = score

player = 0
while True:
    move(player)
    if scores[player] >= 1000:
        print(rolls * scores[1 - player])
        break
    player = 1 - player
