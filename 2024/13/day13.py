#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc

def minimize_presses(da, db, px, py, cost_a=3, cost_b=1):
    """
    Press buttons A and B to reach (px, py) from (0, 0).
    """
    dx1, dy1 = da
    dx2, dy2 = db

    # Brute force.
    # This will not work for part 2.
    # We need to find a better way to solve this.
    min_tokens = float('inf')
    best_a, best_b = None, None
    max_a = max(px // dx1, py // dy1) + 1
    max_b = max(px // dx2, py // dy2) + 1
    for a in range(max_a):
        for b in range(max_b):
            x_total = a * dx1 + b * dx2
            y_total = a * dy1 + b * dy2

            if x_total == px and y_total == py:
                tokens = a * cost_a + b * cost_b
                if tokens < min_tokens:
                    min_tokens = tokens
                    best_a, best_b = a, b

    if min_tokens == float('inf'):
        return False

    return min_tokens

data = aoc.lines_of_ints(sys.argv[1])

# Part 1
ntokens = 0
for i in range(0, len(data), 4):
    ax, ay = data[i + 0]
    bx, by = data[i + 1]
    px, py = data[i + 2]
    tokens = minimize_presses((ax, ay), (bx, by), px, py)
    if tokens:
        ntokens += tokens
print('Part 1:', ntokens)

# Part 2
ntokens = 0
offset = 10000000000000
for i in range(0, len(data), 4):
    ax, ay = data[i + 0]
    bx, by = data[i + 1]
    px, py = data[i + 2]
    tokens = minimize_presses((ax, ay), (bx, by), offset + px, offset + py)
    if tokens:
        ntokens += tokens
print('Part 2:', ntokens)
