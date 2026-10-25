# Cryptography

Run Bash blocks in the named environment from the extracted guide root. Set each `FILE` to your supplied artifact; outputs are working copies. [Full reference](../reference/chapters/07-cryptography.md) · [Tool chooser](../TOOL-CHOOSER.md#cryptography).

## Quick: inspect a public key

**WSL · OpenSSL.** Input: PEM public key.

```bash
FILE='public.pem'
openssl pkey -pubin -in "$FILE" -text -noout
```

**Look for:** modulus, exponent, key type and size.
**If not:** a certificate needs `openssl x509`; raw integers belong in the RSA JSON below.

## Quick: decode bytes before attacking them

**WSL · Python 3.** Input: Base64 text; recipe also recognizes one gzip/zlib layer. Choose a new output directory each run.

```bash
FILE='message.txt'
python3 recipes/layers.py "$FILE" --out crypto-decoded
```

For plain hexadecimal text:

```bash
FILE='hex.txt'
python3 - "$FILE" <<'PY'
from pathlib import Path
import sys
data = bytes.fromhex(Path(sys.argv[1]).read_text())
Path('hex-decoded.bin').write_bytes(data)
print(len(data), repr(data[:160]))
PY
```

**Look for:** recognizable headers or plaintext.
**If not:** inspect the new bytes; another decoder needs supporting evidence.

## Quick: decrypt RSA with known or close factors

**WSL · Python 3.** Create `rsa.json` using supplied integers: `n`, `e`, `c`, optional prime factors `p`, `q`, optional plaintext byte `length`. This toy returns `A`:

```bash
cat > rsa-toy.json <<'JSON'
{"n":3233,"e":17,"c":2790,"p":61,"q":53,"length":1}
JSON
python3 recipes/rsa.py rsa-toy.json --out rsa-toy.bin
```

Without factors, the recipe tries bounded Fermat factoring:

```bash
FILE='rsa.json'
python3 recipes/rsa.py "$FILE" --steps 100000 --out rsa-plain.bin
```

**Look for:** `re-encryption: OK` and sensible bytes; padding remains intact.
**If not:** check distinct prime factors, encoding, or the next RSA branches.

## Quick: find a shared RSA prime

**WSL · Python 3.** Input: one decimal modulus per line in `moduli.txt`.

```bash
FILE='moduli.txt'
python3 - "$FILE" <<'PY'
from pathlib import Path
from math import gcd
import sys
ns = [int(s) for s in Path(sys.argv[1]).read_text().split()]
for i, n in enumerate(ns):
    for j, other in enumerate(ns[:i]):
        p = gcd(n, other)
        if 1 < p < min(n, other):
            print('rows', j+1, i+1, 'p', p, 'q', n//p)
PY
```

**Look for:** a proper factor; put it and `n//p` into your RSA JSON.
**If not:** duplicate moduli reveal no new factor; inspect exponent/message reuse.

## Quick: test an unpadded small exponent

**WSL · Python 3.** Input: `rsa.json` with integer `n`, `e`, `c`; bounded to `e <= 17`.

```bash
FILE='rsa.json'
python3 - "$FILE" <<'PY'
import json, sys
from pathlib import Path
d = json.loads(Path(sys.argv[1]).read_text())
n, e, c = (int(d[k]) for k in ('n', 'e', 'c'))
assert n > 1 and 2 <= e <= 17 and 0 <= c < n
lo, hi = 0, 1 << ((c.bit_length()+e-1)//e)
while lo < hi:
    mid = (lo+hi+1)//2
    if mid**e <= c: lo = mid
    else: hi = mid-1
if lo**e == c:
    print(lo.to_bytes(max(1, (lo.bit_length()+7)//8), 'big'))
else: print('No exact root: padding or modular wraparound may apply')
PY
```

**Look for:** an exact root with meaningful bytes.
**If not:** small `e` alone is insufficient; use the reference for broadcast/common-modulus cases.

## Quick: rank single-byte XOR candidates

**WSL · Python 3.** Input: raw ciphertext, already decoded from hex/Base64.

```bash
FILE='cipher.bin'
python3 - "$FILE" <<'PY'
from pathlib import Path
import sys
data = Path(sys.argv[1]).read_bytes()
rows = []
for key in range(256):
    plain = bytes(b ^ key for b in data)
    score = sum((32 <= b <= 126 or b in (9,10,13)) +
                2*(b in b' etaoinshrdluETAOINSHRDLU') for b in plain)
    rows.append((score, key, plain))
for score, key, plain in sorted(rows, reverse=True)[:10]:
    print(f'key={key:02x}', score, repr(plain[:200]))
PY
```

**Look for:** coherent structure across the message; ranking is only a guess.
**If not:** test repeating-key alignment or classical-cipher clues in the reference.

## Quick: detect repeated AES-size blocks

**WSL · Python 3.** Input: raw ciphertext.

```bash
FILE='cipher.bin'
python3 - "$FILE" <<'PY'
from pathlib import Path
from collections import Counter
import sys
data = Path(sys.argv[1]).read_bytes()
for offset in range(16):
    counts = Counter(data[i:i+16] for i in range(offset,len(data)-15,16))
    repeats = sum(n-1 for n in counts.values())
    print('offset', offset, 'repeats', repeats)
PY
```

**Look for:** aligned repetitions supporting an ECB hypothesis.
**If not:** compare nonce/IV generation; CBC/CTR/oracle techniques require the exact protocol.

## Quick: crack a confirmed raw MD5 hash

**Kali · hashcat / John.** Input: one unsalted MD5 hex digest per line in `hashes.txt`; one candidate password per line in `words.txt`. Mode 0 is specifically raw MD5; 32 hex characters alone do not identify it. [Mode reference](https://hashcat.net/wiki/doku.php?id=example_hashes).

```bash
FILE='hashes.txt'
WORDS='words.txt'
hashcat -I
hashcat -m 0 -a 0 "$FILE" "$WORDS"
hashcat -m 0 "$FILE" --show
```

If hashcat has no usable backend:

```bash
FILE='hashes.txt'
WORDS='words.txt'
john --format=raw-md5 --wordlist="$WORDS" "$FILE"
john --show --format=raw-md5 "$FILE"
```

**Look for:** a recovered candidate verified against the challenge.
**If not:** distinguish wrong format from an exhausted wordlist before adding guesses.
