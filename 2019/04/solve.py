#!/usr/bin/env python3

# quick hack. This whole solution could be much improved.

doubles = ['00', '11', '22', '33', '44', '55', '66', '77', '88', '99']

def passfilters1(s):
    # Not decreasing
    for i in range(5):
        if s[i] > s[i + 1]:
            return False

    # At least one double
    for i in range(int(s[0]), 10):
        ss = doubles[i]
        if ss in s:
            return True

    return False

def passfilters2(s):
    # Not decreasing
    for i in range(5):
        if s[i] > s[i + 1]:
            return False

    # At least one exactly double
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


a, b = map(int, input('').split('-'))

p = 0
for i in range(a, b):
    # Change to passfilters1 for task 1
    if passfilters2(str(i)):
        p += 1
print(p)
