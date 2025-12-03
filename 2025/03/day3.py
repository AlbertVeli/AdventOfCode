#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc

lines = aoc.lines(sys.argv[1])

def n_largest_in_order(s, n):
    """
    Return the lexicographically largest subsequence of
    length n from the digit string s, preserving order.
    Use a greedy algorithm.
    """
    if n <= 0 or n > len(s):
        return ""

    digits = [int(c) for c in s]
    L = len(digits)
    res = []
    start = 0

    for k in range(n):
        # Last index we can pick from while still having enough digits left
        last = L - (n - k)
        best_digit = -1
        best_pos = -1

        for i in range(start, last + 1):
            d = digits[i]
            if d > best_digit:
                best_digit = d
                best_pos = i
                if best_digit == 9:  # can't do better
                    break

        res.append(str(best_digit))
        start = best_pos + 1

    return int("".join(res))

p1 = 0
p2 = 0
for line in lines:
    p1 += n_largest_in_order(line.strip(), 2)
    p2 += n_largest_in_order(line.strip(), 12)

print("Part 1:", p1)
print("Part 2:", p2)
