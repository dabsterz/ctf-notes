"""Invert exactly: expected[i] = ROL8(input[i] XOR repeated_key[i], rotation)."""
import argparse
import json
from pathlib import Path


def rol8(x, r):
    r %= 8
    return ((x << r) | (x >> ((8-r) % 8))) & 255


def invert(data):
    key = bytes.fromhex(data['key_hex'])
    expected = bytes(data['expected'])
    r = int(data['rotation'])
    if not key:
        raise ValueError('key_hex must contain at least one byte')
    plain = bytes(rol8(y, -r) ^ key[i % len(key)] for i, y in enumerate(expected))
    forward = bytes(rol8(x ^ key[i % len(key)], r) for i, x in enumerate(plain))
    if forward != expected:
        raise ValueError('forward check failed')
    return plain


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('input', help='JSON: key_hex, rotation, expected (byte integer array)')
    ap.add_argument('--out', default='checker-plain.bin')
    args = ap.parse_args()
    try:
        plain = invert(json.loads(Path(args.input).read_text(encoding='utf-8-sig')))
        Path(args.out).write_bytes(plain)
        print('forward check: OK')
        print('candidate bytes:', repr(plain))
        print('saved:', args.out)
    except (ValueError, KeyError, TypeError, OSError) as exc:
        ap.exit(1, f'Transform stopped: {exc}\n')


if __name__ == '__main__':
    main()
