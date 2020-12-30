#!/usr/bin/env python3
#
# Short version, harder to read

seats = []
for line in open('input.txt').read().splitlines():
    seats.append(int(line.replace('B','1').replace('F','0').replace('R','1').replace('L','0'), 2))

# part 1
print(max(seats))

# part 2
seats.sort()
for i in range(1, len(seats)):
    if seats[i] - seats[i - 1] > 1:
        print('missing', seats[i] - 1)
