#!/usr/bin/env python3

import sys
from collections import deque

player1 = deque()
player2 = deque()

player = 1
for line in open(sys.argv[1]).read().splitlines():
    if len(line) == 0:
        continue
    if line.startswith('Player '):
        if line.replace('Player ', '').replace(':', '') == '1':
            player = 1
        else:
            player = 2
        continue
    val = int(line)
    if player == 1:
        player1.append(val)
    else:
        player2.append(val)

rnd = 1
def do_round():
    global rnd
    #print('1:', player1)
    #print('2:', player2)
    p1 = player1.popleft()
    p2 = player2.popleft()
    if p1 > p2:
        print('Player 1 wins round', rnd)
        player1.append(p1)
        player1.append(p2)
    elif p2 > p1:
        print('Player 2 wins round', rnd)
        player2.append(p2)
        player2.append(p1)
    else:
        print('Draw, quitting')
        sys.exit(1)
    rnd += 1

while True:
    do_round()
    if len(player1) == 0:
        print('Player 2 wins')
        winner = player2
        break
    elif len(player2) == 0:
        print('Player 1 wins')
        winner = player1
        break

print(winner)
multiplier = 1
res = 0
while len(winner) > 0:
    res += winner.pop() * multiplier
    multiplier += 1
print(res)
