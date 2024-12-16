#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc
from collections import deque

# Globals
directions = {
    '<': (-1, 0),  # Left
    '^': (0, -1),  # Up
    '>': (1, 0),   # Right
    'v': (0, 1)    # Down
}

moves = []

def parse_input(input_lines):
    global moves

    warehouse = []

    # Read each line from the input
    for line in input_lines:
        if line.startswith('#'):
            warehouse.append(line)
        elif len(line.strip()) > 0:
            moves += [directions.get(move, (0, 0)) for move in line.strip()]

    return warehouse

def get_start(grid, char):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == char:
                return (x, y)

def visualize(warehouse):
    print('\n'.join(warehouse))

def move_robot(direction):
    global warehouse, position

    x, y = position
    dx, dy = direction
    new_x, new_y = x + dx, y + dy

    # Step 1: Check if the robot can move
    current_x, current_y = new_x, new_y
    while warehouse[current_y][current_x] == 'O':
        current_x += dx
        current_y += dy

    # If the final cell is not '.', movement is not possible
    if warehouse[current_y][current_x] != '.':
        return

    # Step 2: Move robot and packages
    # Start at the empty space and move everything back to the robot
    warehouse[current_y] = warehouse[current_y][:current_x] + 'O' + warehouse[current_y][current_x + 1:]
    while (current_x, current_y) != (x, y):  # Keep moving packages until we reach the robot
        prev_x, prev_y = current_x - dx, current_y - dy
        warehouse[current_y] = warehouse[current_y][:current_x] + warehouse[prev_y][prev_x] + warehouse[current_y][current_x + 1:]
        current_x, current_y = prev_x, prev_y

    # Move the robot to the new position
    warehouse[y] = warehouse[y][:x] + '.' + warehouse[y][x + 1:]
    warehouse[new_y] = warehouse[new_y][:new_x] + '@' + warehouse[new_y][new_x + 1:]

    # Update the global position
    position = (new_x, new_y)

def count_coordinates():
    result = 0
    for y, row in enumerate(warehouse):
        for x, cell in enumerate(row):
            if cell in ('O', '['):
                result += 100 * y + x
    return result

def convert_map(warehouse):
    """
    Converts the warehouse map for part 2 based on the rules:
    - If the tile is #, the new map contains ## instead.
    - If the tile is O, the new map contains [] instead.
    - If the tile is ., the new map contains .. instead.
    - If the tile is @, the new map contains @. instead.
    """
    # Define the mapping for each tile
    conversion = {
        '#': '##',  # Walls
        'O': '[]',  # Packages
        '.': '..',  # Empty space
        '@': '@.'   # Robot
    }

    # Convert each row in the warehouse
    converted_warehouse = []
    for row in warehouse:
        converted_row = ''.join(conversion[tile] for tile in row)
        converted_warehouse.append(converted_row)

    return converted_warehouse

def move_robot_horizontal(dx):
    global warehouse, position

    x, y = position
    new_x = x + dx

    if warehouse[y][new_x] == "#":
        return

    segment_start = new_x
    while warehouse[y][segment_start] in "[]":
        segment_start += dx

    if warehouse[y][segment_start] != ".":
        return

    # Extract the current line
    line = warehouse[y]

    # Build the new line based on the movement
    if dx == -1:
        new_line = (line[:segment_start] + line[segment_start + 1 : x + 1] + "." + line[x + 1:])
    elif dx == 1:
        new_line = (line[:x] + "." + line[x:segment_start] + line[segment_start + 1:])

    # Update the warehouse and position
    warehouse[y] = new_line
    position = (new_x, y)

def put_char(x, y, char):
    global warehouse
    warehouse[y] = warehouse[y][:x] + char + warehouse[y][x + 1:]

# XXX: move up and down could be refactored into a single function
def move_robot_up():
    global warehouse, position

    x, y = position
    new_y = y - 1

    if new_y < 0:
        return

    # Detect the stack above the robot
    stack = []
    if warehouse[new_y][x] == "[":
        stack.append((x, new_y))
        stack.append((x + 1, new_y))
    elif warehouse[new_y][x] == "]":
        stack.append((x - 1, new_y))
        stack.append((x, new_y))
    else:
        if warehouse[new_y][x] == ".":  # Empty space
            # Move the robot
            warehouse[y] = warehouse[y][:x] + "." + warehouse[y][x + 1:]
            warehouse[new_y] = warehouse[new_y][:x] + "@" + warehouse[new_y][x + 1:]
            position = (x, new_y)
        return

    box_coords = stack.copy()

    # Traverse upward to detect the entire stack row by row
    current_y = new_y
    while current_y >= 0:
        new_stack = []
        for bx, by in stack:
            if by == current_y:
                new_stack.append((bx, by))
                # Check above this box coordinate
                above_y = by - 1
                if above_y >= 0:
                    char = warehouse[above_y][bx]
                    if char == "#":  # Wall
                        return  # No movement possible
                    elif char =="[":
                        new_stack.append((bx, above_y))
                        new_stack.append((bx + 1, above_y))
                    elif char =="]":
                        new_stack.append((bx, above_y))
                        new_stack.append((bx - 1, above_y))
        if not new_stack:
            break
        for coord in new_stack:
            if coord not in box_coords:
                x, y = coord
                if warehouse[y][x] != ".":
                    box_coords.append(coord)
        stack = new_stack
        current_y -= 1

    box_coords.sort(key=lambda coord: coord[1])
    for bx, by in box_coords:
        char = warehouse[by][bx]
        warehouse[by] = warehouse[by][:bx] + "." + warehouse[by][bx + 1:]  # Replace with "."
        warehouse[by - 1] = warehouse[by - 1][:bx] + char + warehouse[by - 1][bx + 1:]  # Move char up

    # Move the robot upward
    x, y = position
    put_char(x, y, ".")
    put_char(x, y - 1, "@")
    position = (x, y - 1)

def move_robot_down():
    global warehouse, position

    x, y = position
    new_y = y + 1

    if new_y >= len(warehouse):
        return

    # Detect the stack below the robot
    stack = []
    if warehouse[new_y][x] == "[":
        stack.append((x, new_y))
        stack.append((x + 1, new_y))
    elif warehouse[new_y][x] == "]":
        stack.append((x - 1, new_y))
        stack.append((x, new_y))
    else:
        if warehouse[new_y][x] == ".":  # Empty space
            # Move the robot
            warehouse[y] = warehouse[y][:x] + "." + warehouse[y][x + 1:]
            warehouse[new_y] = warehouse[new_y][:x] + "@" + warehouse[new_y][x + 1:]
            position = (x, new_y)
        return

    box_coords = stack.copy()

    # Traverse downward to detect the entire stack row by row
    current_y = new_y
    while current_y < len(warehouse):
        new_stack = []
        for bx, by in stack:
            if by == current_y:
                new_stack.append((bx, by))
                # Check below this box coordinate
                below_y = by + 1
                if below_y < len(warehouse):
                    char = warehouse[below_y][bx]
                    if char == "#":  # Wall
                        return  # No movement possible
                    elif char == "[":
                        new_stack.append((bx, below_y))
                        new_stack.append((bx + 1, below_y))
                    elif char == "]":
                        new_stack.append((bx, below_y))
                        new_stack.append((bx - 1, below_y))
        if not new_stack:
            break
        for coord in new_stack:
            if coord not in box_coords:
                x, y = coord
                if warehouse[y][x] != ".":
                    box_coords.append(coord)
        stack = new_stack
        current_y += 1

    box_coords.sort(key=lambda coord: coord[1], reverse=True)
    for bx, by in box_coords:
        char = warehouse[by][bx]
        warehouse[by] = warehouse[by][:bx] + "." + warehouse[by][bx + 1:]  # Replace with "."
        warehouse[by + 1] = warehouse[by + 1][:bx] + char + warehouse[by + 1][bx + 1:]  # Move char down

    # Move the robot downward
    x, y = position
    put_char(x, y, ".")
    put_char(x, y + 1, "@")
    position = (x, y + 1)

def move_robot_part2(direction):
    dx, dy = direction
    if dx != 0:
        move_robot_horizontal(dx)
    elif dy == -1:
        move_robot_up()
    elif dy == 1:
        move_robot_down()

def move_char(direction):
    if direction == (-1, 0):
        return '<'
    if direction == (1, 0):
        return '>'
    if direction == (0, -1):
        return '^'
    if direction == (0, 1):
        return 'v'

# Main

lines = aoc.lines(sys.argv[1])
warehouse = parse_input(lines)
# Save the original warehouse for part 2
original_warehouse = warehouse.copy()
#visualize(warehouse)
position = get_start(warehouse, '@')
for move in moves:
    move_robot(move)
    #visualize(warehouse)
#visualize(warehouse)
print('Part 1:', count_coordinates())
warehouse = convert_map(original_warehouse)
position = get_start(warehouse, '@')
for move in moves:
    #visualize(warehouse)
    #input(f'Next move: {move_char(move)}')
    move_robot_part2(move)
visualize(warehouse)
print('Part 2:', count_coordinates())
