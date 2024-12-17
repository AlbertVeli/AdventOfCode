#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc

class CPU:
    def __init__(self, a, b, c, program):
        """
        Initialize the CPU with registers A, B, C, and the program.
        """
        self.a = a
        self.b = b
        self.c = c
        self.program = program
        self.ip = 0
        self.output = []

    def fetch(self):
        """
        Fetch the current opcode and operand from the program.
        """
        if self.ip < len(self.program) - 1:
            opcode = self.program[self.ip]
            operand = self.program[self.ip + 1]
            return opcode, operand
		# End of program
        return None, None

    def step(self):
        """
        Execute a single instruction and update the instruction pointer.
        """
        opcode, operand = self.fetch()
        if opcode is None:
            # End of program
            return False

        # Execute one instruction

        # adv: A = A // (2^operand)
        if opcode == 0:
            self.a = self.a // self.get_denominator(operand)

        # bxl: B ^= operand
        elif opcode == 1:
            self.b ^= operand

        # bst: B = operand % 8
        elif opcode == 2:
            self.b = self.combo(operand) & 7

        # jnz: Jump if A != 0
        elif opcode == 3:
            if self.a != 0:
                self.ip = operand
                # Don't advance ip
                return True

        # bxc: B ^= C (ignore operand)
        elif opcode == 4:
            self.b ^= self.c

        # out: Output operand % 8
        elif opcode == 5:
            self.output.append(self.combo(operand) & 7)

        # bdv: B = A // (2^operand)
        elif opcode == 6:
            self.b = self.b // self.get_denominator(operand)

        # cdv: C = A // (2^operand)
        elif opcode == 7:
            self.c = self.a // self.get_denominator(operand)

        # Advance ip
        self.ip += 2
        return True

    def get_denominator(self, operand):
        """
        Calculate the denominator as 2^combo(operand).
        """
        shift = self.combo(operand)
        if shift < 0:
            raise ValueError('Negative shift not allowed')
        # 2 ** combo(operand)
        denominator = 1 << shift
        if denominator == 0:
            raise ValueError('Division by zero')
        return denominator

    def combo(self, operand):
        """
        Decode a combo operand into its value.
        """
        if operand < 4:
            # Immediate value
            return operand
        elif operand == 4:
            # Register A
            return self.a
        elif operand == 5:
            # Register B
            return self.b
        elif operand == 6:
            # Register C
            return self.c
        else:
            raise ValueError(f'Invalid operand: {operand}')

    def run(self):
        while self.step():
            pass

    def get_output(self):
        return ','.join(map(str, self.output))

# Main

data = aoc.lines_of_ints(sys.argv[1])
a = data[0][0]
b = data[1][0]
c = data[2][0]
program = data[4]

# Part 1, run with a, b, c
cpu = CPU(a, b, c, program)
cpu.run()
print('Part 1:', cpu.get_output())

# Part 2, brute force A until output matches program
# will not work, A is too large. The program needs
# to be decompiled, logic analyzed and a smaller
# brute force solution implemented.
expected_output = ','.join(map(str, program))
a = 0
while True:
    cpu = CPU(a, b, c, program)
    cpu.run()
    if cpu.get_output() == expected_output:
        print('Part 2:', a)
        break
    a += 1
