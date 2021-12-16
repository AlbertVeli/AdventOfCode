#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

bs = '{0:b}'.format(int(open(sys.argv[1]).read().rstrip(), 16))
bs = '0' * (len(bs) & 3) + bs
print(bs)

# Dissect packet, return result of expression
def dissect(i):

    # First 3 bits = version
    v = int(bs[i : i + 3], 2)

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
        value = int(lit, 2)
        print('literal value', lit, value)
        # return offset of last dissected bit
        return (j, value)
    else:
        # Operator
        values = []
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
                j, value = dissect(j)
                values.append(value)
        elif I == '1':
            # next 11 bits = number of sub-packets contained by this packet.
            subpackets = int(bs[i : i + 11], 2)
            dissected = 0
            i += 11
            j = i
            while subpackets - dissected > 0:
                print('dissect', j)
                j, value = dissect(j)
                values.append(value)
                dissected += 1

        # Do operation t on subpacket values
        if t == 0:
            value = sum(values)
        elif t == 1:
            value = 1
            for v in values:
                value *= v
        elif t == 2:
            value = min(values)
        elif t == 3:
            value = max(values)
        elif t == 5:
            value = int(values[0] > values[1])
        elif t == 6:
            value = int(values[0] < values[1])
        elif t == 7:
            value = int(values[0] == values[1])
        return (j, value)

j, value = dissect(0)
print(value)

