#!/usr/bin/env python3

import sys
from itertools import product

# Can the remaining design be matched with the towel patterns?
def can_match(remaining):
    if not remaining:
        return True

    for pattern in towel_patterns:
        if remaining.startswith(pattern):
            if can_match(remaining[len(pattern):]):
                return True
    return False

# Main

with open(sys.argv[1], 'r') as f:
    lines = f.read().strip().splitlines()
towel_patterns = lines[0].split(", ")
designs = [line.strip() for line in lines[2:]]
#print("Towel Patterns:", towel_patterns)
#print("Designs:", designs)

# Part 1
possible = 0
for design in designs:
    if can_match(design):
        possible += 1
print("Part 1:", possible)

# Part 2

# Thanks ChatGPT for suggesting a dynamic programming algorithm
# because the recursive part 1 style counting is too slow for part 2
def dp_count_patterns(design):
    # dp[i] represents the number of ways to match
    # the first i characters of the design
    dp = [0] * (len(design) + 1)
    # Base case: one way to match an empty design
    # (which is to use no patterns)
    dp[0] = 1

    for i in range(1, len(design) + 1):
        for pattern in towel_patterns:
            if design[:i].endswith(pattern):
                dp[i] += dp[i - len(pattern)]

    return dp[len(design)]

possible = 0
for design in designs:
    possible += dp_count_patterns(design)
print("Part 2:", possible)
