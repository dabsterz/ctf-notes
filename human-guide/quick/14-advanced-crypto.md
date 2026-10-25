# Advanced cryptography

Use after [basic crypto](07-cryptography.md). Set `FILE` to your supplied parameters. JSON examples below use decimal integers, not hexadecimal strings. [Full reference](../reference/chapters/14-advanced-crypto.md) preserves complete lattice, GF(2), LFSR, sharing, proof-system and algebra explanations.

## Quick: test an unusually small RSA private exponent

**WSL · Python 3.** Input: `rsa.json` containing `n`, `e`. Wiener works only under small-private-exponent assumptions.

```bash
FILE='rsa.json'
python3 - "$FILE" <<'PY'
import json, sys
from pathlib import Path
from math import isqrt
v = json.loads(Path(sys.argv[1]).read_text()); n, e = v['n'], v['e']
a, b, p0, p1, q0, q1 = e, n, 0, 1, 1, 0
while b:
    t, r = divmod(a, b); a, b = b, r
    p0, p1 = p1, t*p1+p0; q0, q1 = q1, t*q1+q0
    k, d = p1, q1
    if not k or (e*d-1) % k: continue
    phi = (e*d-1)//k; s = n-phi+1; delta = s*s-4*n
    if delta < 0: continue
    root = isqrt(delta)
    if root*root != delta or (s+root) % 2: continue
    p, q = (s+root)//2, (s-root)//2
    if p > 1 and q > 1 and p*q == n:
        print('d', d, 'p', p, 'q', q); break
else: print('No verified Wiener candidate')
PY
```

**Look for:** factors whose product equals `n`; decrypt/re-encrypt with the basic recipe.
**If not:** inspect key generation; failure does not establish secure parameters.

## Quick: try bounded local p-minus-one factoring

**WSL · Python 3.** Input: `rsa.json` containing `n`. Bound 10,000 is a deliberate time limit.

```bash
FILE='rsa.json'
python3 - "$FILE" <<'PY'
import json, sys
from pathlib import Path
from math import gcd
n = json.loads(Path(sys.argv[1]).read_text())['n']; a = 2
for j in range(2, 10001):
    a = pow(a, j, n); p = gcd(a-1, n)
    if 1 < p < n:
        print('p', p, 'q', n//p); break
    if p == n:
        print('Both factors reached; change model/base'); break
else: print('No factor within bound')
PY
```

**Look for:** a proper factor when a prime's predecessor is smooth.
**If not:** stop expanding blindly; inspect another structural weakness.

## Quick: factor from a faulty RSA signature

**WSL · Python 3.** Input JSON: `n`, `e`, `signature`, `m`; `m` is the encoded integer being signed, including any hashing/padding.

```bash
FILE='fault.json'
python3 - "$FILE" <<'PY'
import json, sys
from pathlib import Path
from math import gcd
v = json.loads(Path(sys.argv[1]).read_text()); n = v['n']
p = gcd(pow(v['signature'], v['e'], n)-v['m'], n)
print(('p', p, 'q', n//p) if 1 < p < n else 'No proper factor')
PY
```

**Look for:** one correct CRT residue exposing a proper factor.
**If not:** check message encoding and whether the fault preserves either residue.

## Quick: recover a candidate hidden RSA modulus

**WSL · Python 3.** Input JSON: `e`, `pairs` containing `[message_integer,ciphertext_integer]` rows. Use at least two known pairs; bounds prevent huge unreduced powers.

```bash
FILE='samples.json'
python3 - "$FILE" <<'PY'
import json, sys
from pathlib import Path
from math import gcd
v = json.loads(Path(sys.argv[1]).read_text()); e, pairs = v['e'], v['pairs']
assert 2 <= e <= 17 and len(pairs) >= 2
candidate = 0
for m, c in pairs:
    assert m >= 0 and c >= 0 and m.bit_length() <= 8192
    candidate = gcd(candidate, abs(m**e-c))
if candidate > max(c for m,c in pairs):
    print('candidate, possibly a multiple of n:', candidate)
    print('all samples fit:', all(pow(m,e,candidate) == c for m,c in pairs))
else: print('No usable modulus candidate')
PY
```

**Look for:** a candidate explaining every sample.
**If not:** verify textbook RSA assumptions; collect independent pairs to reduce multiples.

## Quick: test a genuinely small discrete-log range

**WSL · Python 3.** Input JSON: prime `p`, generator/base `g`, target `h`, inclusive exponent `bound` no larger than 1,000,000.

```bash
FILE='dlog.json'
python3 - "$FILE" <<'PY'
import json, sys
from pathlib import Path
v = json.loads(Path(sys.argv[1]).read_text())
p,g,h,bound = (v[k] for k in ('p','g','h','bound'))
assert p > 2 and 0 < g < p and 0 < h < p and 0 <= bound <= 1000000
value = 1
for x in range(bound+1):
    if value == h:
        assert pow(g,x,p) == h
        print('verified exponent', x); break
    value = value*g % p
else: print('No exponent in the stated range')
PY
```

**Look for:** an exponent verified by modular exponentiation.
**If not:** use the reference's bounded baby-step/giant-step or subgroup analysis.

## Quick: check supplied elliptic-curve points

**WSL · Python 3.** Input JSON: prime `p`, coefficients `a`,`b`, and finite `points` containing `[x,y]` rows for `y² = x³ + ax + b`.

```bash
FILE='curve.json'
python3 - "$FILE" <<'PY'
import json, sys
from pathlib import Path
v = json.loads(Path(sys.argv[1]).read_text()); p,a,b = (v[k] for k in ('p','a','b'))
assert p > 3
print('nonsingular:', (4*a**3+27*b**2) % p != 0)
for i, (x,y) in enumerate(v['points']):
    print(i, 'canonical:', 0 <= x < p and 0 <= y < p,
          'on curve:', (y*y-x*x*x-a*x-b) % p == 0)
PY
```

**Look for:** singular parameters or missing point validation in the challenge source.
**If not:** membership alone proves neither subgroup order nor nonce safety.

## Quick: recover a repeated-nonce DSA candidate

**WSL · Python 3.** Input JSON: prime subgroup `q`, repeated `r`, signatures `s1`,`s2`, message-hash integers `h1`,`h2` reduced as the signer does. Assumes the same key and exact same nonce.

```bash
FILE='signatures.json'
python3 - "$FILE" <<'PY'
import json, sys
from pathlib import Path
v = json.loads(Path(sys.argv[1]).read_text())
q,r,s1,s2,h1,h2 = (v[k] for k in ('q','r','s1','s2','h1','h2'))
k = (h1-h2)*pow((s1-s2) % q,-1,q) % q
x = (s1*k-h1)*pow(r,-1,q) % q
assert (s1*k-h1-x*r) % q == (s2*k-h2-x*r) % q == 0
print('nonce candidate', k, 'private-key candidate', x)
PY
```

**Look for:** a candidate matching the public key and validating both original signatures.
**If not:** check hash reduction, nonce assumptions and inverse failures; algebra alone is insufficient.

## Quick: locate the matching advanced implementation

**Kali · ripgrep / crypto-attacks checkout.** Read assumptions and function signatures before choosing dependencies; this block does not run attacks.

```bash
DIR='/opt/tools/crypto-attacks'
rg --files "$DIR" | rg 'hidden_number|lwe|coppersmith|knapsack|lcg|shamir|wiener'
rg -n '^def |^from |^import ' "$DIR/attacks/rsa/wiener.py"
```

**Look for:** the exact equation, unknown bounds, input format and verification condition.
**If not:** use the full reference to build the model; a missing dependency is not a reason to upload parameters online.
