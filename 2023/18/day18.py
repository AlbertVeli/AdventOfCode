#!/usr/bin/env python3
import sys
sys.path.append('../..')
import aoc

def pos_mul_dir(pos, dir, mul):
    return (pos[0] + dir[0] * mul, pos[1] + dir[1] * mul)

dirs = {
    'R': (1, 0),
    'D': (0, 1),
    'L': (-1, 0),
    'U': (0, -1)
}

dirs2 = ((1, 0), (0, 1), (-1, 0), (0, -1))

pos1 = (0, 0)
pos2 = (0, 0)
corners1 = [pos1]
corners2 = [pos2]
lines = aoc.lines(sys.argv[1])
for line in lines:
    dir = line[0]
    line = line[2:].split()
    # part 1
    d = dirs[dir]
    length = int(line[0])
    pos1 = pos_mul_dir(pos1, d, length)
    corners1.append(pos1)

    # part 2
    color = line[1][2:-1]
    d = dirs2[int(color[-1])]
    length = int(color[:5], 16)
    pos2 = pos_mul_dir(pos2, d, length)
    corners2.append(pos2)

def manhattan_distance(point1, point2):
    return abs(point2[0] - point1[0]) + abs(point2[1] - point1[1])

# Simplified shoelace formula
def shoelace(corners):
    area = 0
    len_boundary = 1
    length = len(corners)
    for i in range(length):
        x1, y1 = corners[i]
        x2, y2 = corners[(i + 1) % length]
        area += x1 * y2 - y1 * x2
        len_boundary += manhattan_distance((x1, y1), (x2, y2))
    return int(abs(area) / 2 + len_boundary // 2 + 1)

print('Part 1:', shoelace(corners1))
print('Part 2:', shoelace(corners2))
