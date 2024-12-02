#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc

data = aoc.lines_of_ints(sys.argv[1])

def is_safe(report):
    inc = report[1] > report[0]

    for i in range(1, len(report)):
        diff = abs(report[i] - report[i - 1])

        if diff < 1 or diff > 3:
            return False

        if inc and report[i] < report[i - 1]:
            return False

        if (not inc) and report[i] > report[i - 1]:
            return False

    return True

# Part 1
result = 0
for report in data:
    safe = is_safe(report)
    #print(report, safe)
    if safe:
        result += 1

print("Part 1:", result)

# Part 2
result = 0
for report in data:
    safe = is_safe(report)
    if not safe:
        for i in range(len(report)):
            # Remove one level
            modified_report = report[:i] + report[i+1:]
            if is_safe(modified_report):
                safe = True
                break
    #print(report, safe)
    if safe:
        result += 1

print("Part 2:", result)
