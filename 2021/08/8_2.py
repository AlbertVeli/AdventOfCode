#!/usr/bin/env python3

import sys
sys.path.insert(0,'../')
from aoc_input import *
from itertools import permutations

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

a = input_as_lines(sys.argv[1])

lines = []
for line in a:
    lines.append(re.findall(r'([a-z]+)', line))

nums = ['abcefg', 'cf', 'acdeg', 'acdfg', 'bcdf', 'abdfg', 'abdefg', 'acf', 'abcdefg', 'abcdfg']
letters = 'abcdefg'

def check_permutation(p, line):
    scrambled = line[:10]
    d = dict(zip(letters, p))
    for word in scrambled:
        unscrambled = ''
        for i in range(len(word)):
            unscrambled += d[word[i]]
        unscrambled = ''.join(sorted(unscrambled))
        if not unscrambled in nums:
            return False
    return True

def unscramble(p, word):
    d = dict(zip(letters, p))
    unscrambled = ''
    for i in range(len(word)):
        unscrambled += d[word[i]]
    unscrambled = ''.join(sorted(unscrambled))
    return unscrambled

def decode_line(line):
    for p in permutations(letters):
        if check_permutation(p, line):
            # Yay, got the correct one
            num = ''
            for word in line[10:]:
                unscrambled = unscramble(p, word)
                num += str(nums.index(unscrambled))
            return int(num)

sm = 0
for line in lines:
    num = decode_line(line)
    print(num)
    sm += num
print(sm)
