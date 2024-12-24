#!/usr/bin/env python3

import sys

def parse_input(filename):
    with open(filename, "r") as file:
        input_text = file.read()
    lines = input_text.strip().split("\n")
    wire_values = {}
    gates = []

    # Process each line
    for line in lines:
        if ":" in line:  # Initial wire value
            wire, value = line.split(":")
            wire_values[wire.strip()] = int(value.strip())
        elif "->" in line:  # Gate definition
            parts = line.split("->")
            output_wire = parts[1].strip()
            operation = parts[0].strip()

            # Extract inputs and gate type
            if " AND " in operation:
                inputs = operation.split(" AND ")
                gate_type = "AND"
            elif " OR " in operation:
                inputs = operation.split(" OR ")
                gate_type = "OR"
            elif " XOR " in operation:
                inputs = operation.split(" XOR ")
                gate_type = "XOR"
            else:
                raise ValueError(f"Unknown operation: {operation}")

            gates.append({
                "inputs": [inputs[0].strip(), inputs[1].strip()],
                "gate_type": gate_type,
                "output": output_wire
            })

    return wire_values, gates

def simulate_gates(wire_values, gates):
    unresolved_gates = gates.copy()

    while unresolved_gates:
        for gate in unresolved_gates[:]:
            inputs = gate["inputs"]
            gate_type = gate["gate_type"]
            output = gate["output"]

            # Check if inputs are resolved
            if all(inp in wire_values for inp in inputs):
                inp_values = [wire_values[inp] for inp in inputs]

                # Perform the logic operation
                if gate_type == "AND":
                    result = inp_values[0] & inp_values[1]
                elif gate_type == "OR":
                    result = inp_values[0] | inp_values[1]
                elif gate_type == "XOR":
                    result = inp_values[0] ^ inp_values[1]
                else:
                    raise ValueError(f"Unknown gate type: {gate_type}")

                # Update wire values and remove gate from unresolved list
                wire_values[output] = result
                unresolved_gates.remove(gate)

    return wire_values

def concatenate_z_bits(wire_values):
    z_bits = [value for key, value in sorted(wire_values.items()) if key.startswith('z')]
    binary_string = ''.join(map(str, z_bits))
    return binary_string[::-1]

# Main

wires, gates = parse_input(sys.argv[1])
#print(wires)
#print(gates)
new_wires = simulate_gates(wires, gates)
#print(new_wires)
print('Part 1:', int(concatenate_z_bits(new_wires), 2))
