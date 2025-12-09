#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc

points = aoc.lines_of_ints(sys.argv[1])

def rect_area(p, q):
    dx = abs(p[0] - q[0]) + 1
    dy = abs(p[1] - q[1]) + 1
    return dx * dy

def largest_rectangle():
    max_area = 0
    best_pair = None

    n = len(points)
    for i in range(n):
        for j in range(i + 1, n):
            area = rect_area(points[i], points[j])
            if area > max_area:
                max_area = area
                best_pair = (points[i], points[j])

    return max_area, best_pair

print(largest_rectangle())
