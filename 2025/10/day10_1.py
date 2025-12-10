#!/usr/bin/env python3

import sys
import re
from itertools import combinations

# Regexes for the three parts of each line
INDICATOR_RE = re.compile(r'\[([.#]+)\]')
BUTTON_RE    = re.compile(r'\(([^)]*)\)')
JOLTAGE_RE   = re.compile(r'\{([^}]*)\}')

class Machine:
    """
    One factory machine configuration
    num_lights: Number of indicator lights
    target_mask: Bitmask of target light pattern
    button_masks: List of bitmasks for each button
    """

    def __init__(self, line):
        """Parse a single input line into a Machine instance."""
        line = line.strip()

        # Indicator pattern: [.##..#...]
        m = INDICATOR_RE.search(line)
        pattern = m.group(1)
        self.num_lights = len(pattern)

        # Build target bitmask from pattern (# = 1, . = 0)
        self.target_mask = int(pattern.replace('.', '0').replace('#', '1'), 2)

        # Buttons: (0,2,3) (1,4,5) ...
        self.button_masks = []
        for bmatch in BUTTON_RE.finditer(line):
            contents = bmatch.group(1).strip()
            if not contents:
                # Empty button: toggles nothing
                self.button_masks.append(0)
                continue

            indices = [int(x) for x in contents.split(',')]
            mask = 0
            for idx in indices:
                bit = (self.num_lights - 1) - idx
                mask |= (1 << bit)
            self.button_masks.append(mask)

        # TODO: Parse joltages
        return

    def min_presses(self):
        """
        Compute the minimum number of button presses to
        reach the target pattern. Test all combinations
        of buttons starting from 1. Return the first
        number of presses that achieves the target, this
        will be the minimum.
        """
        n = len(self.button_masks)
        for n_buttons in range(n + 1):
            for c in combinations(range(n), n_buttons):
                mask = 0
                for mask_n in c:
                    mask ^= self.button_masks[mask_n]
                    if mask == self.target_mask:
                        #print(f'  Found with buttons {c}, total presses {n_buttons}')
                        return n_buttons
        print(f'No combination to reach target pattern {self.target_mask}')
        return None

def mask_to_bits(mask, n):
    bits = []
    for i in range(n - 1, -1, -1):   # MSB -> LSB
        bits.append('#' if (mask >> i) & 1 else '.')
    return ''.join(bits)

# main

with open(sys.argv[1], 'r') as f:
    machines = []
    for raw_line in f:
        line = raw_line.strip()
        if not line:
            continue
        machines.append(Machine(line))

p1 = 0
for i, m in enumerate(machines):
    #print(f'Machine {i}:')
    #print(f'  Lights: {m.num_lights}')
    #print(f'  Target: {mask_to_bits(m.target_mask, m.num_lights)}, ({m.target_mask})')
    #print(f'  Buttons:')
    #for j, bmask in enumerate(m.button_masks):
    #    print(f'    {j}: {mask_to_bits(bmask, m.num_lights)}, ({bmask})')
    p1 += m.min_presses()
print('Part 1:', p1)
