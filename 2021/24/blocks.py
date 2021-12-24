#!/usr/bin/env python3

# Separate each block to a file (for diffing)
lines = open('input.txt').read().rstrip().split('\n')
f = False
for i in range(len(lines)):
    # Each block is 18 lines
    if i % 18 == 0:
        if f:
            f.close()
        f = open('b' + str(i // 18 + 1) + '.txt', 'w')
    f.write(lines[i] + '\n')
f.close()
