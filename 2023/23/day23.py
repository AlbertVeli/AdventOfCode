#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc
import copy

grid = aoc.char_matrix(sys.argv[1])
width = len(grid[0])
height = len(grid)

start_position = (grid[0].index('.'), 0)
end_position = (grid[-1].index('.'), height - 1)

def dump_grid(visited: list[tuple]):
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if (x, y) in visited:
                print('O', end='')
            else:
                print(c, end='')
        print('')

# east, south, west, up
dirs = ((1, 0), (0, 1), (-1, 0), (0, -1))

def add_pos_dir(pos, dir):
    return tuple(map(sum, zip(pos, dir)))

def possible_positions(cur_pos, visited):
    l = []
    for dir in dirs:
        x, y = add_pos_dir(cur_pos, dir)
        if x < 0 or x > width - 1 or y < 0 or y > height - 1:
            continue
        if (x, y) in visited:
            continue
        c = grid[y][x]
        if c == '#':
            continue
        elif c == '>' and dir == (-1, 0):
            continue
        elif c == 'v' and dir == (0, -1):
            continue
        else:
            l.append((x, y))
    return l

def find_max_path(from_pos: tuple, visited: list[tuple], taken_steps: int):
    if from_pos == end_position:
        return taken_steps

    # Optimization, continue walking until a fork
    # this reduces recursion depth
    single_steps = 0
    single_visited = copy.copy(visited)
    while True:
        #dump_grid(single_visited)
        #input('')
        positions = possible_positions(from_pos, single_visited)
        l = len(positions)
        if l > 1:
            break
        if l == 0:
            # nowhere to go, return 0
            break
        from_pos = positions[0]
        single_visited.append(from_pos)
        single_steps += 1
        if from_pos == end_position:
            return taken_steps + single_steps

    max_steps = 0
    for new_pos in positions:
        new_visited = copy.copy(single_visited)
        new_visited.append(new_pos)
        new_steps = find_max_path(new_pos, new_visited, taken_steps + single_steps + 1)
        if new_steps > max_steps:
            max_steps = new_steps
    return max_steps

# Probably not good solution if this is needed...
#sys.setrecursionlimit(10000)

print('Part 1:', find_max_path(start_position, [start_position], 0))
#dump_grid([start_position])
# Part 2, remove all '>', 'v' slopes
for row in grid:
    for x, c in enumerate(row):
        if c == '>' or c == 'v' or c == '<' or c == '^':
            row[x] = '.'
#dump_grid([start_position])
print('Part 2:', find_max_path(start_position, [start_position], 0))