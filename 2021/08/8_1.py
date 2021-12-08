#!/usr/bin/env python3

import sys
sys.path.insert(0,'../')
from aoc_input import *

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

a = input_as_lines(sys.argv[1])
#a = input_as_line_of_ints(sys.argv[1])
#a = input_as_ints(sys.argv[1])

lines = []
for line in a:
    lines.append(re.findall(r'([a-z]+)', line))

# lens -> digit
# 2 -> 1
# 3 -> 7
# 4 -> 4
# 7 -> 8
unique_lens = {2, 3, 4, 7}
num_unique = 0
for line in lines:
    lens = []
    for i in range(10, 14):
        l = len(line[i])
        if l in unique_lens:
            num_unique += 1
print(num_unique)
