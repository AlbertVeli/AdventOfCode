#!/usr/bin/env python3

import sys
import re
from collections import defaultdict

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

positions = []
for s in open(sys.argv[1]).readlines():
    s = s.rstrip()
    pos = int(re.findall(r'Player \d starting position: (\d)', s)[0])
    positions.append(pos)

rolls = defaultdict(int)
for a in range(1, 4):
    for b in range(1, 4):
        for c in range(1, 4):
            outcome = a + b + c
            rolls[outcome] += 1
# convert to iterable type
rolls = tuple(rolls.items())

# Move one player, return new position and new score
def move(pos, score, roll):
    # pos goes from 0 - 9
    pos = (pos + roll - 1) % 10 + 1
    return (pos, score + pos)

# One game state = scores and positions of both players
# Keep all seen states in a dict and count how many times they occur
states = { (0, positions[0], 0, positions[1]): 1 }
wins = [0, 0]
while True:
    new_states = defaultdict(int)
    # universes = how many universes with this state there are
    for state, universes in list(states.items()):
        score1, pos1, score2, pos2 = state
        # roll_count = ways of rolling this universe
        # each will generate a new universe
        for roll, roll_count in rolls:
            p1, s1 = move(pos1, score1, roll)
            if s1 >= 21:
                wins[0] += universes * roll_count
                continue
            for roll2, roll2_count in rolls:
                p2, s2 = move(pos2, score2, roll2)
                if s2 >= 21:
                    wins[1] += universes * roll_count * roll2_count
                    continue
                new_states[(s1, p1, s2, p2)] += universes * roll_count * roll2_count

    # Both players have finished
    if len(new_states) == 0:
        break

    states = new_states

print(max(wins))
