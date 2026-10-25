import json
from math import gcd, isqrt, lcm
from pathlib import Path

def fermat(n, budget=10000):
    if n % 2 == 0:
        return 2, n//2
    a = isqrt(n)
    if a*a < n:
        a += 1
    for _ in range(budget):
        delta = a*a - n
        b = isqrt(delta)
        if b*b == delta:
            return a-b, a+b
        a += 1
    return None

data = json.loads(Path(__file__).with_name('rsa.json').read_text())
n, e, c = data['n'], data['e'], data['c']
factors = fermat(n)
print('Fermat factors:', factors)
if factors is None:
    raise SystemExit('Guide Fermat route exhausted; stop this route.')
p, q = factors
assert p*q == n
lam = lcm(p-1, q-1)
assert gcd(e, lam) == 1
d = pow(e, -1, lam)
recovered = pow(c, d, n)
assert pow(recovered, e, n) == c
print('plaintext integer:', recovered)
print('re-encryption:', pow(recovered, e, n), 'matches:', pow(recovered, e, n) == c)
# Independent basic sizing glue: round bit count up to byte count.
length = (recovered.bit_length() + 7) // 8
raw = recovered.to_bytes(length, 'big')
Path(__file__).with_name('rsa-plaintext.bin').write_bytes(raw)
print('minimal-length plaintext bytes:', raw)
