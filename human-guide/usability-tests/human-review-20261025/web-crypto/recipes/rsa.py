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
