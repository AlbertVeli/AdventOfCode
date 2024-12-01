#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc

data = aoc.lines_of_ints(sys.argv[1])

# Split into two lists
left_list, right_list = zip(*data)

# Part 1: Calculate the total distance between the sorted lists
sorted_left = sorted(left_list)
sorted_right = sorted(right_list)

part1_result = sum(abs(a - b) for a, b in zip(sorted_left, sorted_right))
print("Part 1:", part1_result)

# Part 2: Calculate the similarity score
similarity_score = sum(n * right_list.count(n) for n in left_list)
print("Part 2:", similarity_score)
