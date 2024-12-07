#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc
from itertools import product

def get_ops(length):
    """
    Generate combinations of operators for given length
    cache results for faster lookup.
    globals: operator_cache, operators
    """
    if length not in operator_cache:
        # Number of operators is length - 1
        # ie. 3 numbers, 2 operators
        operator_cache[length] = list(product(operators, repeat=length - 1))
    return operator_cache[length]

# Use lambda to evaluate expressions
# for faster execution
eval_expr = lambda a, b, op: (
        a + b if op == '+' else
        a * b if op == '*' else
        # '||'
        int(str(a) + str(b))
)

def evaluate(values, target):
    """
    Evaluate using all possible combinations of operators
    and check if any of them match the target.
    globals: operators
    """

    length = len(values)

    if not values or length < 2:
        return False

    # Generate all combinations of operators
    for ops in get_ops(length):

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
operator_cache = {}
for line in eqs:
    result += evaluate(line[1:], line[0])
print('Part 1:', result)

# Part 2
result = 0
operators = ['+', '*', '||']
operator_cache = {}
for line in eqs:
    result += evaluate(line[1:], line[0])
print('Part 2:', result)
