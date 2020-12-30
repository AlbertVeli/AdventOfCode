#!/usr/bin/env python3

from collections import deque
import sys

def print_cups(dq, curr, pickup, dest):
    print('\n-- move', mv, ' --')
    sys.stdout.write('cups: (' + str(curr) + ') ')
    for i in range(3):
        sys.stdout.write(str(pickup[i]) + ' ')

    for i, n in enumerate(dq):
        sys.stdout.write(str(n) + ' ')
    sys.stdout.write('\n')
    print('pick up:', pickup)
    print('destination:', dest)

def move(dq):
    current_cup = dq.popleft()
    pickup = [dq.popleft(), dq.popleft(), dq.popleft()]
    next_cup = current_cup - 1
    if next_cup == 0:
        next_cup = max_cup
    while next_cup in pickup:
        next_cup -= 1
        if next_cup == 0:
            next_cup = max_cup
    print(next_cup)
    print_cups(dq, current_cup, pickup, next_cup)
    dq.append(current_cup)
    i = dq.index(next_cup) + 1
    pickup.reverse()
    for n in pickup:
        dq.insert(i, n)

line = open(sys.argv[1]).readline().rstrip()
nums = deque(map(int, list(line)))
mv = 1
max_cup = max(nums)

for mv in range(1, 101):
    move(nums)
print('\n-- final --')
print(nums)
ix = nums.index(1)
l = len(nums)
for i in range(1, l):
    sys.stdout.write(str(nums[(i + ix) % l]))
sys.stdout.write('\n')
