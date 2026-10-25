# Miscellaneous: turn unfamiliar artifacts into a small model

**Quick route:** [Short commands](../QUICKSTART.md#decode-layers) · [Tool strengths and weaknesses](../TOOL-CHOOSER.md#miscellaneous). Use this chapter for deeper explanations.

Miscellaneous is one of the PDF's seven competition categories. Its techniques also overlap cryptography, forensics, network analysis, steganography, reversing and web security. Use the artifact and intended operation to choose the next step.

This chapter covers layered encodings, symbolic puzzles, jails, games, audio/RF data, and challenge navigation. Work only on supplied files and assigned challenge services. A challenge container escape is not authorization to modify the organizer's Kali host, workstation, or scoring platform.

## 1. Platform map

| Task | Windows/WSL route | Organizer Kali route |
|---|---|---|
| Decode bytes or solve small puzzles | WSL Python 3 standard library | Python 3; check actual interpreter |
| QR scanning | Listed WSL ZBar | Use a provisioned approved scanner if available; do not assume Windows tools are duplicated |
| Inspect bytes | Windows HxD or WSL xxd | Listed file, local editor, Python |
| Audio/spectrogram | Standard-library WAV inspection below | Listed Audacity, Sonic Visualiser, FFmpeg, SoX |
| Source search | Editor or Python file reads | Listed ripgrep |
| Constraints | Small Python enumeration; non-AI library under PDF p.5 | Check the interpreter; non-AI libraries may be added under PDF p.5 |
| Interactive protocol | Python socket to the assigned host | Python socket or listed Ncat |

Check only the dependency needed for the next step. PDF p.5 permits non-AI libraries/dependencies/plugins/packages in both environments; [package setup](00-tool-rules.md#non-ai-python-package-checks) preserves named exclusions and the AI/ML ban. Use local decoders and compilers for challenge material.

## 2. Preserve the original and inspect the representation

Save as `inspect_bytes.py`, then run `python3 inspect_bytes.py artifact.bin`:

```python
from pathlib import Path
from collections import Counter
import hashlib
import math
import sys

data = Path(sys.argv[1]).read_bytes()
counts = Counter(data)
entropy = -sum((n/len(data))*math.log2(n/len(data)) for n in counts.values()) if data else 0
print('bytes:', len(data))
print('sha256:', hashlib.sha256(data).hexdigest())
print('first64 hex:', data[:64].hex())
print('first64 repr:', repr(data[:64]))
print('byte entropy:', round(entropy, 3))
```

High entropy suggests compressed, encrypted, or naturally varied data; it does not identify which. A known magic header plus a mismatched extension is more useful than entropy alone. Keep transformed outputs under new names so you can reverse a mistaken branch.

**Kali only:** `file artifact.bin` provides another format hypothesis. Check the actual bytes before trusting an extension or a single tool label.

## 3. Decode one layer with a reason

| Appearance | Candidate | Confirm before decoding again |
|---|---|---|
| Even number of hex digits | Hex bytes | Decoded length halves; inspect header |
| Alphabet/base64 padding | Base64 | Strict decoder accepts it; inspect bytes |
| A–Z and 2–7 | Base32 | Padding/case rules match |
| `%xx` sequences | URL encoding | Distinguish bytes from Unicode text |
| `\xNN`, `\uNNNN` | Language/string escapes | Decode according to the source language |
| Two decimal digits per byte | BCD | Each nibble must be 0–9 |
| Mostly invisible Unicode | Tags/variation selectors/zero-width marks | Print code points, not rendered text |
| Numeric columns | ASCII, coordinates, or samples | Check ranges and column meaning |

Save as `encoding_toys.py`:

```python
import base64
import codecs
from urllib.parse import unquote_to_bytes

original = b'CTF{layers}'
encoded = base64.b64encode(original.hex().encode()).decode()
stage1 = base64.b64decode(encoded, validate=True)
stage2 = bytes.fromhex(stage1.decode('ascii'))
assert stage2 == original
assert unquote_to_bytes('CTF%7Blayers%7D') == original
assert codecs.decode(codecs.encode('hello', 'rot_13'), 'rot_13') == 'hello'
print(encoded)
print(stage1)
print(stage2)
```

The order matters: base64 decoding reveals hex text, then hex decoding reveals the flag-shaped toy. Do not feed arbitrary strings to `eval` to “decode” them.

### Unicode tags and variation selectors

Save as `unicode_inspect.py`, then run it on a UTF-8 text file:

```python
from pathlib import Path
import sys
import unicodedata

text = Path(sys.argv[1]).read_text(encoding='utf-8')
tags = []
selectors = []
for position, char in enumerate(text):
    point = ord(char)
    if point > 127 or not char.isprintable():
        print(position, f'U+{point:04X}', unicodedata.name(char, 'UNNAMED'))
    if 0xE0020 <= point <= 0xE007E:
        tags.append(point-0xE0000)
    # A common byte mapping, not a universal Unicode steganography standard.
    if 0xFE00 <= point <= 0xFE0F:
        selectors.append(point-0xFE00)
    elif 0xE0100 <= point <= 0xE01EF:
        selectors.append(point-0xE0100+16)
print('tag ASCII:', bytes(tags))
print('selector bytes:', bytes(selectors))
```

The tags block and variation-selector mapping are different encodings. Confirm the producer's convention. Zero-width characters can encode bits with a custom alphabet; enumerate symbols first. UTF-16 endianness reversal instead acts on byte pairs, so retain original bytes rather than copying rendered text.

### Floats, Gray code, and BCD

Save as `numeric_encodings.py`:

```python
import struct

raw = b'ABCD'
value = struct.unpack('<f', raw)[0]
assert struct.pack('<f', value) == raw
print('float carrying four bytes:', value)

def gray_to_binary(gray):
    result = gray
    while gray:
        gray >>= 1
        result ^= gray
    return result

for n in range(256):
    assert gray_to_binary(n ^ (n >> 1)) == n
print('Gray-code checks passed')

packed = bytes([0x12, 0x34, 0x56])
digits = ''
for byte in packed:
    hi, lo = byte >> 4, byte & 15
    assert hi < 10 and lo < 10
    digits += str(hi) + str(lo)
assert digits == '123456'
print(digits)
```

A decimal float text dump may have rounded away the original bits. IEEE-754 endian choice and width matter. Gray code requires cumulative XOR, not simply reading the Gray-coded integer as binary. Packed BCD is not hexadecimal ASCII.

## 4. Archive and polyglot puzzles

List contents before extraction. Nested archives may hide a password or next filename in metadata, comments, or a previous layer. Do not blindly recurse without depth, size, and path limits.

**Kali only**, for the listed archive tools:

```bash
7z l challenge.zip
unzip -l challenge.zip
```

For a ZIP on either Python environment, use `zipfile.ZipFile(...).infolist()` to inspect names, compressed/uncompressed lengths, and comments. The web chapter includes a path/symlink inspector. Extract into a fresh challenge directory only after reviewing traversal and total size.

PNG/JAR/ZIP, JPEG/HTML, and WAV/polyglot formats exploit parsers that read different regions. Identify where each parser starts and stops. Appended ZIP data may be visible to an archive reader even when an image viewer ignores it. Do not execute an embedded JAR or program merely because an image opened successfully.

RTF custom tags and SMS PDU payloads need format-aware extraction. Preserve escape sequences, record PDU user-data length and encoding, and reassemble concatenated SMS parts by their reference/sequence fields. Ordinary UTF-8 decoding is not a substitute for GSM 7-bit unpacking.

## 5. QR reconstruction and other visual alphabets

Determine the module grid, orientation, polarity, and quiet zone. A normal QR has three finder patterns and timing patterns; decorative image pixels are not necessarily modules. Rotate/flip only with a record of each transformation.

For a text file of `0`/`1` module rows, save `grid_to_pgm.py`:

```python
from pathlib import Path
import sys

rows = [line.strip() for line in Path(sys.argv[1]).read_text().splitlines() if line.strip()]
assert rows and all(len(row) == len(rows[0]) for row in rows)
assert all(set(row) <= {'0', '1'} for row in rows)
scale, quiet = 8, 4
height, width = len(rows), len(rows[0])
out_w, out_h = (width+2*quiet)*scale, (height+2*quiet)*scale
pixels = bytearray()
for y in range(out_h):
    for x in range(out_w):
        gx, gy = x//scale-quiet, y//scale-quiet
        dark = 0 <= gx < width and 0 <= gy < height and rows[gy][gx] == '1'
        pixels.append(0 if dark else 255)
Path('grid.pgm').write_bytes(f'P5\n{out_w} {out_h}\n255\n'.encode()+pixels)
print(out_w, out_h, 'grid.pgm')
```

**Windows WSL**, with listed ZBar:

```bash
python3 grid_to_pgm.py modules.txt
zbarimg --raw grid.pgm
```

Expected output is decoded text, which may itself be another layer. If scanning fails, inspect the grid visually and check whether `1` should be light instead. Do not “repair” random modules until finder/timing patterns and dimensions are consistent.

For tile reassembly, use filenames, directory indexes, edge continuity, and QR structural constraints to reduce permutations. A nonogram may produce the QR grid: solve row/column run constraints, then render with the script above. Hexadecimal Sudoku may similarly map symbols to image modules.

Pigpen, flag semaphore, musical intervals, DTMF, keyboard shifts, and MaxiCode have different symbol systems. Identify the alphabet first. ZBar support is not universal across barcode types; a scanner failure may mean unsupported symbology rather than a damaged image.

## 6. Audio: inspect channels before interpreting tones

**Kali only**, with listed FFmpeg:

```bash
ffprobe -v error -show_entries stream=codec_name,sample_rate,channels,bits_per_sample -of default=noprint_wrappers=1 audio.wav
ffmpeg -i audio.wav -lavfi showspectrumpic=s=1600x900:legend=1 spectrum.png
```

Open the spectrogram and look for text, repeated bursts, paired tones, or frequency shifts. Try Audacity's Spectrogram view if you need to zoom and compare channels. Preserve the original sample rate; resampling can destroy symbol timing.

On Windows WSL, a standard-library WAV inspection works without assuming FFmpeg:

```python
# Save as wav_info.py; run: python3 wav_info.py audio.wav
import wave
import sys

with wave.open(sys.argv[1], 'rb') as wav:
    print('channels:', wav.getnchannels())
    print('sample width:', wav.getsampwidth())
    print('sample rate:', wav.getframerate())
    print('frames:', wav.getnframes())
    print('seconds:', wav.getnframes()/wav.getframerate())
```

The `wave` module handles supported uncompressed WAV variants, not every audio codec. An unsupported-format error means use an available approved decoder, not rename an MP3 to `.wav`.

### Morse bursts from one PCM channel

Save as `morse_runs.py`. It prints high/low envelope run lengths; it does not guess a threshold or a Morse alphabet for you.

```python
import sys
import wave
import struct
import math

filename = sys.argv[1]
threshold = float(sys.argv[2])  # RMS amplitude, e.g. 1000 for 16-bit PCM
channel = int(sys.argv[3]) if len(sys.argv) > 3 else 0
with wave.open(filename, 'rb') as wav:
    assert wav.getsampwidth() == 2, 'requires 16-bit PCM'
    count, rate = wav.getnchannels(), wav.getframerate()
    assert 0 <= channel < count
    raw = wav.readframes(wav.getnframes())
samples = struct.unpack('<'+'h'*(len(raw)//2), raw)[channel::count]
window = max(1, rate//100)  # approximately 10 ms
states = []
for start in range(0, len(samples), window):
    chunk = samples[start:start+window]
    rms = math.sqrt(sum(x*x for x in chunk)/len(chunk))
    states.append(rms > threshold)
runs = []
for state in states:
    if runs and runs[-1][0] == state:
        runs[-1][1] += 1
    else:
        runs.append([state, 1])
for state, length in runs:
    print('tone' if state else 'gap', round(length*window/rate, 3))
```

```bash
python3 morse_runs.py audio.wav 1000 0
```

Expect short/long tone clusters and several gap clusters. For conventional Morse, dot and dash lengths are roughly 1:3; within-letter, letter, and word gaps are roughly 1:3:7. Choose the basic unit from the run histogram, not a single noisy burst. If both channels differ, run each separately. Continuous music requires band filtering before envelope thresholding.

### DTMF, SSTV, and hidden sample bits

DTMF uses one low and one high frequency per key. After decoding digits, repeated presses may represent multi-tap text rather than a telephone number. Compare tone duration and pauses.

SSTV sounds like a long modulated image transmission. The Kali sheet has an `sstv`/PySSTV entry, but package name and decoding CLI capability must be verified with local help; do not assume an encoder package provides the source repository's decoder command. MMSSTV and RX-SSTV are explicitly unapproved. If the provided CLI cannot decode, retain the mode/timing observations and report the limitation.

Sample LSB extraction needs the correct sample width, signedness, endian order, channel, and bit order. Read PCM values rather than the WAV header bytes. Test whether an extracted stream begins with a plausible header; a handful of printable bytes is weak evidence.

## 7. RF/IQ files: get units and layout right

An IQ file may contain interleaved signed 8-bit, signed 16-bit, or float32 I/Q pairs. Determine the format from the challenge description or generator. A wrong dtype can produce a plausible-looking but meaningless constellation.

Save as `iq_peek.py` for a **little-endian float32 IQ** hypothesis:

```python
from pathlib import Path
import struct
import math
import sys

raw = Path(sys.argv[1]).read_bytes()
assert len(raw) % 8 == 0, 'not whole float32 I/Q pairs'
pairs = list(struct.iter_unpack('<ff', raw[:8*10000]))
assert pairs and all(math.isfinite(i) and math.isfinite(q) for i, q in pairs)
power = sum(i*i+q*q for i, q in pairs)/len(pairs)
print('pairs total:', len(raw)//8)
print('first five:', pairs[:5])
print('sampled mean power:', power)
```

Next establish sample rate, occupied bandwidth, carrier offset, symbol rate, and modulation. With a provisioned non-AI numerical library, plot a short spectrum and constellation locally. For QAM, carrier rotation and timing recovery must precede symbol slicing. Try a known preamble to resolve quadrant ambiguity and bit order.

FFT bins are in cycles per sample until multiplied by the sample rate. A frequency peak in a squared signal is not always the symbol rate; modulation and filtering can produce harmonics. Validate the proposed rate by a stable eye/constellation and repeated frame synchronization.

Manchester coding, whitening, convolutional coding, checksums, and framing may follow demodulation. A valid packet CRC is a much stronger success check than a few recognizable letters.

## 8. Interactive protocols without losing synchronization

Read the prompt and response framing before automating. A service may use newline-delimited JSON, length prefixes, menus, or multiple phases. TCP reads do not correspond one-to-one with server messages.

Save as `read_prompt.py` and replace the host/port only with the assigned challenge endpoint:

```python
import socket
import sys

host, port = sys.argv[1], int(sys.argv[2])
with socket.create_connection((host, port), timeout=5) as sock:
    sock.settimeout(5)
    stream = sock.makefile('rb')
    line = stream.readline(65537)
    if len(line) > 65536:
        raise SystemExit('line exceeds local limit')
    print(repr(line))
```

This reads one line and sends nothing. If the prompt has no newline, use a bounded `recv` loop until the observed delimiter instead. Preserve state in one connection when the challenge requires it; reconnecting may reset the secret or invalidate prior observations.

For a timed multi-phase puzzle, implement and test each local solver first, then connect the phases through explicit parsers. Never use a remote response as Python source. Treat a timeout as an unknown state, not automatically a wrong answer.

## 9. Python jails: inspect the evaluator, then build the primitive

Read the supplied jail source. Record the Python version, `eval` versus `exec`, available globals/builtins, input normalization, blacklist/allowlist, AST checks, length limit, output handling, and whether state persists between inputs.

Use small diagnostic expressions, one at a time:

```python
1+1
"A"*3
().__class__
(1).__class__.__name__
```

Expected results tell you whether arithmetic, strings, attribute access, and normal Python objects exist. A syntax error, filter rejection, NameError, and runtime exception reveal different stages. Do not assume `eval` accepts statements such as `x=1`; it does not. A walrus expression has separate syntax and scope restrictions.

### A complete object-reference escape toy

Removing `__builtins__` does not make references to powerful Python objects safe. Save as `jail_reference_toy.py`:

```python
FLAG = 'CTF{function_globals_are_reachable}'

def helper():
    return 'ordinary helper'

def toy_jail(expression):
    return eval(expression, {'__builtins__': {}, 'helper': helper}, {})

assert toy_jail('1+1') == 2
result = toy_jail("helper.__globals__['FLAG']")
assert result == FLAG
print(result)
```

For a real challenge, inspect which function/object is exposed and which globals it retains. If an exposed function's globals contain real builtins and the supplied flag path is `/app/flag.txt`, a corresponding builtins `open` call can read that file. The exact dictionary/module shape and filter rules decide the syntax.

Subclass enumeration is another route, but hard-coded indexes are unreliable across versions and imported modules. Search by class name and verify its attributes in a local reproduction. Decorators, format-field traversal, `__getitem__`, and object lifecycle hooks can create implicit calls only if the jail permits the required syntax and objects.

Unicode identifier normalization occurs during Python parsing; string literals are not normalized in the same way. Encoding comments matter only when source bytes are decoded as a file, not necessarily when an already-decoded input string is passed to `eval`.

### Advanced jail constraints

| Restriction | Useful starting point | Failure to avoid |
|---|---|---|
| No quotes | Existing docstrings, names, or indexed strings | Assuming the same docstring offsets across Python versions |
| No direct calls | Allowed decorators, indexing, or formatting hooks | Mutating immutable built-in classes |
| One dot | An already available attribute-access primitive | Presenting a chain containing many dots as a solution |
| Prime length | Count actual transmitted characters; pad with a permitted comment | Confusing escaped source spelling with received bytes |
| Length checked before a second read | Trace the second input's validation path | Treating assignment statements as valid `eval` expressions |
| Audit hooks | Determine Python hook, native hook, and events actually monitored | Assuming private CPython memory offsets are portable |
| Mastermind/distance oracle | Define exact score and input bounds | Interpreting a different score metric as character equality |

Private-runtime memory corruption and hard-coded `_PyRuntime` offsets are not portable recipes. Keep those source examples as version-specific reverse-engineering leads, and validate in the supplied local binary before attempting anything against a service.

## 10. Bash and restricted-shell puzzles

Find the real shell and input path. A filter before `eval`, a restricted shell mode, a menu wrapper, and a seccomp sandbox impose different constraints. Test quoting and expansion locally with a harmless marker.

```bash
printf '%s\n' $'\103\124\106'
printf '%s\n' "$0"
```

Expected first output: `CTF`. ANSI-C octal quoting creates bytes after the raw-input filter has already seen a different spelling. It helps only if the shell supports that syntax and the necessary characters survive the filter.

For an assigned jail that permits the shell built-in `read` and redirection, a supplied flag path can be read without an external `cat`:

```bash
while IFS= read -r line; do printf '%s\n' "$line"; done < /app/flag.txt
```

This assumes that exact challenge file path and permissions. If redirection is filtered or execution happens in another shell, it fails. Closed stdout requires tracing the actual output channel; carriage returns can alter display but do not create file access by themselves.

`HISTFILE`, startup files, environment variables, editor command hooks, and dynamic-loader variables are meaningful only if the wrapper invokes the corresponding feature. Do not set persistent startup variables on the competition workstation to test a challenge theory.

## 11. Games, virtual machines, and finite-state puzzles

Locate the authoritative state. Browser-rendered scores, local cookies, a WebSocket server, WASM memory, and server databases are different sources of truth. Change a harmless client value and check whether the server accepts the resulting state.

For an unsigned or disclosed-secret Flask session, separate decoding from forging; a readable cookie is not necessarily modifiable. For WebSocket games, compare a normal frame with a controlled changed field. Server-time-only validation and floating-point edge cases require actual server acceptance, not just a changed display.

WASM memory is linear bytes, but compiler layouts and exported functions determine meaningful offsets. Use supplied source and browser DevTools to correlate one known value before patching. Roblox files, PyInstaller bundles, remapped Python opcodes, and memfd-packed binaries belong primarily to reverse engineering; preserve their container/bytecode version and use the approved local tools from that chapter.

### A shortest-path toy you can adapt

Save as `maze_bfs.py`:

```python
from collections import deque

grid = ['S..#', '.#..', '...E']
start, goal = (0, 0), (2, 3)
queue = deque([start])
previous = {start: None}
while queue:
    r, c = queue.popleft()
    if (r, c) == goal:
        break
    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nr, nc = r+dr, c+dc
        if not (0 <= nr < len(grid) and 0 <= nc < len(grid[0])):
            continue
        if grid[nr][nc] == '#' or (nr, nc) in previous:
            continue
        previous[(nr, nc)] = (r, c)
        queue.append((nr, nc))
assert goal in previous
path = []
current = goal
while current is not None:
    path.append(current)
    current = previous[current]
path.reverse()
assert len(path)-1 == 5
assert all(abs(a[0]-b[0])+abs(a[1]-b[1]) == 1 for a, b in zip(path, path[1:]))
print(path)
```

For image mazes, first derive a stable grid from cell centers. Anti-aliased edges, moving sprites, and coordinate scaling can corrupt wall detection. If a move depends on inventory or switches, include them in the BFS state; position alone is insufficient.

### Recurrences and number representation

For a recurrence puzzle, compute a dozen terms locally, compare all supplied examples, then use dynamic programming or matrix exponentiation. Do not upload the challenge sequence to an online lookup service. OEIS-style automated online searching from the original source is excluded here.

JavaScript integers lose exactness above `2^53-1`. **Kali only**, with listed Node.js:

```javascript
// Save as precision-demo.js; run: node precision-demo.js
const x = 2 ** 53;
console.log(x === x + 1); // true
console.log(BigInt(x) === BigInt(x) + 1n); // false
```

A challenge must actually use floating-point number semantics for this to matter. JSON-to-integer conversion in another language may reject or preserve the value differently.

De Bruijn sequences cover all fixed-length substrings efficiently, but cyclic versus linear output changes the required suffix. The 100-prisoners strategy follows permutation cycles; it does not guarantee success for an arbitrary instance. Fifteen-puzzle solvability depends on inversion parity and blank-row convention, so verify with a solved board before decoding bits.

## 12. Constraint solving and esoteric languages

Write constraints in the original domain. For bytes, constrain `0..255`; for fixed-width arithmetic, preserve wrapping and signedness. Add a second-solution check to learn whether the model is unique.

Without an SMT dependency, small domains can be enumerated exactly. Save as `constraints_toy.py`:

```python
solutions = [(x, y) for x in range(10) for y in range(10)
             if x+y == 11 and 3*x-y == 9]
assert solutions == [(5, 6)]
print(solutions[0])
```

For a provisioned `z3` library, model the same constraints first and verify its solution with ordinary Python. A SAT result is not a flag until it passes the challenge checker. YARA-derived conditions, Boolean circuits, nonograms, and type constraints may each need different domain choices.

Brainfuck requires a tape size policy, cell width, EOF behavior, and matched bracket map. Instrument each opcode and bound the step count before running unknown code. Whitespace languages treat spaces, tabs, and newlines as syntax; do not strip them. Piet requires image color transitions and direction state; an image viewer alone does not execute it.

Verilog/HDL puzzles require combinational versus sequential semantics, bit widths, signedness, and clock/reset behavior. If an unlisted simulator is required, manually translate a small circuit into a local Boolean model or use the provided approved environment; do not use an online HDL compiler.

## 13. DNS and protocol puzzles

Use the organizer-provided resolver or packet capture, not public infrastructure. DNS round-robin responses may reveal a set over repeated queries, but caching, TTL, and load balancing affect observations. A DNS maze needs a visited set and an explicit next-label rule.

For DNSSEC NSEC walking, inspect predecessor/successor names and whether the zone uses NSEC or NSEC3. An IXFR request differs from AXFR and requires the proper serial framing. EDNS Client Subnet affects resolver behavior only when the server honors it; it is not a universal source-address spoof.

When DNS carries encoded data, use transaction IDs, sequence fields, timestamps, and domain labels to reconstruct order. Remove the fixed suffix before decoding. Do not send challenge secrets through public DNS as a recovery method.

DNS rebinding is a timing and resolution disagreement; capture both validation and fetch phases. A hostname resolving twice to the same address is a failed experiment, not proof that the application is safe.

## 14. Challenge-scoped privilege puzzles

These source topics apply only when the challenge explicitly gives you a shell or local service and makes privilege escalation part of the objective. Run checks inside that challenge, never on the competition workstation:

```bash
id
pwd
sudo -l
```

Read the exact allowed program and argument constraints. Wildcards can match path separators depending on the matching function; a symlink can change what a later privileged open sees. Confirm ownership and permissions of the specific file involved. Do not modify `/etc/sudoers` or host service configuration merely to prove a theory.

SUID file readers, backup jobs, writable script paths, database program execution, print deployment services, and monitoring-agent arguments are separate primitives. Start with the supplied service's normal behavior and a harmless marker. The end goal is the designated challenge file, not persistence or workstation control.

Docker socket, privileged containers, BuildKit secrets, Kubernetes tokens, NFS, and internal proxies require explicit inclusion in the challenge topology. A token found in a challenge does not authorize unrelated infrastructure. For a permitted local puzzle, determine the token's actual namespace/role or socket permissions before choosing an action.

Historical polkit overflows, seccomp high-bit descriptor mistakes, editor escapes, and WinSSHTerm credential formats are version-specific. Use the supplied binary/configuration and approved reverse-engineering tools to verify the failing check. Source writeup commands are not portable proof.

## 15. Portal workflow and a useful handoff

Use the organizer's normal browser interface to read descriptions, download attachments, start instances, request hints, and submit flags. A CTFd-looking theme does not prove its API or authentication behavior. Hints can cost points; read the displayed consequence before purchasing.

If the organizer explicitly documents an API for competitors, use its token and endpoint format as supplied. Keep the token out of notes and logs. Do not scrape hidden challenges, attack the scoring platform, or automate repeated submissions because an old repository script can do so.

Record each solve as input artifact/hash, interpretation, exact transformation or script, expected output, final flag, and remaining assumptions. If a QR, audio, game, or jail solution depends on manual transcription, save that intermediate representation so a teammate can reproduce it.

The 14 source files in `ctf-misc/` are merged here: overview; encodings and advanced formats; audio and RF; Python/Bash jails; games/VMs parts 1–4; DNS; CTFd navigation; and Linux privilege puzzles. Overlapping network, media, crypto, and reverse-engineering details are cross-category material rather than new official event categories.
