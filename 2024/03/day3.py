#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc
import re

def process_line(line):
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    matches = re.findall(pattern, line)

    result = 0
    for x, y in matches:
        #print(f"{x} * {y} = {int(x) * int(y)}")
        result += int(x) * int(y)
    #print(f"Result: {result}")
    return result

def process_line2(corrupted_line):
    global enabled

    pattern = r"(mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\))"
    matches = re.findall(pattern, corrupted_line)

    # Process each match sequentially
    result = 0
    for match in matches:
        full_match = match[0]
 
        if full_match.startswith("do()"):
            enabled = True
        elif full_match.startswith("don't()"):
            enabled = False
        elif full_match.startswith("mul("):
            if enabled:
                x, y = int(match[1]), int(match[2])
                result += x * y

    return result

data = aoc.lines(sys.argv[1])
result = 0
for line in data:
    result += process_line(line)
print("Part 1", result)

result = 0
enabled = True
for line in data:
    result += process_line2(line)
print("Part 2", result)
