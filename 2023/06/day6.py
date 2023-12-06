#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc

lines = aoc.lines(sys.argv[1])

times = aoc.ints(lines[0])
distances = aoc.ints(lines[1])

def sim_race(time, distance):
    num = 0
    for speed in range(1, time):
        time_left = time - speed
        if time_left * speed > distance:
            num += 1
    return num

prod = 1
for i in range(len(times)):
    prod *= sim_race(times[i], distances[i])

print('Part 1:', prod)

# Part 2, concatenate all numbers on line
time = int(lines[0].split(':')[1].replace(' ', ''))
distance = int(lines[1].split(':')[1].replace(' ', ''))

# Could do bisections here to find min/max hold time but
# brute force is fast enough for relatively small values
print('Part 2:', sim_race(time, distance))