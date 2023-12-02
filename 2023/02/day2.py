#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc

# count used reds, greens and blues in one set
def count_rgb(st):
    reds = 12
    greens = 13
    blues = 14
    for s in st:
        n, col = s.split(' ')
        n = int(n)
        if col == 'red':
            reds -= n
        elif col == 'green':
            greens -= n
        elif col == 'blue':
            blues -= n
    return (reds, greens, blues)

lines = aoc.lines(sys.argv[1])
games = []
game = 1
# part 1, count id of possible games
goodgames = 0
# part 2, count powers
pows = 0
for line in lines:
    # Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    sets = list(map(str.strip, line.split(':')[1].strip().split(';')))
    # 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    # part 1, keep track of good games
    good = True
    # part 2, keep track of max r, g, b
    maxr = maxg = maxb = 0
    for st in sets:
        r, g, b = count_rgb(list(map(str.strip, st.split(','))))
        if not (r >= 0 and g >= 0 and b >= 0):
            good = False
        # part 2
        mr = 12 - r
        mg = 13 - g
        mb = 14 - b
        if mr > maxr:
            maxr = mr
        if mg > maxg:
            maxg = mg
        if mb > maxb:
            maxb = mb
    if good:
        goodgames += game
    pows += maxr * maxg * maxb
    game += 1

print('Part 1:', goodgames)
print('Part 2:', pows)