#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc
import re
from collections import Counter, defaultdict
from string import ascii_lowercase

def parse_line(line):
    g = re.match(r'([a-z]+(?:-[a-z]+)*)-(\d+)(\[[a-z]+\])', line).groups()
    return [g[0], int(g[1]), g[2][1:-1]]

def common(s):
    c = Counter(s.replace('-', ''))
    d = defaultdict(list)
    for letter, count in c.most_common():
        d[count].append(letter)
    r = ''
    for count, letters in d.items():
        r = r + ''.join(sorted(letters))
    return r[:5]

def is_real(room):
    return common(room[0]) == room[2]

rooms = []
for line in aoc.lines(sys.argv[1]):
    rooms.append(parse_line(line))

sm = 0
for room in rooms:
    if is_real(room):
        sm += room[1]
print('part 1:', sm)

# part 2, caesar shift rooms
def caesar(s, r):
    ciph = bytearray(26)
    a = ord('a')
    offs = r - a
    i = 0
    for c in ascii_lowercase:
        ciph[i] = (ord(c) + offs) % 26 + a
        i += 1
    t = str.maketrans(ascii_lowercase, ciph.decode('ascii'))
    return s.translate(t)

for room in rooms:
    if caesar(room[0], room[1]) == 'northpole-object-storage':
        print('part 2:', room[1])