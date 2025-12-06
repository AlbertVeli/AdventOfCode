#!/usr/bin/env python3

import sys

def read_grid(filename: str) -> list[str]:
    '''Read all non-empty lines (including the operator line) as strings.'''
    with open(filename, 'r') as f:
        return [line.rstrip('\n') for line in f if line.strip()]

def transpose_and_group(lines: list[str]) -> list[list[str]]:
    '''
    Transpose the whole grid and split into groups on blank columns.

    Returns a list of groups, where each group is a list of column-strings,
    e.g. ['623+', '431 ', '  4 '] for one 'problem'.
    '''
    width = max(len(line) for line in lines)
    grid = [line.ljust(width) for line in lines]
    height = len(grid)

    # Transpose: each entry is a full vertical column as a string
    cols = [''.join(grid[r][c] for r in range(height)) for c in range(width)]

    groups = []
    current = []
    for col in cols:
        if col.strip() == '':          # blank column = separator
            if current:
                groups.append(current)
                current = []
        else:
            current.append(col)
    if current:
        groups.append(current)

    return groups

def group_to_part2_numbers(group: list[str]) -> list[int]:
    '''
    From one group of column-strings (left→right), build the part-2 numbers:
    read columns right→left, digits top→bottom.

    Example group: ['623+', '431 ', '  4 ']
    → [4, 431, 623]
    '''
    nums = []
    for col in reversed(group):  # rightmost to leftmost
        digits = ''.join(ch for ch in col if ch.isdigit())
        if digits:
            nums.append(int(digits))
    return nums

def group_to_operator(group: list[str]) -> str:
    '''
    Infer the operator ('+' or '*') from a group by scanning for it.
    Assumes exactly one operator per group (at the bottom row).
    '''
    ops = {ch for col in group for ch in col if ch in '+*'}
    if len(ops) != 1:
        raise ValueError(f'Ambiguous operators in group: {ops}')
    return ops.pop()

def parse_part2(filename: str):
    '''
    Return (ops_part2, cols_part2) where:
      - ops_part2 is a list of '+'/'*' per problem
      - cols_part2 is a list of lists of ints (the transposed numbers)
    '''
    lines = read_grid(filename)
    groups = transpose_and_group(lines)

    ops_part2 = []
    cols_part2 = []
    for g in groups:
        ops_part2.append(group_to_operator(g))
        cols_part2.append(group_to_part2_numbers(g))

    return ops_part2, cols_part2

def calc_column(op, values):
    '''Compute the result of one column.'''
    if op == '+':
        total = 0
        for v in values:
            total += v
        return total
    elif op == '*':
        total = 1
        for v in values:
            total *= v
        return total
    else:
        raise ValueError(f'Unknown operator: {op}')

ops, cols = parse_part2(sys.argv[1])

p2 = 0
for i in range(len(ops)):
    n = calc_column(ops[i], cols[i])
    p2 += n
print('Part 2:', p2)
