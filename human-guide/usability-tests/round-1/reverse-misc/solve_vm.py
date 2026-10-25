import json
from pathlib import Path

program = json.loads(Path(__file__).with_name('payload.json').read_text())['program']
# Guide section 8: reverse modular addition by subtraction, then XOR again.
assert [i[0] for i in program] == ['LOAD_INPUT', 'XOR', 'ADD', 'CMP', 'HALT']
candidate = ((program[3][1] - program[2][1]) & 255) ^ program[1][1]
print(f'candidate: {candidate} / 0x{candidate:02x} / {chr(candidate)!r}')
# Adapted section 10: JSON instruction rows instead of numeric bytecode.
pc, accumulator = 0, 0
steps = 0
passed = False
while pc < len(program):
    steps += 1
    if steps > 100: raise RuntimeError('instruction budget exhausted')
    at = pc
    instruction = program[pc]
    opcode = instruction[0]
    pc += 1
    if opcode == 'HALT':
        break
    if opcode == 'LOAD_INPUT':
        accumulator = candidate
    elif opcode in ('LOAD', 'XOR', 'ADD', 'CMP'):
        if len(instruction) != 2: raise ValueError('truncated operand')
        operand = instruction[1]
        if opcode == 'LOAD': accumulator = operand
        elif opcode == 'XOR': accumulator ^= operand
        elif opcode == 'ADD': accumulator = (accumulator + operand) & 255
        elif opcode == 'CMP':
            passed = accumulator == operand
            print(f'comparison: {accumulator} == {operand}: {passed}')
    else:
        raise ValueError(f'unknown opcode {opcode} at {at}')
    print(f'pc={at:02x} op={opcode} a={accumulator:02x}')
assert passed
