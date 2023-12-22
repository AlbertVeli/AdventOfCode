#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc
from collections import deque
from functools import reduce
from operator import mul

modules = dict()

for line in aoc.lines(sys.argv[1]):
    module, targets = line.split(' -> ')
    targets = targets.split(', ')

    if module == 'broadcaster':
        modules[module] = { 'type': 'broadcast', 'destinations': targets }
    else:
        type = module[0]
        name = module[1:]
        if type == '%':
            # Init to low (False)
            modules[name] =  { 'type': 'flip-flop', 'state': False, 'destinations': targets }
        elif type == '&':
            # memory remembers last value for each input
            modules[name] = { 'type': 'conjunction', 'memory': {}, 'destinations': targets }

# Find output target
targets = set()
for name, module in modules.items():
    for destination in module['destinations']:
        targets.add(destination)
for name in targets:
    if not name in modules:
        # There is only one output target
        # in example.txt this is 'output', in input.txt it is 'rx'
        output = name
        modules[name] = {'type': 'output', 'destinations': []}

# Fill in conjunction module inputs
for name, module in modules.items():
    for destination in module['destinations']:
        if destination == output:
            continue
        dest_module = modules[destination]
        if dest_module['type'] == 'conjunction':
            # Init to low (False)
            dest_module['memory'][name] = False

def button_press(length):
    # one low is sent to broadcaster
    n_low  = 1
    n_high = 0

    signal_q = deque()
    bit_value = False

    # Start with broadcaster module
    for dest in modules['broadcaster']['destinations']:
        # (source, low or high, dest)
        signal_q.append(('broadcaster', bit_value, dest))

    while len(signal_q) > 0:
        source, bit_value, dest = signal_q.popleft()

        dest_module = modules[dest]

        n_high += int(bit_value)
        n_low  += int(not bit_value)

        if dest_module['type'] == 'output':
            continue

        # flip internal state and output if input is low
        if dest_module['type'] == 'flip-flop':
            if not bit_value:
                new_state = not dest_module['state']
                dest_module['state'] = new_state
                for dest_target in dest_module['destinations']:
                    signal_q.append((dest, new_state, dest_target))
        # Update internal memory
        elif dest_module['type'] == 'conjunction':
            memory = dest_module['memory']
            memory[source] = bit_value
            # If all memory bits are high, output False
            if all(element for element in memory.values()):
                new_bit_val = False
            else:
                # else True
                new_bit_val = True
                # This is only for part 2
                if dest in cycle_lengths.keys():
                    if cycle_lengths[dest] == False:
                        cycle_lengths[dest] = length

            # output to signal_q
            for dest_target in dest_module['destinations']:
                signal_q.append((dest, new_bit_val, dest_target))
    
    return (n_low, n_high)

# For part 2
cycle_lengths = dict()

n_low = 0
n_high = 0
for i in range(1000):
    new_low, new_high = button_press(i)

    n_low  += new_low
    n_high += new_high

print('Part 1:', n_low * n_high)

# part 2
def modules_which_has_target(target):
    mods = []
    for name, module in modules.items():
        for destination in module['destinations']:
            if target == destination:
                mods.append(name)
    return mods

# Only one module outputs to output
last_module = modules_which_has_target(output)[0]
input_last_modules = modules_which_has_target(last_module)
# My son tells me the cycle starts at offset 0
# and starts repeating after the first 1 value
for name in input_last_modules:
    # Init to False
    cycle_lengths[name] = False

# reset modules (init all to false) for part 2
for name, module in modules.items():
    typ = module['type']
    if typ == 'flip-flop':
        module['state'] = False
    elif typ == 'conjunction':
        memory = module['memory']
        for key in memory.keys():
            memory[key] = False

# The first state is the init state where
# everything is set to 0, so init length to 1
length = 1
while True:
    button_press(length)
    length += 1

    if all(value != False for value in cycle_lengths.values()):
        break

# Since all cycle_lengths are primes we only need to multiply them
# If they were not prime we could use lcm
print('Part 2:', reduce(mul, cycle_lengths.values()))