#!/usr/bin/env python3

import sys
from pathlib import Path

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

# cwd + filename : filesize
files = dict()
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
def cd(d):
    global cwd

    if d == '/':
        # cd /
        cwd = '/'
    elif d == '..':
        # cd ..
        p = Path(cwd)
        cwd = str(p.parent)
    else:
        # cd <dir>
        cwd = cwd + '/' + d
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

# Part 2
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
