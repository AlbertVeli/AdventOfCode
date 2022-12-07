#!/usr/bin/env python3

import sys
from collections import defaultdict
import os

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

def def_value():
    return 0

# cwd + filename : filesize
files = defaultdict(def_value)
files['/'] = 0
cwd = '/'
dirs = set()

# Disk usage of directory d and subdirs
def du(d):
    total = 0
    for f, sz in files.items():
        if f.startswith(d):
            total += sz
    return total

# Change directory
# TODO: Clean up this function
def cd(d):
    global cwd

    if d == '/':
        # cd /
        cwd = '/'
    elif d == '..':
        # cd ..
        if cwd == '/':
            return None
        cwd = '/'.join(cwd.split('/')[:-1])
    else:
        # cd <dir>
        cwd = '/'.join([cwd, d])

    # Fixes because of stupid handling of rootdir '/' above
    if cwd.startswith('//'):
        cwd = cwd[1:]
    if cwd == '':
        cwd = '/'
    dirs.add(cwd)

# Add file in current directory
def add_file(line):
    global files

    sz, name = line.split(' ')
    if not sz.isdecimal():
        print('Error:', line, 'is not a file')
        sys.exit(1)
    if cwd == '/':
        path = cwd + name
    else:
        path = cwd + '/' + name
    files[path] = int(sz)

def parseline(line):
    global disk
    global cwd
    if line.startswith('$ cd '):
        cd(line.split('$ cd ')[1])
    elif line.startswith('dir '):
        # ignore directories, just assume they exist
        return None
    elif line.startswith('$ ls'):
        # ignore ls, assume lines starting with numbers are files
        return None
    else:
        add_file(line)

lines = open(sys.argv[1]).read().rstrip().split('\n')
for line in lines:
    parseline(line)

#print(sorted(list(dirs)))

# Part 1
total = 0
sizes = dict()
for d in dirs:
    #print(d, du(d))
    sz = du(d)
    sizes[d] = sz
    if sz <= 100000:
        total += sz
print('Part 1', total)

total = 70000000
used = sizes['/']
need_to_free = 30000000 - (total - used)
best = sys.maxsize
for d, sz in sizes.items():
    i = sz - need_to_free
    if i >= 0 and i < best:
        best = i
        bestsize = sz
print('Part 2', bestsize)
