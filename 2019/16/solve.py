#!/usr/bin/env python3

import numpy as np
import sys

basepat = [0, 1, 0, -1]
def pattern(level):
    global length
    pat = []
    for i in range(length + 1):
        pat.append(basepat[(i // level) % 4])
    # Remove first element
    del(pat[0])
    return pat

def phase(signal):
    global length
    newsignal = []
    for l in range(1, length + 1):
        pat = np.array(pattern(l), dtype = np.int64)
        digit = abs(sum(signal * pat)) % 10
        newsignal.append(digit)
    return np.array(newsignal, dtype = np.int64)

def part1(signal, loops):
    for _ in range(loops):
        signal = phase(signal)
    # return 8 first digits
    return signal[:8]

# Full disclosure. Couldn't figure out the algorithm for part2
# myself so I peeked here to get the shortcut algorithm:
# https://www.reddit.com/r/adventofcode/comments/ebai4g/2019_day_16_solutions/
def part2(signal, loops):
    global length
    for _ in range(loops):
        for i in range(length - 2, -1, -1):
            signal[i] = (signal[i] + signal[i + 1]) % 10
    return signal[:8]

def printans(ans):
    for i in ans:
        sys.stdout.write(str(i))
    print('')

line = input('')
signal = np.array([int(c) for c in line], dtype = np.int64)
length = len(signal)

# Part 1
ans = part1(signal, 100)
printans(ans)

# Part 2
offset = int(line[:7])
signal = np.tile(signal, 10000)[offset:]
length = len(signal)
ans = part2(signal, 100)
printans(ans)
