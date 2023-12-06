#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc

lines = aoc.lines(sys.argv[1])

times = aoc.ints(lines[0])
distances = aoc.ints(lines[1])

# For bisection, just return True/False
def good_hold_time(time, distance, hold_time):
    time_left = time - hold_time

    if time_left * hold_time > distance:
        return True

    return False

# TODO: find_min_hold_time and find_max_hold_time
# are very similar. Could be broken out to a single
# bisection function.
def find_min_hold_time(time, distance):
    min_hold_time = 1
    max_hold_time = time - 1

    # Use bisect to find the minimum value of hold_time
    while min_hold_time < max_hold_time:
        mid_hold_time = (min_hold_time + max_hold_time) // 2
        if good_hold_time(time, distance, mid_hold_time):
            max_hold_time = mid_hold_time
        else:
            min_hold_time = mid_hold_time + 1

    return min_hold_time

def find_max_hold_time(time, distance):
    min_hold_time = 1
    max_hold_time = time - 1

    # Use bisect to find the minimum value of hold_time
    while min_hold_time < max_hold_time:
        mid_hold_time = (min_hold_time + max_hold_time + 1) // 2
        if good_hold_time(time, distance, mid_hold_time):
            min_hold_time = mid_hold_time
        else:
            max_hold_time = mid_hold_time - 1

    return max_hold_time

# Use bisection to find min/max hold_times
def sim_race(time, distance):

    min_hold_time = find_min_hold_time(time, distance)
    max_hold_time = find_max_hold_time(time, distance)

    return max_hold_time + 1 - min_hold_time

prod = 1
for i in range(len(times)):
    prod *= sim_race(times[i], distances[i])

print('Part 1:', prod)

# Part 2, concatenate all numbers on line
time = int(lines[0].split(':')[1].replace(' ', ''))
distance = int(lines[1].split(':')[1].replace(' ', ''))

print('Part 2:', sim_race(time, distance))