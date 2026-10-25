# Miscellaneous

Run Bash in the named environment, from the extracted guide root for `recipes/` commands. Set each `FILE` to your artifact. [Full reference](../reference/chapters/11-miscellaneous.md) includes RF, games, constraint solvers and complete jail examples.

## Quick: identify unfamiliar bytes

**WSL · xxd / strings.** Input: raw artifact.

```bash
FILE='artifact.bin'
xxd -l 128 "$FILE"
strings -a -n 6 "$FILE" | head -n 50
```

**Kali · file / 7-Zip.** Check container recognition without extracting:

```bash
FILE='artifact.bin'
file "$FILE"
7z l "$FILE"
```

**Look for:** actual signatures, embedded names and unexpectedly large members.
**If not:** inspect byte distribution and source; the extension may be misleading.

## Quick: decode one justified layer

**WSL · Python 3.** Input: Base64 text. Output directory must be new; recipe keeps decoded/compressed layers separately.

```bash
FILE='message.txt'
python3 recipes/layers.py "$FILE" --out misc-decoded
```

**Look for:** a coherent new header or readable text.
**If not:** check hex, binary digits or Unicode in the reference; do not stack arbitrary decoders.

## Quick: inspect JSON without executing it

**WSL · jq.** Input: JSON document.

```bash
FILE='challenge.json'
jq 'type' "$FILE"
jq 'keys' "$FILE"
jq . "$FILE"
```

**Look for:** arrays, encoded strings, coordinates and numeric bounds.
**If not:** inspect the first bytes for compression, JSON Lines or malformed syntax; never use `eval` to parse data.

## Quick: preserve duplicate archive members

**WSL · Python 3.** Input: TAR, TAR.GZ or another tarfile-supported compression. New output directory required; numbered files preserve duplicate names.

```bash
FILE='bundle.tar'
python3 recipes/tar_keep.py "$FILE" --out misc-tar-parts
```

**Look for:** repeated original names in `manifest.jsonl`, differing content or ordered fragments.
**If not:** use the matching archive format; ordinary extraction can overwrite duplicates.

## Quick: reconstruct a binary QR grid

**WSL · Python 3 / ZBar.** Input `grid.txt`: equal-length rows containing only `0`/`1`, where `1` means black. Adds a four-module white border.

```bash
FILE='grid.txt'
python3 - "$FILE" <<'PY'
from pathlib import Path
import sys
rows = Path(sys.argv[1]).read_text().split()
assert rows and len(rows) == len(rows[0]) <= 177
assert all(len(r) == len(rows[0]) and set(r) <= {'0','1'} for r in rows)
size, scale = len(rows)+8, 8
pixels = bytearray()
for y in range(size):
    line = bytes(0 if 4 <= y < size-4 and 4 <= x < size-4 and rows[y-4][x-4] == '1' else 255 for x in range(size))
    pixels.extend(b''.join(bytes([v])*scale for v in line)*scale)
Path('grid.pgm').write_bytes(f'P5\n{size*scale} {size*scale}\n255\n'.encode()+pixels)
PY
zbarimg --raw grid.pgm
```

**Look for:** decoded payload matching the challenge.
**If not:** verify finder squares, row order and polarity before modifying modules.

## Quick: inspect audio channels and duration

**WSL · Python 3.** Input: uncompressed PCM WAV.

```bash
FILE='audio.wav'
python3 - "$FILE" <<'PY'
import sys, wave
with wave.open(sys.argv[1], 'rb') as w:
    print('channels', w.getnchannels(), 'sample bytes', w.getsampwidth())
    print('rate', w.getframerate(), 'frames', w.getnframes())
    print('seconds', w.getnframes()/w.getframerate())
PY
```

**Kali · Audacity:** File → Open → select audio → track dropdown → Spectrogram → zoom suspicious interval; inspect channels separately.

**Look for:** tone pairs, Morse timing, repeated bursts or drawn text.
**If not:** compressed audio needs format-aware inspection; see the reference for PCM/IQ layout checks.

## Quick: inspect a Python jail before probing

**Kali · ripgrep.** Input: supplied jail source; this reads it without running it.

```bash
FILE='jail.py'
rg -n 'eval|exec|compile|__builtins__|globals|locals|ast\.|audit|normalize|encode|len\(|input\(' "$FILE"
```

**Look for:** parser stage, allowed names, length limit and persistent state.
**If not:** read the full source and protocol; version-specific object indices are unreliable.

## Quick: enumerate a known one-byte VM

**WSL · Python 3.** Input: JSON `program` array using the recipe's `LOAD_INPUT`, `XOR`, `ADD`, `ROL`, `CMP`, `HALT` operations. This toy returns byte `K`; replace its instructions only after recovering opcode semantics.

```bash
cat > vm-toy.json <<'JSON'
{"program":[["LOAD_INPUT"],["XOR",35],["ADD",7],["CMP",111],["HALT"]]}
JSON
python3 recipes/vm_byte.py vm-toy.json
```

**Look for:** a candidate passing every comparison with a reproducible trace.
**If not:** verify overflow, rotation direction and state resets; larger games need an explicit state model.
