#!/usr/bin/env python3

import sys
sys.path.insert(0,'../')
from aoc_input import *

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

a = input_as_line_of_ints(sys.argv[1])
fish = {}
for i in range(9):
    fish[i] = 0
for i in a:
    fish[i] += 1

org_fish = dict(fish)

def go_fishing(fish, days):
    for i in range(days):
        new_fishes = fish[0]
        for j in range(8):
            fish[j] = fish[j + 1]
        fish[6] += new_fishes
        fish[8] = new_fishes
    return sum(fish.values())

# Part 1
print(go_fishing(fish, 80))

# Part 2
fish = dict(org_fish)
print(go_fishing(fish, 256))
