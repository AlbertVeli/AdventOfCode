#!/usr/bin/env python3

import sys
from collections import defaultdict

def mix_and_prune(secret, value):
    # mod = 16777216  # 2^24
    and_mask = 0xFFFFFF  # 2^24 - 1

    # Mix the value into the secret using XOR
    secret ^= value
    secret &= and_mask
    return secret

def transform_secret(secret):

    # Step 1: Multiply by 64
    value1 = secret * 64
    secret = mix_and_prune(secret, value1)

    # Step 2: Divide by 32 and round down (integer division)
    value2 = secret // 32
    secret = mix_and_prune(secret, value2)

    # Step 3: Multiply by 2048
    value3 = secret * 2048
    secret = mix_and_prune(secret, value3)

    return secret

def calc_2kth(secret_in):
    secret = secret_in
    for _ in range(2000):
        secret = transform_secret(secret)
    return secret

# Part 2 (thanks William)

def find_best_sequence(data, iterations = 2000):
    sequence_profits = defaultdict(int)

    # Iterate over each buyer's initial secret
    for secret in data:
        cur_sequence = []
        prev_price = secret % 10
        prev_sequences = set()

        for i in range(iterations):
            secret = transform_secret(secret)

            price = secret % 10

            # Calculate the change in price
            delta = price - prev_price
            cur_sequence.append(delta)

            # Maintain the length of cur_sequence to 4
            if len(cur_sequence) > 4:
                cur_sequence.pop(0)

            # Process sequences of length 4
            if i >= 3:
                cur_tuple = tuple(cur_sequence)

                # Only add to profits if the sequence is new for this buyer
                if cur_tuple not in prev_sequences:
                    sequence_profits[cur_tuple] += price
                    prev_sequences.add(cur_tuple)

            # Update the previous price
            prev_price = price

    # Find the sequence with the maximum profit
    best_sequence = max(sequence_profits, key=sequence_profits.get)

    # Retrieve the total bananas for the best sequence
    max_profit = sequence_profits[best_sequence]

    return best_sequence, max_profit

# Main

with open(sys.argv[1]) as f:
    data = list(map(int, f.read().splitlines()))

sum = 0
for val in data:
    #print(calc_2kth(val))
    sum += calc_2kth(val)
print('Part 1:', sum)

best_sequence, max_bananas = find_best_sequence(data)
print('Part 2:', max_bananas)
