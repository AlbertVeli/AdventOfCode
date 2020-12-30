#!/usr/bin/env python3

# Day 3, with some speed optimizations
# Not really necessary for day 3, but probably later

import sys
import typing
import array

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

width = 0
heigth = 0

# Use 1-d array of bytes to keep pixels
def read_input(fname: str) -> array.array[int]:
    global width
    global heigth
    a = array.array('b')
    width = len(open(fname).readline().rstrip())
    for line in open(fname).read().splitlines():
        heigth += 1
        for c in line:
            # Each pixel is True or False
            a.append(c == '#')
    return a

a = read_input(sys.argv[1])

# for faster x,y lookup in a
ytab = array.array('I')
for y in range(heigth):
    ytab.append(y * width)

def get_pixel(x: int, y: int) -> int:
    return a[(x % width) + ytab[y]]

def slope(dx: int, dy: int) -> int:
    x = 0
    y = 0
    trees = 0
    while True:
        x += dx
        y += dy
        if y >= heigth:
            break
        if get_pixel(x, y) == True:
            trees += 1
    return trees


# part 1
print(slope(3, 1))

# part 2
slopes = [
        (1,1),
        (3,1),
        (5,1),
        (7,1),
        (1,2)
        ]

f = 1
for s in slopes:
    f *= slope(s[0], s[1])

print(f)
