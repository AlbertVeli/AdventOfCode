#!/usr/bin/env python3

import sys

def parse_variables(lines):
    n_vars = {'x': set(), 'y': set(), 'z': set()}
    for line in lines:
        if ':' in line:
            var, _ = line.split(': ')
            first_char = var[0]
            if first_char in 'xy':
                n_vars[first_char].add(var)
    return n_vars

def parse_gates(lines):
    """
    Parse gates and return sets of variables for each type of gate.
    """
    xyadd, xycarry = set(), set()
    carries, ands, outs = set(), set(), set()
    carries_rows, outs_rows = set(), set()
    wrong_registers = set()

    for line in lines:
        if '->' not in line:
            continue

        inp, outp = line.split(' -> ')
        v1, op, v2 = inp.split(' ')

        if v1[0] in 'xy' or v2[0] in 'xy':
            if op == 'AND':
                # Special case for first carry
                if v1 == 'x00' and v2 == 'y00':
                    continue
                xycarry.add(outp)
            elif op == 'XOR':
                if outp[0] == 'z' and outp != 'z00':
                    wrong_registers.add(outp)
                if outp != 'z00':
                    xyadd.add(outp)
        else:
            if op == 'AND':
                ands.add(outp)
            elif op == 'OR':
                carries.add(outp)
                carries_rows.add((v1, v2, outp))
            elif op == 'XOR':
                # Ensure XOR outputs only to z variables
                if outp[0] != 'z':
                    wrong_registers.add(outp)
                outs.add(outp)
                outs_rows.add((v1, v2, outp))

        # Validate z variables
        if outp[0] == 'z':
            if op != 'XOR' and not (outp == 'z45' and op == 'OR'):
                wrong_registers.add(outp)

    return xyadd, xycarry, carries, ands, outs, carries_rows, outs_rows, wrong_registers

def validate_carries(xycarry, carries_rows, wrong_registers):
    """
    Validate that xycarry variables appear in carry rows.
    """
    for carry in xycarry:
        valid = any(carry == v1 or carry == v2 for (v1, v2, _) in carries_rows)
        if not valid:
            wrong_registers.add(carry)

def validate_adds(xyadd, outs_rows, wrong_registers):
    """
    Validate that xyadd variables appear in output rows.
    """
    for add in xyadd:
        valid = any(add == v1 or add == v2 for (v1, v2, _) in outs_rows)
        if not valid:
            wrong_registers.add(add)

# Main

# Read input from the file
with open(sys.argv[1], 'r') as f:
    input_text = f.read()
lines = input_text.strip().split('\n')

# Parse input
n_vars = parse_variables(lines)
xyadd, xycarry, carries, ands, outs, carries_rows, outs_rows, wrong_registers = parse_gates(lines)

# Validate carry and add variables
validate_carries(xycarry, carries_rows, wrong_registers)
validate_adds(xyadd, outs_rows, wrong_registers)

# Output sorted list of wrong registers
print('Part 2:', ','.join(sorted(wrong_registers)))
