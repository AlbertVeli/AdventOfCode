#!/usr/bin/env python3

import sys
sys.path.insert(0,'../')
from aoc_input import *
from collections import deque

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

a = input_as_line_of_ints(sys.argv[1])
fish = deque([0] * 9)
for i in a:
    fish[i] += 1

def go_fishing(fish, days):
    for i in range(days):
        new_fishes = fish[0]
        # rotate puts fish[0] -> fish[8]
        fish.rotate(-1)
        fish[6] += new_fishes
    return sum(fish)

# Part 1
print(go_fishing(fish, 80))

# Part 2
print(go_fishing(fish, 256 - 80))
