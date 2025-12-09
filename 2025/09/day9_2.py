#!/usr/bin/env python3

# The part 2 solution is mostly from the
# AoC subreddit. I got stuck real bad.

import sys
from dataclasses import dataclass
from collections import deque

UNKNOWN = 0
BOUNDARY = 1
OUTSIDE = 2

@dataclass(frozen=True)
class Point:
    x: int
    y: int

def all_point_pairs():
    pairs = []
    n = len(red_tiles)
    for i in range(n):
        for j in range(i + 1, n):
            pairs.append((red_tiles[i], red_tiles[j]))
    return pairs

def rectangle_area(a, b):
    return (abs(a.x - b.x) + 1) * (abs(a.y - b.y) + 1)

def build_compressed_grid():
    xs = set()
    ys = set()

    xs.add(0)
    ys.add(0)

    for p in red_tiles:
        xs.add(p.x)
        ys.add(p.y)

    max_x = max(xs)
    max_y = max(ys)
    xs.add(max_x + 1)
    ys.add(max_y + 1)

    sorted_x = sorted(xs)
    sorted_y = sorted(ys)

    xmap = {x: i for i, x in enumerate(sorted_x)}
    ymap = {y: i for i, y in enumerate(sorted_y)}

    W = len(sorted_x)
    H = len(sorted_y)

    # 0 = unknown, 1 = boundary, 2 = outside
    grid = [[0] * H for _ in range(W)]

    n = len(red_tiles)
    for i in range(n):
        cur = red_tiles[i]
        nxt = red_tiles[(i + 1) % n]

        x_min = min(cur.x, nxt.x)
        x_max = max(cur.x, nxt.x)
        y_min = min(cur.y, nxt.y)
        y_max = max(cur.y, nxt.y)

        if cur.y == nxt.y:  # horizontal
            y_idx = ymap[cur.y]
            x1 = xmap[x_min]
            x2 = xmap[x_max]
            for x in range(x1, x2 + 1):
                grid[x][y_idx] = BOUNDARY

        elif cur.x == nxt.x:  # vertical
            x_idx = xmap[cur.x]
            y1 = ymap[y_min]
            y2 = ymap[y_max]
            for y in range(y1, y2 + 1):
                grid[x_idx][y] = BOUNDARY

        else:
            raise ValueError("Non axis-aligned edge")

    flood_fill_outside(0, 0, grid)
    return grid, xmap, ymap


def flood_fill_outside(start_x, start_y, grid):
    W = len(grid)
    H = len(grid[0])

    if grid[start_x][start_y] == UNKNOWN:
        grid[start_x][start_y] = OUTSIDE

    q = deque([(start_x, start_y)])

    while q:
        x, y = q.popleft()
        for dx, dy in ((0,1),(0,-1),(1,0),(-1,0)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < W and 0 <= ny < H and grid[nx][ny] == UNKNOWN:
                grid[nx][ny] = OUTSIDE
                q.append((nx, ny))


def is_rectangle_inside(tile1, tile2, grid, xmap, ymap):
    x1 = min(tile1.x, tile2.x)
    x2 = max(tile1.x, tile2.x)
    y1 = min(tile1.y, tile2.y)
    y2 = max(tile1.y, tile2.y)

    ix1 = xmap[x1]
    ix2 = xmap[x2]
    iy1 = ymap[y1]
    iy2 = ymap[y2]

    for y in range(iy1, iy2 + 1):
        for x in range(ix1, ix2 + 1):
            if grid[x][y] == OUTSIDE:
                return False

    return True

# main

# read input
red_tiles = []
with open(sys.argv[1]) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        x, y = map(int, line.split(","))
        red_tiles.append(Point(x, y))

grid, xmap, ymap = build_compressed_grid()

pairs = all_point_pairs()

best = 0
for a, b in pairs:
    area = rectangle_area(a, b)
    if area > best and is_rectangle_inside(a, b, grid, xmap, ymap):
        best = area

print(best)

