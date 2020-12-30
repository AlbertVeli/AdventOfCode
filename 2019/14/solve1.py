#!/usr/bin/env python3

import sys

# --- globals ---

# [(output chemical), [(input chemical 1), (input chemical 2), ...]]
reactions = []

# Chemicals in storage after production
storage = {}
# ores treated special, can't be produced by reaction
ores = 0

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
    global ores
    # not possible to produce ORE, just
    # store how many needs to be mined
    if chem == 'ORE':
        ores += quantity
        return None

    r = reaction(chem)
    # One reaction produces rq chems
    rq = r[0][1]
    ns = num_in_storage(chem)
    if ns >= quantity:
        # No new reaction needed
        update_storage(chem, -quantity)
        return None

    # At least one reaction needed
    rs = (quantity - ns) // rq
    extra = (quantity - ns) % rq
    if extra != 0:
        rs += 1
    store_production(r, rs)
    # produced rs * rq items and consumed quantity items
    update_storage(chem, rs * rq - quantity)
    # continue to recursively produce needed chemicals
    # recursion will stop with ores
    for c in r[1]:
        # print('DBG: need to also produce', c)
        produce(c[0], rs * c[1])

# --- main ---

produce('FUEL', 1)
for p in productions:
    print(p)

print(ores)
