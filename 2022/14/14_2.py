#!/usr/bin/env python3

import sys

lines = open(sys.argv[1]).read().rstrip().split('\n')
xs = set()
ys = set()
rows = []
for line in lines:
    points = line.split(' -> ')
    row = []
    for point in points:
        x, y = map(int, point.split(','))
        xs.add(x)
        ys.add(y)
        row.append((x, y))
    rows.append(row)

grid = []

def print_grid():
    for row in grid:
        for e in row:
            sys.stdout.write(e)
        sys.stdout.write('\n')

def insert_grid(x, y, c):
    # y starts at 0, no need to subtract miny
    grid[y][x - minx] = c

def get_grid(x, y):
    return grid[y][x - minx]

# build grid
minx = min(xs)
maxx = max(xs)
miny = 0
maxy = max(ys)
# part 2, infinite line at maxy + 2
maxy += 2
minx -= 200
maxx += 200
for y in range(maxy - miny + 1):
    row = []
    for x in range(maxx - minx + 1):
        row.append('.')
    grid.append(row)

def draw_line(x1, y1, x2, y2):
    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1
    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            insert_grid(x, y, '#')
# draw lines
for row in rows:
    for i in range(1, len(row)):
        x1, y1 = row[i - 1]
        x2, y2 = row[i]
        draw_line(x1, y1, x2, y2)


# bottom line
draw_line(minx, maxy, maxx, maxy)

#print_grid()

start = (500, 0)
insert_grid(start[0], start[1], '+')

#print_grid()

def move_one_sand(x, y):
    if y + 1 > maxy:
        # off grid
        return (False, False)
    # down
    if get_grid(x, y + 1) == '.':
        return (x, y + 1)
    # down left
    if x - 1 < minx:
        # off grid
        return (False, False)
    if get_grid(x - 1, y + 1) == '.':
        return (x - 1, y + 1)
    # down right
    if x + 1 > maxx:
        # off grid
        return (False, False)
    if get_grid(x + 1, y + 1) == '.':
        return (x + 1, y + 1)
    # at rest
    return (x, y)

def do_one_sand(x, y):
    if get_grid(x, y) == 'o':
        return False
    #insert_grid(x, y, 'o')
    #print_grid()
    newx, newy = move_one_sand(x, y)
    if newx == False:
        # off grid, done
        return False
    while newy != y:
        #input()
        #insert_grid(x, y, '.')
        x, y = newx, newy
        #insert_grid(x, y, 'o')
        #print_grid()
        newx, newy = move_one_sand(x, y)
        if newx == False:
            return False
    insert_grid(x, y, 'o')
    return True

sands = 0
while do_one_sand(start[0], start[1]):
    sands += 1
print_grid()
print(sands)
