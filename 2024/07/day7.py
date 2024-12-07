#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc
from itertools import product

def eval_expr(a, b, op):
        if op == '+':
            return a + b
        elif op == '*':
            return a * b
        elif op == '||':
            return int(str(a) + str(b))

def evaluate(values, target, operators):

    if not values or len(values) < 2:
        return False

    # Generate all combinations of operators
    for ops in product(operators, repeat=len(values) - 1):

        result = values[0]

        # Apply each operator in sequence
        for num, op in zip(values[1:], ops):
            result = eval_expr(result, num, op)

        if result == target:
            return result

    return 0

# Main

eqs = aoc.lines_of_ints(sys.argv[1])

# Part 1
result = 0
operators = ['+', '*']
for line in eqs:
    result += evaluate(line[1:], line[0], operators)
print('Part 1:', result)

# Part 2
result = 0
operators = ['+', '*', '||']
for line in eqs:
    result += evaluate(line[1:], line[0], operators)
print('Part 2:', result)
