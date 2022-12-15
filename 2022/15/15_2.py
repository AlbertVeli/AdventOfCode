#!/usr/bin/env python3

import sys
import re

lines = open(sys.argv[1]).read().rstrip().split('\n')
sensors = []
for line in lines:
    sx, sy, bx, by = list(map(int, re.findall(r'([-]?\d+)', line)))
    sensors.append((sx, sy, abs(sx - bx) + abs(sy - by)))

# example
#maxx = 25
#maxy = 22
maxx = 4000000
maxy = 4000000

# Missing beacon must be on border of one of the signals
def manhattan_edge(x, y, dist):
    points = []
    for dx in range(dist + 1):
        dy = dist - dx
        for px, py in [
                # right down
                (x + dx, y + dy),
                # left down
                (x - dx, y + dy),
                # right up
                (x + dx, y - dy),
                # left up
                (x - dx, y - dy)]:
            if px >= 0 and px < maxx and py >= 0 and py < maxy:
                points.append((px, py))
    return points

# only for example
def draw_points(points):
    grid = []
    for y in range(maxy):
        row = []
        for x in range(maxx):
            row.append('.')
        grid.append(row)
    for x, y in points:
        grid[y][x] = '#'
    for y in range(maxy):
        print('{:2d}'.format(y), ''.join(grid[y]))

def covered_by_any_sensor(x, y):
    for sx, sy, dist in sensors:
        dist_xy = abs(sx - x) + abs(sy - y)
        if dist_xy <= dist:
            return True
    return False

for sx, sy, dist in sensors:
    for x, y in manhattan_edge(sx, sy, dist + 1):
        if not covered_by_any_sensor(x, y):
            print(x, y, 4000000 * x + y)
