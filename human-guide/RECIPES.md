# Recipe downloads and source

The short guide uses these complete scripts. In the website, each download is embedded and works offline. Save it inside a folder named `recipes` beside your challenge files; run from the parent folder. The ZIP already contains this layout. In Markdown, each link points to the included file.

Use WSL Python 3 from the supplied list. These helpers use the standard library only. Each script accepts `--help`. They implement the specific assumptions stated in the [quick reference](QUICKSTART.md); they do not choose an attack for you.

## jwt_claim.py

[Download jwt_claim.py](recipes/jwt_claim.py)

```python
"""Edit a JWT payload locally. This does NOT generate a valid signature."""
import argparse
import base64
import json
from pathlib import Path


def mutate(token, claim, value):
    header, payload, signature = token.strip().split('.')
    obj = json.loads(base64.urlsafe_b64decode(payload + '=' * (-len(payload) % 4)))
    if not isinstance(obj, dict):
        raise ValueError('JWT payload must be a JSON object')
    obj[claim] = json.loads(value)
    encoded = base64.urlsafe_b64encode(json.dumps(obj, separators=(',', ':')).encode()).rstrip(b'=').decode()
    return '.'.join((header, encoded, signature))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('input', help='text file containing only the captured JWT')
    ap.add_argument('--claim', default='role')
    ap.add_argument('--value', default='"admin"', help='JSON value; default is string admin')
    ap.add_argument('--out', default='edited-token.txt')
    args = ap.parse_args()
    try:
        token = mutate(Path(args.input).read_text(encoding='utf-8-sig'), args.claim, args.value)
        Path(args.out).write_text(token, encoding='ascii')
        print('saved:', args.out)
        print('Signature unchanged and invalid for edited payload. Only a server response can establish acceptance.')
    except (ValueError, TypeError, OSError) as exc:
        ap.exit(1, f'JWT stopped: {exc}\n')


if __name__ == '__main__':
    main()
```

## layers.py

[Download layers.py](recipes/layers.py)

```python
"""Strict Base64 decode; optionally decompress one zlib/gzip layer, keeping both."""
import argparse
import base64
import zlib
from pathlib import Path


def decode(raw, limit=16_000_000):
    if len(raw) > limit:
        raise ValueError('encoded input exceeds size budget')
    first = base64.b64decode(b''.join(raw.split()), validate=True)
    gzip = first.startswith(b'\x1f\x8b')
    zheader = len(first) >= 2 and first[0] & 15 == 8 and first[0] >> 4 <= 7 and int.from_bytes(first[:2], 'big') % 31 == 0
    if not (gzip or zheader):
        return first, None, b''
    dec = zlib.decompressobj(31 if gzip else 15)
    second = dec.decompress(first, limit+1)
    if len(second) > limit or dec.unconsumed_tail:
        raise ValueError('decompressed output exceeds size budget')
    if not dec.eof:
        raise ValueError('compressed stream is truncated or needs a different format')
    return first, second, dec.unused_data


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('input')
    ap.add_argument('--out', default='decoded', help='new output directory; existing directory is refused')
    args = ap.parse_args()
    try:
        path = Path(args.input)
        if path.stat().st_size > 16_000_000:
            raise ValueError('input exceeds 16 MB budget')
        first, second, trailer = decode(path.read_bytes())
        out = Path(args.out)
        out.mkdir(exist_ok=False)
        (out/'layer1.bin').write_bytes(first)
        print('layer1:', len(first), 'bytes; header:', first[:8].hex())
        if second is not None:
            (out/'layer2.bin').write_bytes(second)
            print('layer2:', len(second), 'bytes; preview:', repr(second[:200]))
            if trailer:
                (out/'trailing.bin').write_bytes(trailer)
            print('complete compressed stream; extra trailing bytes:', len(trailer))
        else:
            print('no zlib/gzip header; inspect layer1:', repr(first[:200]))
        print('saved in:', out)
    except (ValueError, OSError, zlib.error) as exc:
        ap.exit(1, f'Decoding stopped: {exc}\n')


if __name__ == '__main__':
    main()
```

## pattern.py

[Download pattern.py](recipes/pattern.py)

```python
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
parser.add_argument('--sent', help='verify the found offset against the pattern file actually sent')
args = parser.parse_args()
pattern = de_bruijn(b'abcdefgh', 4)
assert len({pattern[i:i+4] for i in range(len(pattern)-3)}) == len(pattern)-3
if args.find:
    needle = bytes.fromhex(args.find)
    if len(needle) != 4: raise SystemExit('supply exactly four bytes')
    offset = pattern.find(needle)
    print(offset)
    if args.sent:
        sent = Path(args.sent).read_bytes()
        if sent != pattern[:len(sent)] or offset < 0 or offset+4 > len(sent) or sent[offset:offset+4] != needle:
            raise SystemExit('not verified: wrong generator or crash bytes outside sent pattern')
        print('verified against sent file:', args.sent, '; length:', len(sent))
else:
    if args.sent: parser.error('--sent requires --find')
    if not 1 <= args.length <= len(pattern):
        raise SystemExit(f'length must be 1..{len(pattern)}')
    Path('pattern.bin').write_bytes(pattern[:args.length])
    print('wrote', args.length, 'bytes')
```

## png_tail.py

[Download png_tail.py](recipes/png_tail.py)

```python
"""Walk PNG chunk boundaries and save bytes after IEND. CRC issues are reported, not repaired."""
import argparse
import struct
import zlib
from pathlib import Path


def inspect(data):
    if data[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError('bad PNG signature')
    pos, checks = 8, []
    while pos+12 <= len(data):
        size = struct.unpack_from('>I', data, pos)[0]
        kind = data[pos+4:pos+8]
        end = pos+12+size
        if end > len(data):
            raise ValueError('chunk extends beyond file')
        crc = struct.unpack_from('>I', data, pos+8+size)[0]
        checks.append((kind, size, zlib.crc32(data[pos+4:pos+8+size]) == crc))
        pos = end
        if kind == b'IEND':
            if size != 0:
                raise ValueError('IEND must have length zero')
            return data[pos:], checks
    raise ValueError('no complete IEND chunk')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('input')
    ap.add_argument('--out', default='png-trailer.bin')
    args = ap.parse_args()
    try:
        path = Path(args.input)
        if path.stat().st_size > 64_000_000:
            raise ValueError('input exceeds 64 MB budget')
        tail, checks = inspect(path.read_bytes())
        for kind, size, valid in checks:
            print(kind, size, 'CRC OK' if valid else 'BAD CRC: inspect before trusting the structure')
        Path(args.out).write_bytes(tail)
        print('trailing bytes:', len(tail), 'preview:', repr(tail[:200]))
        print('saved:', args.out)
        print('Chunk walk only; not a full PNG validity check.')
    except (ValueError, OSError) as exc:
        ap.exit(1, f'PNG inspection stopped: {exc}\n')


if __name__ == '__main__':
    main()
```

## rsa.py

[Download rsa.py](recipes/rsa.py)

```python
"""Raw two-prime RSA: known factors or a bounded close-prime check. No padding removal."""
import argparse
import json
import math
from pathlib import Path


def recover(data, steps=100000):
    number = lambda x: int(x, 0) if isinstance(x, str) else int(x)
    n, e, c = (number(data[k]) for k in ('n', 'e', 'c'))
    if n <= 3 or e <= 1 or not 0 <= c < n:
        raise ValueError('require n > 3, e > 1, and 0 <= c < n')
    if 'p' in data and 'q' in data:
        p, q = number(data['p']), number(data['q'])
    else:
        if n % 2 == 0:
            raise ValueError('even modulus: inspect factor 2 separately')
        a = math.isqrt(n)
        a += a*a < n
        for _ in range(steps):
            b2 = a*a - n
            b = math.isqrt(b2)
            if b*b == b2:
                p, q = a-b, a+b
                break
            a += 1
        else:
            raise ValueError('no close factors within budget; use another RSA route')
    if p <= 1 or q <= 1 or p == q or p*q != n:
        raise ValueError('need distinct factors p*q == n; formula assumes both are prime')
    d = pow(e, -1, math.lcm(p-1, q-1))
    m = pow(c, d, n)
    if pow(m, e, n) != c:
        raise ValueError('re-encryption failed; check the factors and RSA assumptions')
    length = number(data.get('length', max(1, (m.bit_length()+7)//8)))
    return p, q, m.to_bytes(length, 'big')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('input', help='JSON: n, e, c; optional p, q and byte length')
    ap.add_argument('--steps', type=int, default=100000)
    ap.add_argument('--out', default='rsa-plain.bin')
    args = ap.parse_args()
    try:
        p, q, plain = recover(json.loads(Path(args.input).read_text(encoding='utf-8-sig')), args.steps)
        Path(args.out).write_bytes(plain)
        print('factors:', p, q)
        print('re-encryption: OK')
        print('plaintext bytes:', repr(plain))
        print('saved:', args.out)
        print('No padding removed. Without length, leading zero bytes cannot be recovered.')
    except (ValueError, KeyError, TypeError, OSError, OverflowError) as exc:
        ap.exit(1, f'RSA stopped: {exc}\n')


if __name__ == '__main__':
    main()
```

## tar_keep.py

[Download tar_keep.py](recipes/tar_keep.py)

```python
"""Keep every regular tar member, including duplicate names, without trusting archive paths."""
import argparse
import json
import tarfile
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('input')
    ap.add_argument('--out', default='tar-parts', help='new output directory')
    args = ap.parse_args()
    try:
        out = Path(args.out)
        out.mkdir(exist_ok=False)
        total = 0
        with tarfile.open(args.input, 'r:*') as tf, (out/'manifest.jsonl').open('w', encoding='utf-8') as log:
            for i, member in enumerate(tf):
                if i >= 10000:
                    raise ValueError('member-count budget exceeded')
                if not member.isfile():
                    continue
                total += member.size
                if member.size > 64_000_000 or total > 512_000_000:
                    raise ValueError('extraction budget exceeded; earlier members retained')
                src = tf.extractfile(member)
                if src is None:
                    raise ValueError('regular file has no readable body')
                with src:
                    data = src.read(member.size+1)
                if len(data) != member.size:
                    raise ValueError('truncated member')
                name = f'{i:06d}.bin'
                (out/name).write_bytes(data)
                log.write(json.dumps(dict(index=i, name=member.name, saved=name, size=len(data)))+'\n')
                print(name, repr(member.name), len(data), 'bytes; preview:', repr(data[:120]))
        print('manifest:', out/'manifest.jsonl')
    except (ValueError, OSError, tarfile.TarError) as exc:
        ap.exit(1, f'Tar extraction stopped: {exc}\n')


if __name__ == '__main__':
    main()
```

## transform.py

[Download transform.py](recipes/transform.py)

```python
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
```

## vm_byte.py

[Download vm_byte.py](recipes/vm_byte.py)

```python
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
```
