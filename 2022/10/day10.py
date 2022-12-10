#!/usr/bin/env python3

import sys
import fileinput

sx = 1
pixels = []

# Read from given file or stdin if no file given
for line in map(str.rstrip, fileinput.input(sys.argv[1:])):
    if line == 'noop':
        pixels.append(sx)
    else:
        instr, op = line.split(' ')
        if instr == 'addx':
            pixels.append(sx)
            pixels.append(sx)
            sx += int(op)

# Part 1
total = 0
for cycle in range(20, 220 + 1, 40):
    val = pixels[cycle - 1]
    total += cycle * val
print(total)

# Part 2
i = 0
for y in range(6):
    for x in range(40):
        sx = pixels[i]
        if sx < x - 1 or sx > x + 1:
            sys.stdout.write('.')
        else:
            sys.stdout.write('#')
        i += 1
    sys.stdout.write('\n')
