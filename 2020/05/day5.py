#!/usr/bin/env python3

import sys
import typing

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

# Return list of (row, col)
def read_input(fname: str) -> typing.List[tuple]:
    a = []
    for line in open(fname).read().splitlines():
        row = int(line[:7].replace('B','1').replace('F','0'), 2)
        col = int(line[7:].replace('R','1').replace('L','0'), 2)
        a.append((row, col))
    return a

a = read_input(sys.argv[1])

seats = []
for row, col in a:
    seat = row * 8 + col
    seats.append(seat)

print('max', max(seats))

# part 2
seats.sort()
for i in range(1, len(seats)):
    if seats[i] - seats[i - 1] > 1:
        #print(seats[i-1], seats[i])
        print('missing', seats[i] - 1)
