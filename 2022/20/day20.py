#!/usr/bin/env python3

import sys

ints = list(map(int, open(sys.argv[1]).read().rstrip().split('\n')))
nints = len(ints)
# list of indexes (unique elements), only change this list
ixs = list(range(nints))

# Move index i n steps forward
# in ixs where n is ints[i]
def move_ixs(i):
    n = ints[i]
    # indexes are unique
    old_ix = ixs.index(i)
    # pop ix from ixs (should be same as i)
    ix = ixs.pop(old_ix)
    #assert ix == i, 'index error in move_ixs'
    # insert it at new_ix (old index + n)
    new_ix = (old_ix + n) % (nints - 1)
    ixs.insert(new_ix, ix)

def print_ints():
    for i in ixs:
        sys.stdout.write(str(ints[i]) + ', ')
    print('')
    print(ixs)

def get_answer():
    ix0 = ixs.index(ints.index(0))
    ix1 = ixs[(ix0 + 1000) % nints]
    ix2 = ixs[(ix0 + 2000) % nints]
    ix3 = ixs[(ix0 + 3000) % nints]
    return sum([ints[ix1], ints[ix2], ints[ix3]])

print('start state')
#print_ints()
for i in range(nints):
    move_ixs(i)
    #print(f'round {i + 1}')
    #print_ints()

# Find answer
ans = get_answer()
print('Part 1:', ans)

# Part 2
for i in range(nints):
    ints[i] *= 811589153
ixs = list(range(nints))
#print_ints()
for mix in range(10):
    for i in range(nints):
        move_ixs(i)
    #print(f'round {i + 1}')
    #print_ints()

ans = get_answer()
print('Part 2:', ans)

# ints and ixs for the given example:
# 1, 2, -3, 3, -2, 0, 4
# 0  1   2  3   4  5  6
#
# 1 moves between 2 and -3:
# 2, 1, -3, 3, -2, 0, 4
# 1  0   2  3   4  5  6
#
# 2 moves between -3 and 3:
# 1, -3, 2, 3, -2, 0, 4
# 0   2  1  3   4  5  6
#
# -3 moves between -2 and 0:
# 1, 2, 3, -2, -3, 0, 4
# 0  1  3   4   2  5  6
#
# 3 moves between 0 and 4:
# 1, 2, -2, -3, 0, 3, 4
# 0  1   4   2  5  3  6
#
# -2 moves between 4 and 1:
# 1, 2, -3, 0, 3, 4, -2
# 0  1   2  5  3  6   4

# 0 does not move:
# 1, 2, -3, 0, 3, 4, -2
# 0  1   2  5  3  6   4
#
# 4 moves between -3 and 0:
# 1, 2, -3, 4, 0, 3, -2
# 0  1   2  6  5  3   4
