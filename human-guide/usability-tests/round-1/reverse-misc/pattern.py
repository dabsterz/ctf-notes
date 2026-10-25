import argparse
from pathlib import Path

def de_bruijn(alphabet, width):
    k = len(alphabet)
    work = [0] * (k * width)
    result = []
    def visit(t, period):
        if t > width:
            if width % period == 0:
                result.extend(work[1:period + 1])
        else:
            work[t] = work[t - period]
            visit(t + 1, period)
            for value in range(work[t - period] + 1, k):
                work[t] = value
                visit(t + 1, t)
    visit(1, 1)
    return bytes(alphabet[i] for i in result)

parser = argparse.ArgumentParser()
parser.add_argument('--length', type=int, default=512)
parser.add_argument('--find', help='four bytes in memory order, as eight hex digits')
args = parser.parse_args()
pattern = de_bruijn(b'abcdefgh', 4)
assert len({pattern[i:i+4] for i in range(len(pattern)-3)}) == len(pattern)-3
if args.find:
    needle = bytes.fromhex(args.find)
    if len(needle) != 4: raise SystemExit('supply exactly four bytes')
    print(pattern.find(needle))
else:
    if not 1 <= args.length <= len(pattern):
        raise SystemExit(f'length must be 1..{len(pattern)}')
    Path('pattern.bin').write_bytes(pattern[:args.length])
    print('wrote', args.length, 'bytes')
