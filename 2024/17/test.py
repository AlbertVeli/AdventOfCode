#!/usr/bin/env python3

def run_program(A, B, C, expected_output):
    output = []
    # Forward logic:
    while True:
        B = A % 8
        B ^= 2
        C = A // (2 ** B)
        B ^= C
        A //= 8
        B ^= 7
        output.append(B % 8)
        if A == 0:
            print(A, B, C)
            print(output)
            break
    return output == expected_output

# Initial State:
A = 22817223
B = 0
C = 0
expected_output = [4,3,7,1,5,3,0,5,4]
print(run_program(A, B, C, expected_output))

# Reverse logic, guessing the last A and C values
# XXX: Fix this logic
def reverse_program(A, C, expected_output):
    # Start from the last output and work backward
    for output in reversed(expected_output):
        # Step 1: Reverse `B % 8`
        B = output

        # Step 2: Reverse `B ^= 7`
        B ^= 7

        # Step 3: Reverse `A //= 8`
        A = A * 8  # Multiply A back by 8.

        # Step 4: Reverse `B ^= C`
        B ^= C

        # Step 5: Reverse `C = A // (2 ** B)`
        A = C * (2 ** B)

        # Step 6: Reverse `B ^= 2`
        B ^= 2

        # Step 7: Reverse `B = A % 8`
        A = (B + 8 * 0)  # Use k=0 for simplicity.

    return A

# The wanted program output
expected_output = [2,4,1,2,7,5,4,5,0,3,1,7,5,5,3,0]

# Calculate initial A
for a in range(10):
    for c in range(10):
        initial_A = reverse_program(0, 0, expected_output)
        print(f'a = {a}, c = {c} -> initial a: {initial_A}')
        run_program(initial_A, 0, 0, expected_output)
