#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc

# Part 1
alldirs = [
    (0, 1),   # Right
    (1, 0),   # Down
    (1, 1),   # Down-right
    (-1, 1),  # Up-right
    (0, -1),  # Left
    (-1, 0),  # Up
    (-1, -1), # Up-left
    (1, -1)   # Down-left
]

# Part 2
diagonals = [(1, 1), (-1, -1), (-1, 1), (1, -1)]

def count_xmas(grid):
    n = len(grid)
    m = len(grid[0])
    count = 0

    for x in range(n):
        for y in range(m):
            # Start search if the current cell contains 'X'
            if grid[x][y] == 'X':
                for dx, dy in alldirs:
                    # Check the next three characters in the current direction
                    if (
                        0 <= x + 3 * dx < n and
                        0 <= y + 3 * dy < m and
                        grid[x + dx][y + dy] == 'M' and
                        grid[x + 2 * dx][y + 2 * dy] == 'A' and
                        grid[x + 3 * dx][y + 3 * dy] == 'S'
                    ):
                        count += 1
    return count

def count_xmas_2(grid):
    n = len(grid)
    m = len(grid[0])
    count = 0

    # find As
    for x in range(1, n - 1):
        for y in range(1, m - 1):
            if grid[x][y] == 'A':
                m_count = 0
                s_count = 0
                top_left = None
                bottom_right = None

                # Check diagonals for 'M' and 'S'
                for dx, dy in diagonals:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < n and 0 <= ny < m:
                        if grid[nx][ny] == 'M':
                            m_count += 1
                        elif grid[nx][ny] == 'S':
                            s_count += 1
                        if (dx, dy) == (1, 1):
                            top_left = grid[nx][ny]
                        if (dx, dy) == (-1, -1):
                            bottom_right = grid[nx][ny]

                # Check for valid X-MAS pattern
                if m_count == 2 and s_count == 2 and top_left != bottom_right:
                    count += 1

    return count

a = aoc.lines(sys.argv[1])
print("Part 1:", count_xmas(a))
print("Part 2:", count_xmas_2(a))
