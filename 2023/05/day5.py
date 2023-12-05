#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc
from itertools import groupby

# Split lst into sublists with empty string as separator.
# This could be rewritten more readable.
def split_list(lst):
    return [list(group) for key, group in groupby(lst, lambda x: x == '') if not key]

lines = aoc.input_string(sys.argv[1])
a = split_list(list(map(str.rstrip, lines.split('\n'))))
# a[0] = ['seeds: 79 14 55 13']
seeds = aoc.ints(a[0][0])
# a[1] = ['seed-to-soil map:', '50 98 2', '52 50 48']
seed2soil = list(map(aoc.ints, a[1][1:]))
# a[2] = ['soil-to-fertilizer map:', '0 15 37', '37 52 2', '39 0 15']
soil2fert = list(map(aoc.ints, a[2][1:]))
# a[3] = ['fertilizer-to-water map:', '49 53 8', '0 11 42', '42 0 7', '57 7 4']
fert2water = list(map(aoc.ints, a[3][1:]))
# a[4] = ['water-to-light map:', '88 18 7', '18 25 70']
water2light = list(map(aoc.ints, a[4][1:]))
# a[5] = ['light-to-temperature map:', '45 77 23', '81 45 19', '68 64 13']
light2temp = list(map(aoc.ints, a[5][1:]))
# a[6] = ['temperature-to-humidity map:', '0 69 1', '1 0 69']
temp2hum = list(map(aoc.ints, a[6][1:]))
# a[7] = ['humidity-to-location map:', '60 56 37', '56 93 4']
hum2loc = list(map(aoc.ints, a[7][1:]))

ranges = [seed2soil, soil2fert, fert2water, water2light, light2temp, temp2hum, hum2loc]

# Is n in range src - (length - 1)
def in_range(n, src, length):
    if (n >= src) and (n < (src + length)):
        return True
    return False

# Return mapped number if in a range
# else return n
def get_rnum(n, l):
    for r in l:
        if in_range(n, r[1], r[2]):
            return r[0] + (n - r[1])
    return n

# Loop through all mappings
def get_loc(seed):
    val = seed
    for r in ranges:
        val = get_rnum(val, r)
    return val


locations = []
for seed in seeds:
    locations.append(get_loc(seed))

print('Part 1:', min(locations), '(seed ' + str(seed) + ')')

# Part 2
# Reverse order of mappings
ranges2 = list(reversed(ranges))

# Also reverse range lookup
def get_rnum_reversed(n, l):
    for r in l:
        # Use r[0] as source now
        # and r[1] as destination
        if in_range(n, r[0], r[2]):
            return r[1] + (n - r[0])
    return n

# Reverse of get_loc
def get_seed(location):
    val = location
    for l in ranges2:
        # l is a list of ranges
        val = get_rnum_reversed(val, l)
    return val

def seed_in_range(seed):
    for r in seedranges:
        start, l = r
        if (seed >= start) and (seed < (start + l)):
            return True
    return False

seedranges = []
for i in range(0, len(seeds), 2):
    seedranges.append((seeds[i], seeds[i + 1]))

# Loop through all possible locations
# do reverse mappings and check if resulting
# seed is in a valid range
location = 0
while True:
    seed = get_seed(location)
    if seed_in_range(seed):
        print('Part 2:', location, '(seed ' + str(seed) + ')')
        break
    location += 1
