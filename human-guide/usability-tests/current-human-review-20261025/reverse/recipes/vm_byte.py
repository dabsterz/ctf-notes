"""Enumerate one-byte input for a known straight-line 8-bit VM, resetting state each time."""
import argparse
import json
from pathlib import Path


def validate(program):
    if not isinstance(program, list) or not 3 <= len(program) <= 1000:
        raise ValueError('program must contain 3..1000 instruction rows')
    widths = {'LOAD_INPUT': 1, 'XOR': 2, 'ADD': 2, 'ROL': 2, 'CMP': 2, 'HALT': 1}
    for row in program:
        if not isinstance(row, list) or not row or not isinstance(row[0], str) or len(row) != widths.get(row[0], 0):
            raise ValueError(f'unsupported instruction: {row!r}')
        if len(row) == 2 and (type(row[1]) is not int or not 0 <= row[1] <= 255):
            raise ValueError('operands must be byte integers 0..255')
    if program[0] != ['LOAD_INPUT'] or program[-1] != ['HALT']:
        raise ValueError('program must start LOAD_INPUT and end HALT')
    if sum(row[0] == 'LOAD_INPUT' for row in program) != 1 or sum(row[0] == 'HALT' for row in program) != 1 or not any(row[0] == 'CMP' for row in program):
        raise ValueError('need exactly one input/halt and at least one CMP')


def run(program, value):
    acc, ok, trace = 0, True, []
    for row in program:
        op = row[0]
        if op == 'LOAD_INPUT': acc = value
        elif op == 'XOR': acc ^= row[1]
        elif op == 'ADD': acc = (acc + row[1]) & 255
        elif op == 'ROL':
            r = row[1] % 8
            acc = ((acc << r) | (acc >> ((8-r) % 8))) & 255
        elif op == 'CMP': ok = ok and acc == row[1]
        elif op == 'HALT': break
        trace.append(f'{op}: 0x{acc:02x}')
    return ok, trace


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('input', help='JSON: program, e.g. [["LOAD_INPUT"],["XOR",35],["ADD",7],["CMP",111],["HALT"]]')
    args = ap.parse_args()
    try:
        program = json.loads(Path(args.input).read_text(encoding='utf-8-sig'))['program']
        validate(program)
        found = []
        for value in range(256):
            ok, trace = run(program, value)
            if ok:
                found.append(value)
                print(f'candidate: {value} / 0x{value:02x} / {bytes([value])!r}')
                print(' -> '.join(trace), 'all comparisons: OK')
        if not found:
            raise ValueError('no byte satisfies every comparison; check opcode semantics')
        print('candidate count:', len(found))
    except (ValueError, KeyError, TypeError, OSError) as exc:
        ap.exit(1, f'VM stopped: {exc}\n')


if __name__ == '__main__':
    main()
