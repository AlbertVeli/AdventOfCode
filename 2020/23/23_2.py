#!/usr/bin/env python3

from collections import deque
import sys

# My code was too slow to solve this in reasonable time.
# Keeping next cups in a dictionary was my son's idea.
# The get_left() function is stolen from his code.
after = dict()
def get_left():
    e = nums.popleft()
    # If leftmost element is in after
    # Move the corresponding pickup cups to
    # the beginning.
    if e in after:
        nums.extendleft(after[e][::-1])
        del after[e]
    return e

def move():
    current_cup = get_left()
    pickup = [get_left(), get_left(), get_left()]
    next_cup = current_cup - 1
    if next_cup == 0:
        next_cup = max_cup
    while next_cup in pickup:
        next_cup -= 1
        if next_cup == 0:
            next_cup = max_cup
    after[next_cup] = pickup
    nums.append(current_cup)

line = open(sys.argv[1]).readline().rstrip()
max_cup = 1000000
# input has numbers 1-9, extend with 10 to max_cup
nums = deque(list(map(int, list(line))) + list(range(10, max_cup + 1)))
# Print progress every 2^20th iteration
mask = (1 << 20) - 1
for mv in range(1, 10000001):
    if mv & mask == 0:
        print(mv)
    move()

# Rotate list until 1 is first
while True:
    n = get_left()
    if n == 1:
        break
    nums.append(n)

n1 = get_left()
n2 = get_left()

print('\n-- final --')
print(n1, n2)
print(n1 * n2)
