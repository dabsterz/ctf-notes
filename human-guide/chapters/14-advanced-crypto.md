# Advanced cryptography

Use after [basic crypto](07-cryptography.md). Set `FILE` to your supplied parameters. JSON examples below use decimal integers, not hexadecimal strings. [Full reference](#full-reference) preserves complete lattice, GF(2), LFSR, sharing, proof-system and algebra explanations.

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

## Full reference

<details class="deep-reference" markdown="1">
<summary>Explanations, advanced cases and sources</summary>

# Advanced cryptography: choose a model you can verify

**Quick route:** [Short commands](../QUICKSTART.md#rsa) · [Tool strengths and weaknesses](../TOOL-CHOOSER.md#cryptography). Use this chapter for deeper explanations.

Use this chapter after [Cryptography](07-cryptography.md). These techniques are retained because the original repository covers considerably more than introductory RSA and XOR. They are not a suggestion to run every attack against every number.

All Python demonstrations run locally with Python 3 in Windows WSL or Kali. Save the named files and run them with `python3`. Where a script imports `math_helpers`, use the helper file from chapter 07 in the same directory. Sage is optional on Kali: the approved sheet records it but gives no installation information. The approved crypto-attacks checkout is also Kali-specific. No online mathematical service is needed here.

## 1. RSA decision points beyond the elementary checks

| Evidence | Candidate technique | Required verification |
|---|---|---|
| Tiny private exponent with balanced primes | Wiener continued fractions | Recovered factors multiply to `n`; private exponent decrypts |
| Larger but unusually small private exponent | Boneh–Durfee lattice | The lattice bounds and model fit the challenge; candidate factors verify |
| Known contiguous bits of a prime or private exponent | Coppersmith/partial-key recovery | Construct the exact polynomial and unknown bound |
| Known small `dp` or `dq` | CRT exponent attack | Respect exponent bounds and recovered congruences |
| Smooth `p-1` or `p+1` | Pollard p−1 or Williams p+1 | GCD returns a proper factor, not 1 or `n` |
| Related messages under the same key | Franklin–Reiter/polynomial GCD | The relation is exact modulo `n` |
| Faulty CRT signature | Bellcore-style GCD | At least one residue remains correct |
| Encryption samples but hidden modulus | GCD of `m^e-c` values | Candidate modulus explains all samples |
| Repeated primes or noncoprime exponent | Root enumeration in prime powers | Enumerate all roots and verify each |

ROCA, restricted-digit primes, base-representation primes, dependent primes, and shared high/low bits are key-generation structures. Start by reproducing that generator on a tiny instance. A patterned decimal modulus does not establish patterned factors.

## 2. Wiener: a complete toy with candidate validation

Save as `wiener_toy.py`:

```python
from math import isqrt, gcd

def convergents(numerator, denominator):
    p0, p1, q0, q1 = 0, 1, 1, 0
    while denominator:
        a, remainder = divmod(numerator, denominator)
        p0, p1 = p1, a*p1+p0
        q0, q1 = q1, a*q1+q0
        yield p1, q1
        numerator, denominator = denominator, remainder

def wiener(e, n):
    for k, d in convergents(e, n):
        if k == 0 or (e*d-1) % k:
            continue
        phi = (e*d-1)//k
        total = n-phi+1
        discriminant = total*total-4*n
        if discriminant < 0:
            continue
        root = isqrt(discriminant)
        if root*root != discriminant or (total+root) % 2:
            continue
        p, q = (total+root)//2, (total-root)//2
        if p*q == n:
            return d, p, q
    return None

p, q, d = 1009, 1013, 5
phi, n = (p-1)*(q-1), p*q
assert gcd(d, phi) == 1
e = pow(d, -1, phi)
answer = wiener(e, n)
assert answer is not None and answer[0] == d
assert answer[1]*answer[2] == n
print(answer)
```

Wiener's sufficient bound assumes suitable prime sizes and a genuinely small private exponent. Failure does not prove secure key generation. Do not increase brute-force ranges blindly; inspect whether the source actually biases `d`.

## 3. Local smoothness factoring and fault checks

Save as `rsa_advanced_toys.py`:

```python
from math import gcd

def pollard_p_minus_one(n, bound):
    a = 2
    for j in range(2, bound+1):
        a = pow(a, j, n)
        candidate = gcd(a-1, n)
        if 1 < candidate < n:
            return candidate
        if candidate == n:
            return None
    return None

n = 257*1019
factor = pollard_p_minus_one(n, 30)
assert factor is not None and n % factor == 0
print('p-1 factor:', factor)

# A correct signature and one faulty CRT residue.
p, q, e, message = 61, 53, 17, 65
n = p*q
d = pow(e, -1, (p-1)*(q-1))
signature = pow(message, d, n)
# Adding p preserves the residue modulo p but changes it modulo q.
faulty = (signature+p) % n
factor = gcd(pow(faulty, e, n)-message, n)
assert factor == p
print('fault factor:', factor)
```

Pollard p−1 depends on smoothness of the factor's predecessor, not the size of the whole modulus. If the GCD becomes `n`, both factors may have entered the exponent; change the bound/base in a controlled local experiment.

Williams p+1 and ECM require different machinery. In the approved Kali crypto-attacks checkout, inspect the relevant implementation's signature and required parameters before importing it. Do not install YAFU: it is explicitly unapproved. A missing local factoring dependency is a limitation to record, not permission to upload the modulus.

## 4. Nonunique roots, Rabin, and unusual totients

Rabin encryption squares a message modulo `pq`. With distinct primes congruent to 3 modulo 4, square roots can be recovered separately and recombined into four candidates.

Save as `rabin_roots.py`:

```python
from math_helpers import crt

p, q, message = 11, 19, 42
n = p*q
ciphertext = message*message % n
rp = pow(ciphertext, (p+1)//4, p)
rq = pow(ciphertext, (q+1)//4, q)
roots = {crt([a, b], [p, q])
         for a in {rp, (-rp) % p}
         for b in {rq, (-rq) % q}}
assert message in roots
assert len(roots) == 4
assert all(x*x % n == ciphertext for x in roots)
print(sorted(roots))
```

Encoding or redundancy selects a candidate; the mathematics alone does not know the flag format. Repeated factors, roots modulo prime powers, Schmidt–Samoa `p²q`, quaternion exponents, and custom expressions such as `(p^4-1)(q^4-1)` need the group actually used by the program. Do not rename such an expression `phi` and assume textbook RSA proof applies.

If a modulus is hidden, collect several known plaintext/ciphertext pairs and compute local GCDs of exact encryption residuals. The result may be a multiple of `n`; require it to fit ciphertext ranges and every sample. Large exponents can make unreduced powers expensive, so assess input size first.

## 5. Small roots and polynomial relations

Coppersmith methods look for bounded integer roots of modular polynomials. Before opening a lattice tool, write:

```text
Ring and modulus: __________________________
Polynomial f(x): ___________________________
Unknown x represents: ______________________
Bound |x| < X: _____________________________
Known factor-size fraction beta: ___________
How candidate x recovers p/message: ________
```

A known-prefix message gives a polynomial such as `(prefix*2^t+x)^e-c`. A known prime prefix instead gives `known+x`, vanishing modulo an unknown factor of `n`. These are different `beta` cases. Linearly related messages suggest a polynomial GCD before a lattice.

**Optional Kali Sage**, first confirm `sage --version`. Save this illustrative, deliberately easy instance as `small_root.sage`:

```sage
N = 1000003 * 1000033
R.<x> = PolynomialRing(Zmod(N))
secret = 123
f = x - secret
roots = f.small_roots(X=2^10, beta=1)
assert secret in [ZZ(r) for r in roots]
assert all(f(r) == 0 for r in roots)
print(roots)
```

Run `sage small_root.sage`. This checks environment and syntax, not the feasibility of a hard RSA attack. For the actual challenge, derive the polynomial and bounds from source. A monic-polynomial requirement, noninvertible leading coefficient, wrong root size, or wrong modulus commonly causes failure.

Hensel lifting solves roots modulo `p^k` from roots modulo `p` when its derivative conditions hold. If the derivative vanishes modulo `p`, branches can disappear or multiply; do not apply the simple-root formula blindly. Polynomial CRT over `GF(2)[x]` uses coprime polynomials, not integer moduli.

## 6. Discrete logarithms with explicit bounds

Baby-step giant-step uses about `sqrt(order)` storage and operations. Use it when that bound is realistically small, not for an arbitrary 256-bit prime-order group.

Save as `bsgs_toy.py`:

```python
from math import isqrt

def bsgs(g, h, p, order):
    width = isqrt(order)+1
    table = {}
    value = 1
    for j in range(width):
        table.setdefault(value, j)
        value = value*g % p
    step = pow(pow(g, width, p), -1, p)
    value = h
    for i in range(width+1):
        if value in table:
            candidate = i*width+table[value]
            if candidate < order and pow(g, candidate, p) == h:
                return candidate
        value = value*step % p
    return None

p, g, secret = 1019, 2, 123
h = pow(g, secret, p)
recovered = bsgs(g, h, p, p-1)
assert recovered == secret
print(recovered)
```

For Pohlig–Hellman, factor the **group order**, solve prime-power subgroup logarithms, then use CRT. A smooth `p-1` helps finite-field DH only if the actual generator order inherits the small factors. For ECC, use the curve/subgroup order, not `p-1`.

Sparse exponents can permit a meet-in-the-middle search over positions instead of all integer values. Count combinations first and verify the sparsity promise from source. A low Hamming weight guess without evidence can be more expensive than ordinary BSGS.

## 7. Elliptic-curve triage

Write down the curve model, field, coefficients, base point, subgroup order, cofactor, point encoding, and validation routine. The following are distinct failure families:

| Family | Observable prerequisite | Starting calculation |
|---|---|---|
| Singular curve | Discriminant vanishes | For short Weierstrass, check `4*a^3+27*b^2 == 0 mod p` |
| Anomalous curve | Curve order equals field prime | Compute/confirm `#E(Fp) == p` before considering Smart's attack |
| Small subgroup | Accepted low-order point and reused scalar | Determine point order; compare oracle outputs for each residue |
| Invalid curve | Coordinates accepted without curve membership check | Check whether scalar multiplication formulas ignore a supplied coefficient |
| Weak twist | X-coordinate-only multiplication plus weak twist order | Analyze the twist order and low-order acceptance |
| MOV reduction | Small embedding degree | Find small `k` for which subgroup order divides `p^k-1` |
| Nonce reuse/bias | Repeated `r`, partial nonce bits, or biased generation | Verify message hashing; then reuse formulas or HNP |
| Faults | Corrupted scalar multiplication or signature | Determine which intermediate relation remains valid |

Point negation, infinity encoding, and malformed points differ across libraries. X25519 low-order input can produce an all-zero shared secret; check whether the protocol rejects it. Ed25519 torsion issues depend on point validation and the verification equation. A cofactor greater than one is not by itself an exploit.

Clock groups satisfying `x²+y²=1`, singular curves with additive/multiplicative parameterizations, and endomorphism-based constructions can reduce to more familiar groups. Derive and test the map on toy points: it must preserve the operation and handle exceptional points. CM/GLV structure alone does not break correctly implemented standard curves.

Isogeny challenges need the exact curve and isogeny construction. Determine what the public key reveals and whether parameters are deliberately weakened; do not treat an isogeny keyword as permission to apply an unrelated historical attack.

## 8. Linear algebra over GF(2)

CRC adjustments, linear PRNGs, XOR aggregate hashes, and some stream-cipher leaks become binary linear systems. Each equation is a bitmask of coefficients plus one result bit. Bit order must match the source.

Save as `gf2_solve.py`:

```python
def solve_gf2(equations, variables):
    rows = [[mask, rhs] for mask, rhs in equations]
    pivots = []
    next_row = 0
    for column in range(variables):
        selected = next((i for i in range(next_row, len(rows))
                         if (rows[i][0] >> column) & 1), None)
        if selected is None:
            continue
        rows[next_row], rows[selected] = rows[selected], rows[next_row]
        for i in range(len(rows)):
            if i != next_row and ((rows[i][0] >> column) & 1):
                rows[i][0] ^= rows[next_row][0]
                rows[i][1] ^= rows[next_row][1]
        pivots.append(column)
        next_row += 1
    if any(mask == 0 and rhs for mask, rhs in rows):
        raise ValueError('inconsistent system')
    if len(pivots) != variables:
        raise ValueError('underdetermined: collect independent equations')
    result = 0
    for row, column in enumerate(pivots):
        result |= rows[row][1] << column
    return result

secret = 0b1011
masks = [0b0011, 0b0110, 0b1100, 0b1000]
equations = [(mask, (mask & secret).bit_count() & 1) for mask in masks]
recovered = solve_gf2(equations, 4)
assert recovered == secret
assert all(((mask & recovered).bit_count() & 1) == rhs
           for mask, rhs in equations)
print(bin(recovered))
```

If rank is low, more repeated versions of the same equation will not help. Choose inputs that excite different state bits. For affine CRC relations, subtract/XOR a fixed baseline before building the linear matrix. Validate the final patch with the original checksum routine.

## 9. LFSR recovery with Berlekamp–Massey

Save as `lfsr_bm.py`:

```python
def berlekamp_massey(bits):
    size = len(bits)
    C, B = [0]*(size+1), [0]*(size+1)
    C[0] = B[0] = 1
    length, since = 0, 1
    for n in range(size):
        discrepancy = bits[n]
        for i in range(1, length+1):
            discrepancy ^= C[i] & bits[n-i]
        if discrepancy == 0:
            since += 1
            continue
        old = C[:]
        for j in range(size+1-since):
            C[j+since] ^= B[j]
        if 2*length <= n:
            length = n+1-length
            B = old
            since = 1
        else:
            since += 1
    return length, C[:length+1]

bits = [1, 0, 0, 1]
for i in range(4, 60):
    bits.append(bits[i-1] ^ bits[i-4])
length, coefficients = berlekamp_massey(bits[:30])
predicted = bits[:30]
for n in range(30, 60):
    bit = 0
    for i in range(1, length+1):
        bit ^= coefficients[i] & predicted[n-i]
    predicted.append(bit)
assert length == 4
assert predicted == bits
print(length, coefficients)
```

Expected recurrence coefficients are `[1, 1, 0, 0, 1]`. Always verify on held-out bits. Fibonacci versus Galois form, reversed bit order, discarded warmup, and output filters can make a correct polynomial appear wrong.

RC4 second-byte bias is statistical across many independent keys; it is not a deterministic two-byte decryption trick. RC4A, VMPC, and Spritz modify the generator, so identify the update algorithm. Trivium, Grain, and Mickey analyses depend strongly on reduced rounds, warmup, and access to chosen IVs.

## 10. Lattices: build the equations before the basis

LLL finds a reduced basis; it is not a command that directly returns a private key. BKZ is stronger and more expensive. Babai estimates a nearby lattice point; exact CVP/SVP have different costs. A short output row must be interpreted and checked in the original problem.

For each lattice write down row/column orientation, modulus, scaling, unknown bounds, error distribution, and extraction rule. Make a tiny generated instance where the secret is known. Recover that secret before increasing dimensions.

| Problem | Equation to derive | Most common modelling error |
|---|---|---|
| Hidden Number Problem | Signature relation with bounded nonce error | Using field prime instead of signature order; wrong known-bit offset |
| Truncated LCG | State recurrence plus missing low/high bits | Treating returned output as full state |
| LWE | `b = A*s + e mod q` | Incorrect centered residues or error scale |
| Approximate GCD | Samples `p*q_i + r_i` with small `r_i` | Residuals too large for the assumed bound |
| Subset sum | `sum(a_i*x_i) = target`, `x_i in {0,1}` | Losing the binary constraint after reduction |
| GGH | Ciphertext near a lattice point | Confusing basis coordinates with ambient coordinates |
| NTRU | Polynomial relation with short private polynomials | Wrong cyclic/negacyclic convolution |
| Orthogonal/HSSP families | Hidden structure orthogonal to supplied samples | Too few independent samples |

On **Kali**, inspect the installed checkout locally:

```bash
rg --files /opt/tools/crypto-attacks | rg 'hidden_number|lwe|coppersmith|knapsack|lcg'
```

Read the selected function, its examples, and imports. Inputs and dependencies are not uniform across attacks. If Sage is unavailable, basic exact arithmetic remains usable, but a high-dimensional lattice attack may be blocked by the environment. Record that honestly rather than silently using an online solver.

Ring-LWE and Module-LWE can be flattened into matrices, but only with the correct coefficient ordering and ring reduction. In `Zq[x]/(x^n+1)`, wraparound changes sign. Structured flattening does not make secure ML-KEM parameters easy to solve.

BDD predicates and LadderLeak-style leakage use additional side information, not just a generic lattice basis. Count how much information each signature gives and whether the predicate is reliable. A tiny bias may require substantially more samples than a full known nonce bit.

## 11. Post-quantum recognition without misleading promises

ML-KEM/Kyber hints include module vectors, polynomial degree 256, modulus 3329, NTT operations, and compression. ML-DSA/Dilithium uses a different modulus and signature structure. Confirm the source instead of classifying by a single constant.

Look for challenge-specific departures: unusually tiny dimensions, exposed noise, repeated randomness, unchecked verification fields, corrupted signatures, or implementation faults. Kannan embeddings, algebraic Arora–Ge models, and primal/dual estimators answer different questions. An estimator predicts cost; it does not recover a secret.

MAYO and other multivariate signatures require the actual public polynomial system and fault model. A malformed signature only helps if it reveals a relation to secret structure. Keep the mathematics local; AI/ML libraries remain forbidden even when a cryptographic scheme has a similar abbreviation.

## 12. Shamir and CRT secret sharing

Save as `shamir_toy.py`:

```python
prime = 2089
secret = 1234

def polynomial(x):
    return (secret + 17*x + 29*x*x) % prime

shares = [(x, polynomial(x)) for x in [1, 2, 3]]
recovered = 0
for i, (xi, yi) in enumerate(shares):
    basis = 1
    for j, (xj, _) in enumerate(shares):
        if i != j:
            basis = basis * (-xj) * pow(xi-xj, -1, prime) % prime
    recovered = (recovered + yi*basis) % prime
assert recovered == secret
print(recovered)
```

Repeated x-coordinates do not add independent shares. Deterministic coefficients or polynomial reuse across sessions can create extra equations; compare coefficients/outputs algebraically rather than assuming all same-threshold schemes are vulnerable.

Asmuth–Bloom uses a different CRT-based construction with size inequalities. Recovering a congruence class is not enough if several candidates remain within the allowed secret range. Check those bounds explicitly.

## 13. Authenticated encryption and reduced-round designs

GCM nonce reuse repeats CTR keystream and creates equations involving GHASH's authentication subkey. GHASH works in `GF(2^128)` with a specified bit convention; integer arithmetic modulo a large prime is not interchangeable. Full/partial tags, associated data, ciphertext lengths, and multiple polynomial roots all affect recovery.

ChaCha20-Poly1305 reuse involves a reused one-time Poly1305 key and stream. Poly1305 arithmetic is modulo `2^130-5`, while the final tag reduction and clamping add constraints. Recover candidate keys from complete message/tag equations and validate on a second independent pair before forging a toy message. A ciphertext XOR alone does not recover a valid tag.

Partitioning oracles and non-key-committing AEAD need a verifier that reveals which candidate key accepts a crafted ciphertext. Establish the acceptance predicate and candidate key set. They are not a generic way to crack arbitrary AEAD passwords.

Reduced-round AES Square attacks require chosen plaintext sets with the required balanced structure. S-box intersection needs controlled differences and an identifiable round boundary. Non-permutation S-boxes can yield collisions, but the collision must survive the surrounding rounds. ForkAES reflective differentials and faulty ChaCha rotations similarly require the exact modified construction.

For sponge designs, record rate, capacity, permutation, domain separation, padding, and round count. Keccak, Ascon, Gimli, and Sparkle are not interchangeable. A small-capacity meet-in-the-middle toy does not imply an attack on a full-strength standardized hash.

## 14. RSA oracles: define the predicate precisely

| Oracle | Predicate | Suitable next step |
|---|---|---|
| Parity/LSB | Decrypted integer is even/odd | Multiply ciphertext by `2^e`; maintain exact rational/integer intervals |
| PKCS#1 v1.5 | Plaintext is a conforming `00 02 ... 00 ...` block | Bleichenbacher interval search with the actual full validation predicate |
| Leading-byte/OAEP | Decrypted representative is below a boundary | Manger-style interval narrowing only if that predicate is observable |
| Noisy bit | Correct predicate with measurable error | Repeated controls, confidence estimate, and error-correcting recovery |
| Timing | Distribution depends on an internal operation | Collect matched controls; confirm relation before recovery |

An error string may combine several rejection stages. If the service checks a hash, length, padding, and text decoding, identify which stage creates the signal. Bleichenbacher and Manger are query-sensitive; estimate the budget before committing.

Use exact fractions or integer intervals, never floating-point bounds. At the end, search the tiny remaining interval and re-encrypt every candidate. With noisy observations, retain uncertainty or backtrack rather than allowing one wrong bit to corrupt the whole result.

## 15. Zero-knowledge proofs, signatures, and garbled circuits

Start by identifying the statement the verifier actually checks. Record public inputs, witness-dependent commitments, challenge derivation, transcript order, and state update. The challenge may be in the protocol wrapper rather than the proof system.

| Source topic | Diagnostic | Constraint |
|---|---|---|
| Schnorr-style proof replay | Compare commitment/challenge/response across sessions | Reused commitment with distinct challenges can expose a witness |
| Fiat–Shamir mistakes | Recompute the transcript hash locally | Missing identity, statement, or commitment binding creates a specific gap |
| Groth16 setup degeneration | Inspect provided verifying/proving key relations | A relation such as equal setup elements needs its exact pairing equation |
| Unconstrained nullifier | Compare circuit inputs with state replay checks | Valid proof does not imply a unique authorized action |
| KZG/pairing oracle | Write the accepted pairing identity | Need the actual oracle outputs and algebraic relation |
| DV-SNARG verifier oracle | Determine precisely what is queryable | A boolean verifier alone may not reveal useful linear data |
| FROST threshold signing | Track participant IDs, nonce commitments, binding factors | FROST is a threshold Schnorr protocol, not inherently a lattice scheme |
| Free-XOR garbled circuits | Compare label pairs for shared global delta | Access to a matching label pair or leaked metadata is required |

The source's FROST heading can mislead: classify the concrete construction from its equations, not that label. Likewise, a proof accepted once does not prove arbitrary proof forgery; replay and unconstrained public input are separate findings.

Graph three-coloring and other constraint puzzles can be modelled with a non-AI SMT library if available under the Python-library rule. Bound every variable and verify the model against the original checker. Bit-vectors use fixed-width arithmetic; integers do not overflow unless explicitly constrained.

## 16. Unusual algebra: reduce to something measurable

| Construction in the sources | First diagnostic | Useful next action |
|---|---|---|
| Paillier/homomorphic oracle | Verify additive homomorphism on toy messages | Determine whether size, parity, or comparison leaks plaintext information |
| ElGamal | Check group order and public element order | Trivial `p-1` elements leak only a small class; use the actual order |
| Matrix ElGamal/Cayley–Purser | Compute characteristic polynomial and centralizers | Test whether conjugation invariants reduce the secret search |
| Tropical semiring | Confirm min-plus or max-plus convention | Residuation solves inequalities; verify equality separately |
| Braid-group DH | Identify computable representation/invariant | Test whether Alexander polynomial or another invariant preserves needed structure |
| Permutation/icosahedral group | Express generators as explicit permutations | Enumerate the finite subgroup and map ciphertext action |
| Monotone function | Prove direction and domain bounds | Binary search, with exact comparisons and truncation accounted for |
| Goldwasser–Micali | Identify quadratic-residuosity encoding | Replication helps only with a matching acceptance oracle |
| BB84 simulation | Trace basis choices, sifting, and authentication | Unauthenticated classical exchange differs from breaking quantum mechanics |
| Differential-privacy noise | Check whether repeated samples share a secret and independent noise | Estimate with uncertainty; bounded query budget and correlated noise matter |

For a matrix or exotic group, verify the operation, identity, inverse, and order on small examples before porting an integer attack. Singular matrices and noncommutative multiplication can invalidate familiar formulas.

BIP39 partial-mnemonic puzzles combine a finite word-index space, checksum bits, and often a known address. Recover only organizer-provided toy wallets. Do not query public wallet services with private material; checksum acceptance alone does not establish the target wallet.

## 17. Historical, media, and error-correcting crypto

Lorenz/Tunny and rotating-wheel ciphers need their alphabet encoding, wheel lengths, stepping rules, and alignment. Start with a short known plaintext and check wheel motion; do not apply ordinary Vigenère frequency analysis to teleprinter bits unchanged.

Hamming codes and interleaving are error correction, not encryption. Identify codeword size, parity placement, and interleaver permutation; compute syndromes on a few known words before decoding an entire file. Nibble-reassembly and random-padding formats similarly need a field layout before byte reconstruction.

For image shifts, grid permutations, and Arnold-cat-map scrambling, preserve dimensions and distinguish coordinate transforms from pixel-value transforms. Check one round on a coordinate grid, then invert it. A visually plausible image can still be mirrored or shifted by one pixel.

## 18. Stopping rules that save time

Stop an attack branch when its required structure is absent, its query budget exceeds the challenge limit, or a small known-secret instance fails. Record the failed condition. Continue with a different mathematically supported branch rather than increasing concurrency or switching to prohibited online analysis.

Before accepting a result, validate it outside the solver: re-encrypt, recompute signatures, regenerate outputs, satisfy the original polynomial equations, or run the challenge's local checker. A lattice vector, SMT model, root, or decoded string is only a candidate until it passes that check.

</details>
