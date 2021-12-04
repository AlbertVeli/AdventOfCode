#!/usr/bin/env python3

import sys
sys.path.insert(0,'../')
from aoc_input import *

import re
import numpy as np
from board import Board

# Read input
if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

a = input_as_lines(sys.argv[1])

nums = re.findall(r'(\d+)', a[0])
nums = list(map(int, nums))

boards = []
brd = []
lineno = 0
for line in a[1:]:
    if len(line) == 0:
        continue
    brd.append(re.findall(r'(\d+)', line))
    lineno += 1
    if lineno == 5:
        lineno = 0
        boards.append(Board(brd))
        brd = []

def part1():
    drawn = np.array([], int)
    for num in nums:
        drawn = np.append(drawn, num)
        for b in boards:
            if b.win(drawn):
                return b.score(num, drawn)

# Part 2 destroys board
def part2():
    drawn = np.array([], int)
    for num in nums:
        drawn = np.append(drawn, num)
        to_remove = []
        for b in boards:
            if b.win(drawn):
                to_remove.append(b)
        for r in to_remove:
            if len(boards) == 1:
                return b.score(num, drawn)
            boards.remove(r)

print('part 1:', part1())
print('part 2:', part2())
