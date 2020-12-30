#!/usr/bin/env python3

import sys

# --- globals ---

# [(output chemical), [(input chemical 1), (input chemical 2), ...]]
reactions = []

# Chemicals in storage after production
storage = {}

# part 2, begin with many orens, produce as much fuel as possible
startorens = 1000000000000
orens = startorens

def reset():
    global storage, orens
    storage = {}
    orens = startorens

# --- input ---

for line in sys.stdin:
    l, r = line.rstrip().split('=>')
    quant, chem = r.strip().split()
    # only one reaction produce each chemical
    ochem = (chem, int(quant))
    ichem = []
    if ',' in l:
        for r in l.split(','):
            q, c = r.strip().split()
            ichem.append((c, int(q)))
    else:
        q, c = l.split()
        ichem.append((c, int(q)))
    reactions.append([ochem, ichem])

# --- functions ---

# Return reaction to produce chem
def reaction(chem):
    for r in reactions:
        rc = r[0][0]
        if rc == chem:
            return r
    print('Error: no reaction exists for chemical', chem)
    exit(0)

# How many of chem do we have in storage?
def num_in_storage(chem):
    global storage
    if chem in storage:
        return storage[chem]
    return 0

# Store or take out from storage.
# Caller must not take out more than available,
# storage[chem] should not be negative after update.
def update_storage(chem, n):
    global storage
    if chem in storage:
        #print('DBG: changing storage for', chem, 'with', n, 'items')
        storage[chem] += n
    else:
        #print('DBG: storing', n, 'items of', chem)
        storage[chem] = n

# Store reactions too. Not really necessary.
# [reaction, quantity]
productions = []
def store_production(r, n):
    global productions
    found = False
    for i in range(len(productions)):
        p = productions[i]
        if p[0] == r:
            #print('DBG: add', n, r, 'total:', n + p[1])
            p[1] += n
            return None
    # r not found in productions
    #print('DBG: add', n, r)
    productions.append([r, n])

def produce(chem, quantity):
    global orens, fuel

    if orens < 0:
        return False

    # not possible to produce ORE, just
    # store how many needs to be mined
    if chem == 'ORE':
        # Here part 2 is different to part 1
        orens -= quantity
        return False

    r = reaction(chem)
    # One reaction produces rq chems
    rq = r[0][1]
    ns = num_in_storage(chem)
    if ns >= quantity:
        # No new reaction needed
        update_storage(chem, -quantity)
        return False

    # At least one reaction needed
    rs = (quantity - ns) // rq
    extra = (quantity - ns) % rq
    if extra != 0:
        rs += 1
    store_production(r, rs)
    # produced rs * rq items and consumed quantity items
    update_storage(chem, rs * rq - quantity)
    # continue to recursively produce needed chemicals
    # recursion will stop with orens
    for c in r[1]:
        # print('DBG: need to also produce', c)
        produce(c[0], rs * c[1])
    return True

# Can we produce n fuels?
def can_produce(n):
    reset()
    produce('FUEL', n)
    if orens < 0:
        return False
    return True

# --- main ---

# Produce 1 fuel and calculate start value for bisection
produce('FUEL', 1)
onecost = startorens - orens
try_n = startorens // onecost
if can_produce(try_n):
    bisect_min = try_n
else:
    print('bisect_min failed, check code')
    exit(0)

# Max value for bisection, change this if too small
try_n = try_n * 2
if not can_produce(try_n):
    bisect_max = try_n
else:
    print('bisect_max too small, use bigger start value')
    exit(0)

# Bisect to find value where can_produce starts to give False
while bisect_max - bisect_min > 1:
    try_n = bisect_min + (bisect_max - bisect_min) // 2
    if can_produce(try_n):
        bisect_min = try_n
    else:
        bisect_max = try_n

# last working value for try_n should be bisect_min
print(bisect_min, bisect_max)

