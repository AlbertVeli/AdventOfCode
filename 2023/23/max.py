# script to collect output steps for different paths
# and print out the max ones, for running many instances
# of day23.py in parallell and outputting to separate files
vals = []
files = ['a.txt', 'b.txt', 'c.txt', 'd.txt']
for filename in files:
    for line in open(filename).readlines():
        line = line.rstrip()
        if not 'Part' in line:
            val = int(line)
            if not val in vals:
                vals.append(int(line))

print(max(vals))
