#!/usr/bin/env python3

import sys
sys.path.insert(0,'../')
from aoc_input import *
import re
import numpy as np

drawn = np.array([], int)

class Board:
    def __init__(self, lines):
        self.board = np.array(lines, int)

    def __str__(self):
        return(self.board.__str__())

    def win(self):
        # rows
        for row in self.board:
            mask = np.in1d(row, drawn)
            nmark = len(np.where(mask)[0])
            if nmark == 5:
                return True

        # cols
        for col in range(5):
            mask = np.in1d(self.board[:,col], drawn)
            nmark = len(np.where(mask)[0])
            if nmark == 5:
                return True

        return False

    def score(self, last_num):
        not_marked = []
        # numpy magic
        for row in self.board:
            mask = np.in1d(row, drawn)
            nm = list(row[np.where(~mask)[0]])
            for n in nm:
                not_marked.append(n)
        return sum(not_marked) * last_num

# Main
if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

a = input_as_lines(sys.argv[1])

nums = re.findall(r'([-+]?\d+)', a[0])
nums = list(map(int, nums))

boards = []
brd = []
lineno = 0
for line in a[1:]:
    if len(line) == 0:
        continue
    brd.append(re.findall(r'([-+]?\d+)', line))
    lineno += 1
    if lineno == 5:
        lineno = 0
        boards.append(Board(brd))
        brd = []

for num in nums:
    drawn = np.append(drawn, num)
    for board in boards:
        if board.win():
            #print(board)
            print(board.score(num))
            exit()
