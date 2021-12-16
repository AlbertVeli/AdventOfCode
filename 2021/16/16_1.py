#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

bs = '{0:b}'.format(int(open(sys.argv[1]).read().rstrip(), 16))
bs = '0' * (len(bs) & 3) + bs
print(bs)

vsum = 0

# Dissect packet, count version numbers
def dissect(i):
    global vsum

    # First 3 bits = version
    v = int(bs[i : i + 3], 2)
    vsum += v

    # Next 3 bits = type id
    t = int(bs[i + 3 : i + 6], 2)

    if t == 4:
        # type id 4 -> literal value
        last = False
        j = i + 6
        lit = ''
        while not last:
            if bs[j] == '0':
                last = True
            lit += bs[j + 1 : j + 5]
            j += 5
        # return offset of last dissected bit
        print('literal value', lit)
        return j
    else:
        # Operator, type != 4
        I = bs[i + 6]
        i += 7
        if I == '0':
            # next 15 bits = length of sub-packets contained by this packet
            length = int(bs[i : i + 15], 2)
            print('sub packets =', length, 'bits')
            i += 15
            j = i
            while j - i < length:
                # dissect sub packet
                j = dissect(j)
            return j
        elif I == '1':
            # next 11 bits = number of sub-packets contained by this packet.
            subpackets = int(bs[i : i + 11], 2)
            dissected = 0
            i += 11
            j = i
            while subpackets - dissected > 0:
                print('dissect', j)
                j = dissect(j)
                dissected += 1
            return j

dissect(0)
print(vsum)
