# Cryptography: recover the structure before the secret

**Quick route:** [Short commands](../QUICKSTART.md#rsa) · [Tool strengths and weaknesses](../TOOL-CHOOSER.md#cryptography). Use this chapter for deeper explanations.

A crypto challenge usually supplies an algorithm, parameters, ciphertext, or a query service. Your first task is to translate those into an exact mathematical statement. A recognizable number size or file extension is a clue; it is not an attack.

This chapter gives runnable local examples for common cases. [Advanced cryptography](14-advanced-crypto.md) preserves the repository's lattice, elliptic-curve, polynomial, proof-system, post-quantum, and unusual algebra topics with diagnostics and constraints.

## 1. Environment and notation

**Windows:** open WSL and use the listed Python 3, OpenSSL, and RsaCtfTool installations. Native Windows Python is not assumed. **Kali:** Python is used throughout; the sheet lists crypto-attacks at `/opt/tools/crypto-attacks`, hlextend, hashcat, John, and other tools. Check the actual interpreter and tool before relying on them.

SageMath is approved on Kali, but its installation details are blank. Try `sage --version`; use the standard-library routes for basic arithmetic if absent. PDF p.5 permits non-AI dependencies in both environments; [package setup](00-tool-rules.md#non-ai-python-package-checks) explains the limits. Named rejected tools and online services remain excluded.

Factordb-python is listed on Kali. That is not authorization to send challenge moduli to the FactorDB website. Keep factoring local. Do not use online hash-cracking, online mathematical solvers, AI tools, or public challenge uploads.

```bash
python3 --version
python3 -c "import sys; print(sys.executable); print(pow(3, -1, 11))"
```

Expected inverse: `4`, because `3*4 % 11 == 1`. Modular inverses require coprime inputs; an exception is meaningful evidence, not a reason to switch to floating point.

| Symbol | Meaning | Common error |
|---|---|---|
| `n` | RSA modulus or a group order, depending on context | Confusing the field prime with the subgroup order |
| `p`, `q` | Usually primes | Assuming repeated or composite factors are impossible |
| `e`, `d` | Public and private exponents | Inverting modulo `n` instead of the appropriate group exponent |
| `m`, `c` | Integer message and ciphertext | Losing leading zero bytes |
| `k` | Nonce, key, or multiplier | Reusing a variable for unrelated quantities |
| `^` | XOR in Python; exponentiation in Sage preparsed files | Copying syntax between interpreters |

Every Python block with a filename below is a complete local demonstration. Save it and run `python3 filename.py`. Replace toy values only after the assertions pass.

## 2. Triage worksheet

Record these before choosing an attack:

```text
Artifact: source / text / binary / capture / query service
Encoding: hex / base64 / decimal integers / raw bytes
Known values: ______________________________
Unknown values: ____________________________
Equation or state update: __________________
Oracle input and exact response: ___________
Query limit / reset behavior: ______________
Verification equation: _____________________
```

Read source in execution order. Trace key generation, serialization, padding, nonce generation, encryption/signing, and verification. Check whether two apparently separate operations share a secret or RNG state. A cryptographically strong primitive can be surrounded by a weak protocol.

| Observation | First local check | Next branch |
|---|---|---|
| Small `e`, short unpadded message | Exact integer root | RSA low-exponent section |
| Several RSA moduli | Pairwise GCD | Shared factors |
| Several encryptions of the same message | Compare modulus/exponent relationships | Common modulus or broadcast |
| Repeated nonce or IV | Compare ciphertext XOR and tags | Stream or authenticated-encryption analysis |
| Equal 16-byte ciphertext blocks | Count block repetitions | ECB hypothesis |
| Distinct decryption errors | Repeat controlled malformed samples | Padding/error oracle |
| Repeated signature `r` | Compare messages and signatures | Nonce reuse |
| Numeric outputs from a PRNG | Check exact bit widths and output transformation | LCG, MT, LFSR, or constraint model |
| Approximate linear equations modulo `q` | Estimate error bound | Lattice chapter |

## 3. Bytes, integers, and encodings

Save as `bytes_basics.py`:

```python
import base64

original = b'\x00CTF{toy}'
value = int.from_bytes(original, 'big')
recovered = value.to_bytes(len(original), 'big')
assert recovered == original
assert bytes.fromhex(original.hex()) == original
assert base64.b64decode(base64.b64encode(original), validate=True) == original
print(original.hex())
print(value)
print(recovered)
```

Expected final line: `b'\x00CTF{toy}'`. If you choose output length solely from `bit_length`, the initial zero disappears. For RSA, use the modulus byte length when inspecting padded plaintext; trim only after recognizing the padding format.

Hex and base64 are encodings, not encryption. Decode one layer into a new file and inspect its header and length. Arbitrarily repeating decoders can turn random data into misleading printable fragments.

## 4. Classical ciphers and XOR

For substitution and transposition, preserve punctuation, spacing, alphabet, and repeated groups. Compare character frequencies and repeated distances. A long alphabetic text supports frequency analysis; a short random flag often does not.

For Vigenère, test plausible key lengths using repeated distances and coincidence statistics, then analyze each residue class separately. For book ciphers, establish the exact edition, tokenization, indexing base, and whether punctuation counts. For Polybius/Nihilist/pigpen/semaphore, identify the symbol alphabet before forcing ASCII.

Save as `xor_known_plaintext.py`:

```python
def xor(a, b):
    if len(a) != len(b):
        raise ValueError('equal lengths required')
    return bytes(x ^ y for x, y in zip(a, b))

key = b'ICE'
plain = b'CTF{repeat_xor_is_not_a_pad}'
cipher = bytes(c ^ key[i % len(key)] for i, c in enumerate(plain))
known = b'CTF'
recovered_key = xor(cipher[:len(known)], known)
recovered = bytes(c ^ recovered_key[i % len(recovered_key)]
                  for i, c in enumerate(cipher))
assert recovered_key == key
assert recovered == plain
print(recovered.decode())
```

This works because the known plaintext covers the entire repeating key at the correct alignment. If the key is longer, those bytes reveal only part of it. Validate a candidate key against file structure, checksum, or several independent known bytes, not just a guessed flag prefix.

For single-byte XOR, all 256 candidates are cheap locally. Score printable text and expected structure; do not select the first candidate containing a brace. For repeating XOR, compare several key lengths and penalize overly long keys that merely fit a guessed prefix.

### Reused one-time pad or stream nonce

For equal-length streams, `c1 XOR c2 = p1 XOR p2`. It removes the reused keystream, not both plaintexts at once.

Save as `reused_stream.py`:

```python
from hashlib import sha256

def xor(a, b):
    assert len(a) == len(b)
    return bytes(x ^ y for x, y in zip(a, b))

p1 = b'known message 01'
p2 = b'secret message!!'
assert len(p1) == len(p2)
stream = sha256(b'toy reused stream').digest()[:len(p1)]
c1, c2 = xor(p1, stream), xor(p2, stream)
recovered = xor(xor(c1, c2), p1)
assert recovered == p2
print(recovered)
```

If output is nonsense, check offsets, encoding, compression, and whether nonce reuse actually produced the same key stream. Load-balanced servers may use different keys or counters; group samples by backend evidence before comparing them.

## 5. Reusable exact arithmetic

Save this as `math_helpers.py`. Later examples import it from the same directory.

```python
from math import gcd, prod

def iroot(value, degree):
    """Return floor(value**(1/degree)) using integer arithmetic."""
    if value < 0 or degree < 1:
        raise ValueError('nonnegative value and positive degree required')
    lo, hi = 0, 1
    while hi ** degree <= value:
        hi *= 2
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid ** degree <= value:
            lo = mid
        else:
            hi = mid
    return lo

def egcd(a, b):
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r:
        q = old_r // r
        old_r, r = r, old_r - q*r
        old_s, s = s, old_s - q*s
        old_t, t = t, old_t - q*t
    return old_r, old_s, old_t

def crt(residues, moduli):
    if len(residues) != len(moduli) or not moduli:
        raise ValueError('one residue per modulus required')
    for i, a in enumerate(moduli):
        if a <= 1 or any(gcd(a, b) != 1 for b in moduli[:i]):
            raise ValueError('pairwise coprime moduli greater than one required')
    total = prod(moduli)
    result = 0
    for residue, modulus in zip(residues, moduli):
        partial = total // modulus
        result += residue * partial * pow(partial, -1, modulus)
    return result % total

if __name__ == '__main__':
    assert iroot(27, 3) == 3 and iroot(28, 3) == 3
    assert iroot(0, 3) == 0
    assert crt([2, 3, 2], [3, 5, 7]) == 23
    g, a, b = egcd(17, 13)
    assert g == 1 and 17*a + 13*b == 1
    print('exact arithmetic checks passed')
```

Run `python3 math_helpers.py`. Never use `int(c ** (1/3))` on large RSA integers: floating-point precision makes it unreliable.

## 6. RSA with known factors

Save as `rsa_known_factors.py`:

```python
from math import gcd, lcm

p, q, e = 61, 53, 17
n = p*q
lam = lcm(p-1, q-1)
assert gcd(e, lam) == 1
d = pow(e, -1, lam)
m = 65
c = pow(m, e, n)
recovered = pow(c, d, n)
assert p*q == n
assert recovered == m
assert pow(recovered, e, n) == c
print(n, c, recovered)
```

Expected output: `3233 2790 65`. Re-encryption is the essential verification. For multiple distinct primes, use the LCM of each `p_i-1`. For repeated prime powers, use the correct totient/group structure; `(p-1)*(q-1)` is wrong when `p == q`.

If `gcd(e, lambda(n)) != 1`, there is no unique private exponent of this form. Factor the modulus and recover all appropriate roots; select using format and re-encryption. See the advanced chapter rather than silently choosing an invalid inverse.

### Shared factors and close primes

Save as `rsa_factor_checks.py`:

```python
from math import gcd, isqrt

moduli = [101*113, 101*127, 131*137]
hits = []
for i, n in enumerate(moduli):
    for j in range(i):
        p = gcd(n, moduli[j])
        if 1 < p < n:
            hits.append((j, i, p))
assert hits == [(0, 1, 101)]
print('shared:', hits)

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

factors = fermat(1009*1013)
assert factors == (1009, 1013)
print('close primes:', factors)
```

For many keys, pairwise GCD is quadratic; use a local batch-GCD implementation from approved crypto-attacks after validating its inputs. Duplicate moduli produce `gcd == n`, which is not a new factor. Fermat is useful when primes are close; an exhausted budget is a reason to pivot.

### Small exponent, common modulus, broadcast

Save as `rsa_structural.py`, beside `math_helpers.py`:

```python
from math_helpers import iroot, egcd, crt

# Case 1: no modular wraparound.
m, e, n = 42, 3, 1000003*1000033
c = pow(m, e, n)
root = iroot(c, e)
assert root**e == c and root == m
print('small exponent:', root)

# Case 2: same message and modulus, coprime exponents.
n, e1, e2, m = 101*113, 3, 7, 42
c1, c2 = pow(m, e1, n), pow(m, e2, n)
g, a, b = egcd(e1, e2)
assert g == 1
recovered = pow(c1, a, n) * pow(c2, b, n) % n
assert recovered == m
assert pow(recovered, e1, n) == c1
print('common modulus:', recovered)

# Case 3: same unpadded message under three coprime moduli.
moduli = [101*113, 107*131, 137*149]
m, e = 42, 3
cs = [pow(m, e, modulus) for modulus in moduli]
combined = crt(cs, moduli)
recovered = iroot(combined, e)
assert recovered**e == combined and recovered == m
assert all(pow(recovered, e, modulus) == ci
           for modulus, ci in zip(moduli, cs))
print('broadcast:', recovered)
```

Small `e` alone is insufficient: padding or modular wraparound defeats the first check. The common-modulus script needs invertible ciphertexts for negative exponents; a failed inverse may expose a factor through GCD. Broadcast needs the same integer message and enough combined modulus size. Randomized padding breaks that assumption.

### Textbook RSA multiplicativity

Save as `rsa_blinding_toy.py`:

```python
from math import gcd

p, q, e = 61, 53, 17
n = p*q
d = pow(e, -1, (p-1)*(q-1))
message = 65
ciphertext = pow(message, e, n)
factor = 2
assert gcd(factor, n) == 1
modified = ciphertext * pow(factor, e, n) % n

def toy_decrypt_oracle(c):
    return pow(c, d, n)

answer = toy_decrypt_oracle(modified)
recovered = answer * pow(factor, -1, n) % n
assert recovered == message
print(recovered)
```

This models an oracle that refuses one ciphertext but decrypts related ciphertexts. Proper padding and protocol validation change the available oracle. Never assume a signing oracle accepts arbitrary integers; inspect hashing and encoding first.

### RsaCtfTool without accidental online analysis

On **Windows WSL**, locate the supplied RsaCtfTool entry point and read its local help. Inspect a PEM public key with the listed OpenSSL:

```bash
openssl pkey -pubin -in public.pem -text -noout
```

Expected fields include the modulus and exponent. Choose a local attack matching an observed property, such as close primes or shared factors. Do not launch an all-attacks mode without checking whether it includes network-backed factoring. If the entry point is absent, extract the numbers from supplied text and use the scripts above.

## 7. Block modes: distinguish confidentiality from integrity

For AES the block size is 16 bytes. ECB encrypts equal plaintext blocks to equal ciphertext blocks under the same key. CBC combines each plaintext block with the previous ciphertext block (or IV). CTR and OFB generate a stream that is XORed with plaintext.

Save as `block_repetitions.py` and pass a raw ciphertext filename:

```python
from collections import Counter
from pathlib import Path
import sys

data = Path(sys.argv[1]).read_bytes()
for offset in range(16):
    blocks = [data[i:i+16] for i in range(offset, len(data)-15, 16)]
    repeats = sum(count-1 for count in Counter(blocks).values() if count > 1)
    if repeats:
        print('offset', offset, 'repeated blocks', repeats)
```

Repeated blocks are evidence of deterministic block behavior, not a complete ECB proof. File headers, duplicated chunks, and framing can create repetitions too. With a chosen-plaintext oracle, compare ciphertext for repeated aligned input blocks.

### CBC bit flipping without an AES dependency

The relation is `P_i = D(C_i) XOR C_(i-1)`. Changing the previous block by `old XOR wanted` changes the targeted plaintext bytes. The previous plaintext block is usually corrupted; changing the IV targets the first block without that side effect.

Save as `cbc_relation.py`:

```python
def xor(a, b):
    assert len(a) == len(b)
    return bytes(x ^ y for x, y in zip(a, b))

# A fixed hypothetical decrypted block D(C1), not an AES implementation.
intermediate = bytes(range(16))
original = b'admin=0;uid=1000'
desired = b'admin=1;uid=1000'
iv = xor(intermediate, original)
modified_iv = xor(iv, xor(original, desired))
assert xor(intermediate, iv) == original
assert xor(intermediate, modified_iv) == desired
print(xor(intermediate, modified_iv))
```

Expected output contains `admin=1`. An authenticated ciphertext should be rejected after modification. If a challenge uses a CRC instead of a MAC, analyze that CRC separately; arbitrary CRC updates do not bypass a real authentication tag.

### ECB suffix recovery: runnable oracle rehearsal

The following uses a deterministic block transform to demonstrate byte alignment and dictionary matching. It is not AES and is not a cryptographically secure encryption implementation. The same equality logic applies to a deterministic ECB oracle with a fixed unknown suffix.

Save as `ecb_suffix_toy.py`:

```python
from hashlib import sha256

BLOCK = 16
secret = b'CTF{ecb_demo}'
key = b'local toy key'

def oracle(prefix):
    data = prefix + secret
    pad = BLOCK - len(data) % BLOCK
    data += bytes([pad]) * pad
    return b''.join(sha256(key + data[i:i+BLOCK]).digest()[:BLOCK]
                    for i in range(0, len(data), BLOCK))

base_length = len(oracle(b''))
growth = next(i for i in range(1, BLOCK+1)
              if len(oracle(b'A'*i)) > base_length)
secret_length = base_length - growth
known = b''
for index in range(secret_length):
    prefix = b'A' * (BLOCK-1-index % BLOCK)
    block_index = index // BLOCK
    start = block_index * BLOCK
    target = oracle(prefix)[start:start+BLOCK]
    matches = []
    for candidate in range(256):
        sample = oracle(prefix + known + bytes([candidate]))
        if sample[start:start+BLOCK] == target:
            matches.append(candidate)
    assert len(matches) == 1
    known += bytes([matches[0]])
assert known == secret
print(known)
```

Failure usually means a changing key, unknown prefix, randomized encryption, wrong block size, compression, or a query limit. Determine whether the prefix is fixed or changes per request before trying to align it. Do not send the toy loop to a remote service until its oracle model and allowed query budget are established.

## 8. Padding and error oracles

A CBC padding oracle reveals whether modified plaintext has valid padding. First distinguish padding rejection from authentication rejection, JSON parsing, UTF-8 decoding, or normal application errors. Repeat controls: one noisy error is insufficient.

This complete local simulator recovers a 16-byte intermediate value using only a padding-validity function. Save as `padding_oracle_toy.py`:

```python
BLOCK = 16
intermediate = bytes([91, 2, 77, 18, 200, 17, 9, 55, 66, 7, 33, 111, 8, 4, 3, 2])
plain = b'CTF{oracle_demo}'
assert len(plain) == BLOCK
original_previous = bytes(a ^ b for a, b in zip(intermediate, plain))
queries = 0

def valid_padding(chosen_previous):
    global queries
    queries += 1
    candidate = bytes(a ^ b for a, b in zip(intermediate, chosen_previous))
    length = candidate[-1]
    return 1 <= length <= BLOCK and candidate[-length:] == bytes([length])*length

recovered = bytearray(BLOCK)
for index in range(BLOCK-1, -1, -1):
    pad = BLOCK-index
    probe = bytearray(BLOCK)
    for j in range(index+1, BLOCK):
        probe[j] = recovered[j] ^ pad
    found = []
    for guess in range(256):
        probe[index] = guess
        if not valid_padding(probe):
            continue
        # Reject accidental padding longer than the intended suffix.
        if index > 0:
            probe[index-1] ^= 1
            still_valid = valid_padding(probe)
            probe[index-1] ^= 1
            if not still_valid:
                continue
        found.append(guess ^ pad)
    assert len(found) == 1, (index, found)
    recovered[index] = found[0]

result = bytes(a ^ b for a, b in zip(recovered, original_previous))
assert bytes(recovered) == intermediate
assert result == plain
print(result, 'queries:', queries)
```

This simulates one block, not a network exploit. To adapt it, preserve the full protocol framing, determine which block is actually decrypted, and confirm that a MAC is not checked first. False positives at padding length 1 need the second probe shown above. UTF-8 or application-format oracles require different logic.

RSA PKCS#1 v1.5 and OAEP-leading-byte oracles use multiplicative interval narrowing, not CBC byte flipping. Record the exact predicate before using a Bleichenbacher or Manger implementation from approved local crypto-attacks. See the advanced chapter for the distinction.

## 9. Hashes, MACs, CRCs, and compression

Hash length is not an algorithm identifier. Compare source, field names, encoding, salt placement, and known test values. A 32-character hex string might be MD5, a random token, or truncated output from another function.

Length extension applies to constructions such as certain Merkle–Damgård hashes of `secret || message`. It does not apply to HMAC simply because HMAC uses the same hash internally. You need the original digest, original message, a secret-length hypothesis, and an application parser that accepts the required glue padding.

**Kali:** hlextend is listed, but check its installed API locally before use:

```bash
python3 -c "import hlextend; help(hlextend)"
```

Start with a toy local verifier and verify the extended digest exactly before querying a challenge. Hash length extension does not decrypt a message and does not recover the secret.

For a custom XOR-aggregate hash or linear MAC, express each known message/signature pair as equations over the correct field. CRC32 is affine for fixed conventions and message lengths; bit order, initial state, and final XOR matter. Compare equal-length messages and verify any proposed correction with the same CRC implementation.

For compression side channels, measure compressed length before encryption noise if the interface permits. Keep secret context and chosen prefix adjacent, repeat samples, and compare candidates of equal input length. Padding, random prefixes, different compression dictionaries, and state resets can hide the signal.

Collision and preimage are different goals. A collision for two chosen files is not a preimage for a fixed digest. A published SHA-1 collision pair does not automatically produce a chosen-prefix collision for an arbitrary challenge document.

## 10. Diffie–Hellman and signature nonces

For finite-field DH, record `p`, generator `g`, both public keys, and whether private keys persist. Check trivial generator values, group order factors, and validation of peer public values.

Save as `dh_toy.py`:

```python
p, g, alice, bob = 1019, 2, 123, 456
A, B = pow(g, alice, p), pow(g, bob, p)
shared_a, shared_b = pow(B, alice, p), pow(A, bob, p)
assert shared_a == shared_b
print('shared:', shared_a)

for bad_g in [0, 1, p-1]:
    possibilities = {pow(bad_g, exponent, p) for exponent in range(1, 12)}
    print('generator', bad_g, 'public possibilities', sorted(possibilities))
assert {pow(p-1, exponent, p) for exponent in range(1, 12)} == {1, p-1}
```

Small-subgroup confinement needs an accepted low-order public value, a persistent secret, and an observable response that distinguishes candidate shared secrets. One oracle output with an ephemeral secret does not accumulate CRT information across sessions.

For DSA/ECDSA, repeated nonce `k` can expose the private key. The modular arithmetic below is common to both signature equations, using a toy subgroup order. It does not generate an elliptic-curve point.

Save as `nonce_reuse.py`:

```python
n = 1019
private, nonce, r = 123, 77, 456
h1, h2 = 100, 200
s1 = pow(nonce, -1, n) * (h1 + r*private) % n
s2 = pow(nonce, -1, n) * (h2 + r*private) % n
recovered_nonce = (h1-h2) * pow(s1-s2, -1, n) % n
recovered_private = (s1*recovered_nonce-h1) * pow(r, -1, n) % n
assert recovered_nonce == nonce
assert recovered_private == private
assert s1*nonce % n == (h1+r*private) % n
assert s2*nonce % n == (h2+r*private) % n
print(recovered_nonce, recovered_private)
```

Use the subgroup order, not the curve field prime. Match the real message hash truncation. ECDSA low-s normalization may require trying sign variants. Validate the recovered private key against the published public key. Ed25519 uses different encoding and scalar derivation; do not paste ECDSA code into it unchanged.

## 11. Predictable randomness

Identify the generator and its output transformation. Record how many hidden draws occur between observations. Timestamp seeds, truncated outputs, floating-point conversion, rejection sampling, and modulo reduction change the attack.

### LCG recovery and backward stepping

Save as `lcg_recovery.py`:

```python
from math import gcd

modulus, multiplier, increment = 1009, 65, 17
states = [123]
for _ in range(7):
    states.append((multiplier*states[-1]+increment) % modulus)

d1 = (states[1]-states[0]) % modulus
d2 = (states[2]-states[1]) % modulus
assert gcd(d1, modulus) == 1
a = d2 * pow(d1, -1, modulus) % modulus
c = (states[1]-a*states[0]) % modulus
assert (a, c) == (multiplier, increment)
assert all((a*x+c) % modulus == y for x, y in zip(states, states[1:]))
previous = (states[1]-c) * pow(a, -1, modulus) % modulus
assert previous == states[0]
print('a, c, previous:', a, c, previous)

# Unknown modulus: differences produce multiples of the modulus.
diffs = [y-x for x, y in zip(states, states[1:])]
candidate = 0
for x, y, z in zip(diffs, diffs[1:], diffs[2:]):
    candidate = gcd(candidate, abs(x*z-y*y))
assert candidate % modulus == 0
print('modulus multiple:', candidate)
```

The GCD may be a multiple of the modulus. Filter candidates using all observations and known bounds. If a difference is not invertible, solve the resulting congruence rather than discarding the case. Truncated outputs need a different model, often constraints or a lattice.

### Time seeds and generator matching

Bound the seed window using challenge timestamps; reproduce the exact language/runtime PRNG. Python `random`, libc `rand`, Java's LCG, and browser `Math.random` are not interchangeable. Use a known output sequence to verify the generator before testing a derived key.

For MT19937, enough full consecutive outputs permit state reconstruction after undoing tempering. Python floating outputs combine parts of multiple draws; they are not full 32-bit words. A tool that expects 624 raw words cannot accept decimal floats unchanged.

PCG, xorshift, xoroshiro, and xoshiro have distinguishable state transitions and output scramblers. Read constants and rotation amounts from source. Chaotic maps also depend on floating-point precision; mathematically similar real-valued recurrences can produce different byte streams.

LFSR output is linear only when the observed output is a linear state function. Filtered or combined LFSRs require correlation, algebraic, or constraint techniques. See the advanced chapter for a tested Berlekamp–Massey example.

## 12. A disciplined finish

Check the recovered object in the original equation: re-encrypt plaintext, verify a signature, regenerate observed RNG outputs, or reproduce the tag. Plausible English is not enough. Keep the original bytes, parameters, solver assumptions, and a minimal script with assertions.

If a solver stalls, reduce a toy instance first. Wrong endianness, the wrong modulus, row/column conventions, hidden random draws, noninvertible values, and incorrect oracle definitions are more common than missing brute-force capacity.

The chapter merges the source skill overview, classic/historical ciphers, RSA, DH, PRNG, stream, modern-mode and MAC notes. Specialized topics continue in [Advanced cryptography](14-advanced-crypto.md); every crypto source file has a disposition in the coverage manifest.
