#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc
from collections import Counter

def blink(stone_counts):
    """
    Don't use huge lists of stones, it works for 25
    blinks but not for 75 blinks. Use a Counter instead
    since there are many repeated values.
    """

    new_stone_counts = Counter()

    for stone, count in stone_counts.items():
        if stone == 0:
            # Rule 1: Replace 0 with 1
            new_stone_counts[1] += count
        elif len(str(stone)) & 1 == 0:
            # Rule 2: Split stones with even number of digits
            digits = str(stone)
            mid = len(digits) // 2
            left = int(digits[:mid])
            right = int(digits[mid:])
            new_stone_counts[left] += count
            new_stone_counts[right] += count
        else:
            # Rule 3: Multiply by 2024 for all other cases
            new_stone_counts[stone * 2024] += count

    return new_stone_counts

#stones = [125, 17]
stones = aoc.line_of_ints(sys.argv[1])
print('stones =', stones)

# Part 1
stone_counts = Counter(stones)
for i in range(25):
    stone_counts = blink(stone_counts)
print("Part 1:", sum(stone_counts.values()))

# Part 2
for i in range(50):
    stone_counts = blink(stone_counts)
print("Part 2:", sum(stone_counts.values()))
