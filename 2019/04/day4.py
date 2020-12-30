#!/usr/bin/env python3

import sys
import re

double_re = re.compile(r'.*(\d)\1')

def passfilters1(s):
    # Not decreasing
    for i in range(5):
        if s[i] > s[i + 1]:
            return False

    # At least one double
    return re.match(double_re, s) != None


def passfilters2(s):
    # Not decreasing
    for i in range(5):
        if s[i] > s[i + 1]:
            return False

    # At least one exactly double
    # This could probably be written much shorter
    same = 1
    last = s[0]
    for i in range(1, 6):
        c = s[i]
        if c == last:
            same += 1
        else:
            if same == 2:
                return True
            same = 1
        last = c
    if same == 2:
        return True

    return False


a, b = map(int, open(sys.argv[1]).readline().split('-'))

print('Part 1:', sum([passfilters1(str(i)) for i in range(a, b + 1)]))
print('Part 2:', sum([passfilters2(str(i)) for i in range(a, b + 1)]))
