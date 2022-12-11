#!/usr/bin/env python3

import sys
import fileinput
import re

def do_op(old, op):
    return eval(op)

class Monkey:
    def __init__(self, m_id, items, op, test, if_t, if_f):
        self.m_id = m_id
        self.items = items
        self.op = op
        self.test = test
        self.if_t = if_t
        self.if_f = if_f
        self.num_inspected = 0

    def __str__(self):
        s  = 'Monkey ' + str(self.m_id) + '\n'
        s += '  items: ' + str(self.items) + '\n'
        s += '  op: ' + self.op + '\n'
        s += '  divisibly by: ' + str(self.test) + '\n'
        s += '  if true: ' + str(self.if_t) + '\n'
        s += '  if false: ' + str(self.if_f) + '\n'
        s += '  inspected: ' + str(self.num_inspected) + '\n'
        return s

    def fetch(self, item):
        self.items.append(item)

    def inspect_items(self):
        for item in self.items:
            # This is not obvious, but to find out if
            # item % self.test will be true or false it
            # is enough to store the item worry levels
            # % the product of all test values multiplied
            # together.
            item = do_op(item, self.op) % tests_prod
            if item % self.test == 0:
                monkeys[self.if_t].fetch(item)
            else:
                monkeys[self.if_f].fetch(item)
            self.num_inspected += 1
        self.items = []

monkeys = []
tests = []
# All divisors are unique primes so
# multiplying them will lead to the
# same result as lcm.
tests_prod = 1
a = open(sys.argv[1]).read().rstrip().split('\n\n')
for monkey in a:
    lines = monkey.split('\n')
    m_id = list(map(int, re.findall(r'(\d+)', lines[0])))[0]
    starting = list(map(int, re.findall(r'(\d+)', lines[1])))
    op = lines[2].split('= ')[1]
    test = int(lines[3].split('divisible by ')[1])
    if_t = int(lines[4].split(' throw to monkey ')[1])
    if_f = int(lines[5].split(' throw to monkey ')[1])
    monkeys.append(Monkey(m_id, starting, op, test, if_t, if_f))
    tests.append(test)
    tests_prod *= test

for _ in range(10000):
    for m in monkeys:
        m.inspect_items()

a = []
for m in monkeys:
    a.append(m.num_inspected)
a.sort(reverse = True)
print(a[0] * a[1])
