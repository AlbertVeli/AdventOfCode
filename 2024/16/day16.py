#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc

from collections import defaultdict
from heapq import heappush, heappop

def get_start(labyrinth, char):
    for y, row in enumerate(labyrinth):
        for x, cell in enumerate(row):
            if cell == char:
                return (x, y)

def put_char(labyrinth, pos, char):
    x, y = pos
    labyrinth[y][x] = char

def count_chars(labyrinth, char):
    return sum(row.count(char) for row in labyrinth)

def visualize(labyrinth):
    for row in labyrinth:
        print(''.join(row))

def is_valid(x, y, labyrinth):
    rows, cols = len(labyrinth), len(labyrinth[0])
    return 0 <= x < cols and 0 <= y < rows and labyrinth[y][x] == "."

def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

# A* implementation, with a little help from ChatGPT
def find_best_paths(labyrinth, start, end):
    rows, cols = len(labyrinth), len(labyrinth[0])
    best_result = float('inf')
    best_paths = []
    visited = defaultdict(lambda: float('inf'))

    # Directions: (dx, dy, direction_name)
    directions = [(-1, 0, 'up'), (1, 0, 'down'), (0, -1, 'left'), (0, 1, 'right')]

    # Priority queue: (f, g, turns, x, y, direction, path)
    pq = []
    heappush(pq, (0, 0, 0, start[0], start[1], 'right', [start]))  # Start facing East

    while pq:
        f, g, turns, x, y, direction, path = heappop(pq)

        # If we reach the end, evaluate the path
        if (x, y) == end:
            result = 1000 * turns + len(path)
            if result < best_result:
                # Found a new best result, reset paths
                best_result = result
                best_paths = [path]
            elif result == best_result:
                # Found another path with the same best result
                best_paths.append(path)
            continue

        # Track the state (x, y, direction)
        state = (x, y, direction)
        current_score = 1000 * turns + len(path)
        # Allow revisits if the current path score is better or equivalent
        if current_score > visited[state]:
            continue
        visited[state] = current_score

        # Explore all neighbors
        for dx, dy, new_direction in directions:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny, labyrinth):
                # Increment turns if changing direction
                new_turns = turns + (1 if direction != new_direction else 0)
                # Compute heuristic
                h = manhattan_distance(nx, ny, end[0], end[1])
                # Add new state to the priority queue
                heappush(pq, (g + 1 + h, g + 1, new_turns, nx, ny, new_direction, path + [(nx, ny)]))

    return best_paths, best_result - 1

def mark_best_tiles(labyrinth, best_paths):
    rows, cols = len(labyrinth), len(labyrinth[0])
    marked = [[False] * cols for _ in range(rows)]

    # Mark all tiles that are part of any best path
    for path in best_paths:
        for x, y in path:
            marked[y][x] = True

    # Update the labyrinth visualization
    output = []
    for y, row in enumerate(labyrinth):
        output.append([
            'O' if (cell in {'.', 'S', 'E'} and marked[y][x]) else cell
            for x, cell in enumerate(row)
        ])
    return output

# Main

labyrinth = aoc.char_matrix(sys.argv[1])
#visualize(labyrinth)
start = get_start(labyrinth, 'S')
end = get_start(labyrinth, 'E')
put_char(labyrinth, start, '.')
put_char(labyrinth, end, '.')

# Merge part 1 and part 2 into one function.
# I originally used BFS for part 1.
best_paths, best_result = find_best_paths(labyrinth, start, end)
print('Part 1:', best_result)

# Part 2
output = mark_best_tiles(labyrinth, best_paths)
#visualize(output)
print('Part 2:', count_chars(output, 'O'))

