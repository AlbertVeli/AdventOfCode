#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc
import copy

orig_arr = list(map(list, aoc.lines(sys.argv[1])))
arr = copy.deepcopy(orig_arr)

height = len(arr)
width = len(arr[0])

def dump_arr():
    for row in arr:
        print(''.join(row))

def get_rock(x, y):
    return arr[y][x]

def put_rock(x, y, c):
    arr[y][x] = c

# Roll one rock until it either
# hits an edge or another rock
# TODO: It is enough to only roll_north
#       and rotate arr, instead of 4 functions
def roll_north(x, y):
    for yy in range(y - 1, -1, -1):
        if get_rock(x, yy) == '.':
            put_rock(x, yy, 'O')
            put_rock(x, yy + 1, '.')
        else:
            break

def roll_south(x, y):
    for yy in range(y + 1, height):
        if get_rock(x, yy) == '.':
            put_rock(x, yy, 'O')
            put_rock(x, yy - 1, '.')
        else:
            break

def roll_west(x, y):
    for xx in range(x - 1, -1, -1):
        if get_rock(xx, y) == '.':
            put_rock(xx, y, 'O')
            put_rock(xx + 1, y, '.')
        else:
            break

def roll_east(x, y):
    for xx in range(x + 1, width):
        if get_rock(xx, y) == '.':
            put_rock(xx, y, 'O')
            put_rock(xx - 1, y, '.')
        else:
            break

def tilt_north():
    for y, row in enumerate(arr):
        for x, c in enumerate(row):
            if c == 'O':
                roll_north(x, y)

def tilt_south():
    for y in range(height - 1, -1, -1):
        row = arr[y]
        for x, c in enumerate(row):
            if c == 'O':
                roll_south(x, y)

def tilt_west():
    for y, row in enumerate(arr):
        for x, c in enumerate(row):
            if c == 'O':
                roll_west(x, y)

def tilt_east():
    for y, row in enumerate(arr):
        for x in range(width - 1, -1, -1):
            if get_rock(x, y) == 'O':
                roll_east(x, y)

def calc_weight():
    weight = 0
    for y, row in enumerate(arr):
        row_weight = height - y
        for c in row:
            if c == 'O':
                weight += row_weight
    return weight

tilt_north()

print('Part 1:', calc_weight())

arr = copy.deepcopy(orig_arr)

def do_cycle():
    tilt_north()
    tilt_west()
    tilt_south()
    tilt_east()

weights = []
hashdic = {}

# Find cycle_start and cycle_length
# The first time the hash of the array
# repeats we have a cycle which will
# repeat infinitely.
i = 0
while True:
    do_cycle()
    weights.append(calc_weight())
    arrhash = hash(tuple(map(tuple, arr)))
    if arrhash in hashdic:
        cycle_start = hashdic[arrhash]
        cycle_length = i - cycle_start
        # Found cycle, end loop
        break
    # Add index of this hash
    hashdic[arrhash] = i
    i += 1

wanted_index = 1000000000 - 1
# Calculate which index is the same as wanted_index
index = cycle_start + (wanted_index - cycle_start) % cycle_length
print('Part 2:', weights[index])