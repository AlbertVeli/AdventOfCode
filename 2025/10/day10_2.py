#!/usr/bin/env python3

import sys
import re

# Import PuLP for integer linear programming
# This was suggested by ChatGPT and it also
# helped to write the min_presses pulp code.
from pulp import (LpProblem, LpMinimize, LpVariable, lpSum, PULP_CBC_CMD, value)

# Regexes for the parts of each line
INDICATOR_RE = re.compile(r'\[([.#]+)\]')   # ignored in part 2
BUTTON_RE    = re.compile(r'\(([^)]*)\)')
JOLTAGE_RE   = re.compile(r'\{([^}]*)\}')

class Machine:
    """
    One factory machine for PART 2 (joltage mode).

    num_counters: number of joltage counters
    targets:      list of required joltage levels for each counter
    buttons:      list of buttons; each is a list of counter indices it increments
    """

    def __init__(self, line):
        line = line.strip()

        # Parse joltage requirements: {3,5,4,7}
        m = JOLTAGE_RE.search(line)
        self.targets = [int(x) for x in m.group(1).split(',')]
        self.num_counters = len(self.targets)

        # Parse buttons: (0,2,3) (1,3) ...
        self.buttons = []
        for bmatch in BUTTON_RE.finditer(line):
            contents = bmatch.group(1).strip()
            self.buttons.append([int(x) for x in contents.split(',')])

    def min_presses(self):
        """
        Solve:
            minimize sum_i x_i
        subject to:
            for each counter j: sum_{i: j in button_i} x_i = targets[j]
            x_i >= 0, integer
        """
        num_buttons = len(self.buttons)

        prob = LpProblem('machine', LpMinimize)

        # x_i: number of times button i is pressed
        x_vars = [
            LpVariable(f'x_{i}', lowBound=0, cat='Integer')
            for i in range(num_buttons)
        ]

        # Objective: minimize total presses
        prob += lpSum(x_vars)

        # Constraints: for each counter j, exact target value
        for j in range(self.num_counters):
            prob += (
                lpSum(
                    x_vars[i]
                    for i, btn in enumerate(self.buttons)
                    if j in btn
                )
                == self.targets[j],
                f'counter_{j}',
            )

        # Solve with CBC, no solver output
        # should return optimal for valid AoC input
        # skip error checking
        prob.solve(PULP_CBC_CMD(msg=False))

        # Total presses from optimized variables
        total_presses = int(round(value(prob.objective)))
        return total_presses

# main

machines = []
with open(sys.argv[1], 'r') as f:
    for raw_line in f:
        line = raw_line.strip()
        if not line:
            continue
        machines.append(Machine(line))

total = 0
for m in machines:
    total += m.min_presses()

print('Part 2:', total)
