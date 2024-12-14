#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc

class Robot:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def move(self):
        self.x = (self.x + self.dx) % width
        self.y = (self.y + self.dy) % height

    @property
    def pos(self):
        return (self.x, self.y)

    def __repr__(self):
        return f"Robot(pos=({self.x}, {self.y}), dir=({self.dx}, {self.dy}))"

def visualize_robots(robots):
    grid = [['.' for _ in range(width)] for _ in range(height)]
    # Count robots
    robot_counts = {}
    for robot in robots:
        x, y = robot.pos
        if (x, y) not in robot_counts:
            robot_counts[(x, y)] = 0
        robot_counts[(x, y)] += 1
    # Draw robots
    for (x, y), count in robot_counts.items():
        grid[y][x] = str(count)
    for row in grid:
        print(''.join(row))

def move_robots(robots):
    for robot in robots:
        robot.move()

def count_quadrants(robots):
    mid_row = height // 2
    mid_col = width // 2

    quadrants = {
        "top_left": 0,
        "top_right": 0,
        "bottom_left": 0,
        "bottom_right": 0
    }

    for robot in robots:
        x, y = robot.x % width, robot.y % height

        # Skip robots in the middle row or column
        if x == mid_col or y == mid_row:
            continue

        if x < mid_col and y < mid_row:
            quadrants["top_left"] += 1
        elif x >= mid_col and y < mid_row:
            quadrants["top_right"] += 1
        elif x < mid_col and y >= mid_row:
            quadrants["bottom_left"] += 1
        elif x >= mid_col and y >= mid_row:
            quadrants["bottom_right"] += 1

    return quadrants

def calc_safety(robots):
    # Multiply quadrant counts
    quadrants = count_quadrants(robots)
    result = 1
    for count in quadrants.values():
        result *= count
    return result

# Main

data = aoc.lines_of_ints(sys.argv[1])
width = 11
height = 7
width = 101
height = 103
robots = []
safeties = []
for x, y, dx, dy in data:
    robots.append(Robot(x, y, dx, dy))

for seconds in range(100):
    move_robots(robots)
    safeties.append(calc_safety(robots))

# Save the lowest safety value of the first 100 seconds
safest = min(safeties)
#visualize_robots(robots)
print('Part 1:', safeties[-1])

# Part 2
input('Part 2. Visually inspect the grids. Press enter to continue.')

# Assume the grid with a christmas tree has a low safety value
# Continue moving robots and visually inspect the grids with
# low safety values
while True:
    # Infinite loop, press Ctrl+C to stop
    move_robots(robots)
    seconds += 1
    safety = calc_safety(robots)
    if safety < safest:
        visualize_robots(robots)
        print(seconds + 1)
        input('Press Enter to continue...')

