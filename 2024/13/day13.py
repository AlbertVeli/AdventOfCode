#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc
import numpy as np

def minimize_presses_1(A, B, P, cost_a=3, cost_b=1):
    """
    Bruteforce solution.
    """
    dx1, dy1 = A
    dx2, dy2 = B
    px, py = P

    # Brute force.
    # This will not work for part 2.
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

def minimize_presses_2(A, B, P, cost_a=3, cost_b=1):
    """
    Numpy matrix vector linalg solution.
    """
    ax, ay = A
    bx, by = B
    px, py = P

    # Construct matrix M and vector v
    M = np.matrix([(ax, bx), (ay, by)], dtype=float)
    v = np.array((px, py), dtype=float)

    # Solve the system of equations
    solution = np.linalg.solve(M, v)
    a, b = solution.round(2)
    if all(n.is_integer() for n in [a, b]):
        cost = int(a) * cost_a + int(b) * cost_b
        return cost

    return False


# Main

data = aoc.lines_of_ints(sys.argv[1])

# Part 1
ntokens = 0
for i in range(0, len(data), 4):
    A = data[i + 0]
    B = data[i + 1]
    px, py = data[i + 2]
    tokens = minimize_presses_1(A, B, (px, py))
    if tokens:
        #print((i // 4) + 1, tokens)
        ntokens += tokens
print('Part 1:', ntokens)

# Part 2
ntokens = 0
offset = 10000000000000
for i in range(0, len(data), 4):
    A = data[i + 0]
    B = data[i + 1]
    px, py = data[i + 2]
    tokens = minimize_presses_2(A, B, (offset + px, offset + py))
    if tokens:
        #print((i // 4) + 1, tokens)
        ntokens += tokens
print('Part 2:', ntokens)
