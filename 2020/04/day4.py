#!/usr/bin/env python3

import sys
import re
import typing
# For DBG. Replace all DBG with
# print to always print
sys.path.insert(0,'../common')
from dbg import DBG

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

def read_input(fname: str) -> typing.List[dict]:
    r = []
    d: dict = {}
    for line in open(fname).read().splitlines():
        a = line.rstrip().split()
        if len(a) == 0:
            if len(d) > 0:
                r.append(d)
                d = {}
        else:
            for b in a:
                c = b.split(':')
                d[c[0]] = c[1]
    # Last one, if no empty line at end
    if len(d) > 0:
        r.append(d)
    return r

def is_valid(d: dict, part1: bool) -> bool:

    DBG(d)

    # Part 1
    if len(d) != 8 and (len(d) < 7 or 'cid' in d):
        DBG('failed part 1 validation')
        return False

    if part1:
        DBG('valid, part 1')
        return True

    # Part 2
    if 'byr' in d:
        byr = int(d['byr'])
        if byr < 1920 or byr > 2020:
            DBG('byr', byr, 'invalid')
            return False
    else:
        DBG('byr not found')
        return False

    if 'iyr' in d:
        iyr = int(d['iyr'])
        if iyr < 2010 or iyr > 2020:
            DBG('iyr', iyr, 'invalid')
            return False
    else:
        DBG('iyr not found')
        return False

    if 'eyr' in d:
        eyr = int(d['eyr'])
        if eyr < 2020 or eyr > 2030:
            DBG('eyr', eyr, 'invalid')
            return False
    else:
        DBG('eyr not found')
        return False

    if 'hgt' in d:
        hgt = d['hgt']
        if 'in' in hgt:
            hgt = hgt.replace('in', '')
            if len(hgt) == 0:
                DBG('hgt empty')
                return False
            hgt = int(hgt)
            if hgt < 59 or hgt > 76:
                DBG('hgt', hgt, 'invalid')
                return False
        elif 'cm' in hgt:
            hgt = hgt.replace('cm', '')
            if len(hgt) == 0:
                DBG('hgt empty')
                return False
            hgt = int(hgt)
            if hgt < 150 or hgt > 193:
                DBG('hgt', hgt, 'invalid')
                return False
        else:
            DBG('neither in nor cm found')
            return False
    else:
        DBG('hgt not found')
        return False

    if 'hcl' in d:
        hcl = d['hcl']
        if re.search(r'^#[0-9a-f]{6}$', hcl) == None:
            DBG('hcl regex', hcl, 'invalid')
            return False
    else:
        DBG('hcl not found')
        return False

    if 'ecl' in d:
        ecl = d['ecl']
        if (ecl != 'amb') and (ecl != 'blu') and \
        (ecl != 'brn') and (ecl != 'gry') and \
        (ecl != 'grn') and (ecl != 'hzl') and (ecl != 'oth'):
            DBG('ecl', ecl, 'invalid')
            return False
    else:
        DBG('ecl not found')
        return False

    if 'pid' in d:
        pid = d['pid']
        if re.search(r'^[0-9]{9}$', pid) == None:
            DBG('pid regex', pid, 'invalid')
            return False
    else:
        DBG('pid not found')
        return False

    DBG('valid')
    return True

a = read_input(sys.argv[1])

# part 1
valid1 = 0
for d in a:
    if is_valid(d, True):
        valid1 += 1

# part 2
valid2 = 0
for d in a:
    if is_valid(d, False):
        valid2 += 1

print(valid1)
print(valid2)
