#!/usr/bin/env python3

import sys

def parse_worksheet_file(filename: str):
    with open(filename, 'r') as f:
        lines = [line.rstrip() for line in f.readlines() if line.strip()]

    # Last line = operators
    op_line = lines[-1]
    num_lines = lines[:-1]

    # Parse number rows
    rows = [list(map(int, line.split())) for line in num_lines]
    ncols = len(rows[0])
    if any(len(r) != ncols for r in rows):
        raise ValueError('Inconsistent number of columns')

    # Parse operators
    ops = op_line.split()
    if len(ops) != ncols:
        raise ValueError('Mismatch between number of operators and columns')

    # Build only the column value lists
    columns_values = [
        [row[c] for row in rows]
        for c in range(ncols)
    ]

    return rows, ops, columns_values

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

rows, ops, columns = parse_worksheet_file(sys.argv[1])

p1 = 0
for i in range(len(ops)):
    n = calc_column(ops[i], columns[i])
    p1 += n
print('Part 1:', p1)
