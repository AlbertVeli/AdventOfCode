#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc

DIR = {'R': 1, 'L': -1}

moves = aoc.line_of_letterints(sys.argv[1])

def part1(moves):
    """Count how many times the position returns to zero."""
    pos = 50
    zero_count = 0

    for direction, dist in moves:
        pos = (pos + DIR[direction] * dist) % 100
        if pos == 0:
            zero_count += 1

    return zero_count

def part2(moves):
    """Count how many times the dial points at zero during any click."""
    pos = 50
    zero_count = 0

    for direction, dist in moves:
        step = DIR[direction]

        # Determine how many clicks until the next zero in this direction.
        # R: first zero is (100 - pos) clicks away
        # L: first zero is pos clicks away,
        #   except when pos is already 0, then it's 100 clicks away.
        if pos == 0:
            first = 100
        else:
            first = (100 - pos) if step == 1 else pos

        # If the rotation is long enough to reach the first zero,
        # count that hit + one for every full 100 clicks after that.
        if dist >= first:
            hits = 1 + (dist - first) // 100
            zero_count += hits

        # Update position
        pos = (pos + step * dist) % 100

    return zero_count

print('Part 1:', part1(moves))
print('Part 2:', part2(moves))
