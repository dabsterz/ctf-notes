# Steganography, documents, and media

**Quick route:** [Short commands](../QUICKSTART.md#png-trailer) · [Tool strengths and weaknesses](../TOOL-CHOOSER.md#steganography-and-audio). Use this chapter for deeper explanations.

Treat each file as a container before treating it as pixels or sound. Read metadata, inspect structural boundaries, enumerate frames/tracks, then test a specific hiding hypothesis. Keep every recovered layer and its extraction settings.

## Tools and execution environment

| Environment | Approved tools | Workbook rows |
|---|---|---|
| Windows native | HxD, PDF viewer | Windows 42, 10 |
| Windows WSL | Python 3, strings, zsteg, binwalk, ExifTool, pdftotext, ZBar, qpdf, xxd | Windows 14, 18–22, 26, 33, 35 |
| Kali | Audacity, FFmpeg, ImageMagick, pngcheck, SoX, Sonic Visualiser, steghide, stegseek, stegsnow, StegSolve | Kali 17, 47, 74, 115, 136, 135, 141–144 |

Python examples run in **WSL**. Non-AI libraries such as Pillow, NumPy and SciPy may be added under PDF p.5; use [targeted package setup](00-tool-rules.md#non-ai-python-package-checks). Keep named exclusions: ML classifiers, DCT-Image-Steganography, sigBits and magiceye-solver are outside this guide's practical routes (Unapproved rows 17, 75, 42).

Keep decoding local. Online image/barcode readers and public analysis uploads are not a substitute for missing tools under the [event rules](https://ajccbc.ncsa.or.th/cyber-sea-game-2026/).

## First five minutes

`carrier.png` is the supplied file; change the filename but preserve the original. **WSL:**

```bash
exiftool -a -u -g1 carrier.png
xxd -l 256 carrier.png
strings -a -n 6 carrier.png
binwalk carrier.png
zsteg -a carrier.png
```

Expected result: a metadata clue, embedded-format offset, or candidate bit layout. Binwalk signatures and zsteg readable fragments are leads, not proof. Validate extracted bytes using their file format. `binwalk -e` may invoke external helpers; prefer targeted carving with the Python extractor in the forensics chapter rather than relying on unlisted helper programs.

For a JPEG, inspect the first few hundred bytes even if ExifTool reports nothing. A passphrase may be raw text in an unusual segment. Extract the thumbnail in **WSL**:

```bash
exiftool -b -ThumbnailImage carrier.jpg > thumbnail.jpg
```

An empty output means the tag is absent. View original and thumbnail at full resolution. Small text, selection masks, and different crops can be the intended clue.

For a suspected steghide carrier, **Kali** rows 141–142:

```bash
steghide info carrier.jpg
steghide extract -sf carrier.jpg -xf recovered.bin
stegseek carrier.jpg challenge-words.txt recovered-from-wordlist.bin
```

Enter a clue-derived password at the steghide prompt; an empty password is a reasonable single test if the clue gives none. `challenge-words.txt` is a small local list built from evidence. A failed password does not prove absence of embedded data. Inspect the extracted format and contents before continuing to another layer.

## PNG chunks, trailers, and safe repairs

**Kali**: `pngcheck -v carrier.png` reports chunk order, CRC failures, and dimensions. The following **WSL Python** script walks actual chunk boundaries; it does not mistake an `IEND` byte string inside compressed data for the file's end. Save as `png_chunks.py` and run `python3 png_chunks.py carrier.png`.

```python
import sys, struct, zlib
from pathlib import Path

d = Path(sys.argv[1]).read_bytes()
assert d[:8] == b'\x89PNG\r\n\x1a\n', 'bad PNG signature'
out = Path('png-parts')
out.mkdir(exist_ok=True)
pos, index = 8, 0
while pos + 12 <= len(d):
    size = struct.unpack_from('>I', d, pos)[0]
    kind = d[pos+4:pos+8]
    end = pos + 12 + size
    assert end <= len(d), 'chunk extends beyond file'
    body = d[pos+8:pos+8+size]
    stored = struct.unpack_from('>I', d, pos+8+size)[0]
    valid = zlib.crc32(kind + body) == stored
    print(hex(pos), kind, size, 'CRC OK' if valid else 'BAD CRC')
    (out / f'{index:03d}-{kind.hex()}.bin').write_bytes(body)
    index += 1
    pos = end
    if kind == b'IEND':
        assert size == 0
        (out / 'trailer.bin').write_bytes(d[pos:])
        print('trailing bytes:', len(d)-pos)
        break
else:
    raise ValueError('no complete IEND')
```

Inspect the saved trailer in WSL with `xxd -l 128 png-parts/trailer.bin` and `strings -a png-parts/trailer.bin`. Or use the [short PNG card](../QUICKSTART.md#png-trailer), whose helper prints a preview automatically.

Check `tEXt`, `iTXt`, `zTXt`, unknown chunks, unused palette data, and bytes after IEND. If an archive signature is overwritten, repair only a copy after verifying the rest of its header. For chunk-case corruption, change the **chunk type field**, then recompute its CRC over type+data. Global byte replacement can corrupt an IDAT stream.

IHDR must be first, IEND last, and IDAT chunks consecutive. PLTE/tRNS and other ancillary chunks have specific ordering requirements: do not move every ancillary chunk before IDAT indiscriminately. Preserve IDAT ordering unless a separate clue defines a permutation.

If only the IHDR height is damaged and the old CRC remains, search a bounded height range. **WSL:**

```python
from pathlib import Path
import struct, zlib
d = bytearray(Path('broken.png').read_bytes())
assert d[12:16] == b'IHDR' and int.from_bytes(d[8:12],'big') == 13
target = int.from_bytes(d[29:33], 'big')
for height in range(1, 8193):
    trial = d[12:20] + struct.pack('>I', height) + d[24:29]
    if zlib.crc32(trial) == target:
        d[20:24] = struct.pack('>I', height)
        Path('height-fixed.png').write_bytes(d)
        print('matching height:', height)
        break
else:
    print('no match: wrong hypothesis, range, or damaged CRC')
```

After repair, verify decoding and expected decompressed scanline length. A matching CRC is not permission to claim arbitrary new rows exist.

## Bitplanes and packed messages

Use when a lossless image looks normal but a hint points to low bits, colors, or parity. **WSL**, save as `planes.py`:

```python
from pathlib import Path
from PIL import Image
import numpy as np

im = np.array(Image.open('carrier.png').convert('RGB'))
out = Path('planes'); out.mkdir(exist_ok=True)
for channel, name in enumerate('RGB'):
    for bit in range(8):
        plane = ((im[:,:,channel] >> bit) & 1).astype('uint8')
        Image.fromarray(plane * 255).save(out / f'{name}{bit}.png')
        for order in ('big','little'):
            (out / f'{name}{bit}-{order}.bin').write_bytes(
                np.packbits(plane.ravel(), bitorder=order).tobytes())
parity = (im.astype('uint16').sum(axis=2) & 1).astype('uint8')
Image.fromarray(parity * 255).save(out / 'rgb-parity.png')
bits = np.stack([(im[:,:,0]>>0)&1, (im[:,:,1]>>1)&1,
                 (im[:,:,2]>>2)&1], axis=-1).ravel()
(out / 'R0-G1-B2.bin').write_bytes(np.packbits(bits).tobytes())
```

```bash
python3 planes.py
zbarimg -q planes/G1.png
zsteg -E 'b1,r,lsb,xy' carrier.png > extracted.bin
```

The zsteg selector is an example; copy the exact promising selector printed by its analysis. Expected output is structured text or a valid file, not merely a short printable run. If nothing works, try row/column order, reversed traversal, bit polarity, RGB/BGR order, or a clue-defined carrier subset. Avoid recompressing to JPEG before extracting low bits.

Conditional carriers: with NumPy, select `im[np.all(im <= 1, axis=2)]` for near-black pixels and pack the chosen channel bits in their original order. Do not remove all zero-valued pixels automatically; zeros may encode valid data.

For a clockwise binary border, avoid reading the corner pixels twice:

```python
from PIL import Image
im = Image.open('carrier.png').convert('RGB')
w,h = im.size
coords = ([(x,0) for x in range(w)] + [(w-1,y) for y in range(1,h)] +
          [(x,h-1) for x in range(w-2,-1,-1)] + [(0,y) for y in range(h-2,0,-1)])
bits = [int(sum(im.getpixel(p)) >= 384) for p in coords]
data = bytes(sum(b << (7-j) for j,b in enumerate(bits[i:i+8]))
             for i in range(0,len(bits)-7,8))
print(repr(data))
```

Use thresholding only for visibly black/white carriers. Lossy images may need a measured threshold; color LSB extraction from JPEG-decoded pixels is usually unstable.

## Palettes, quantization tables, and pixel paths

Unused PNG palette entries can hold bytes without affecting visible pixels. **WSL:**

```python
from PIL import Image
from pathlib import Path
im = Image.open('carrier.png')
assert im.mode == 'P', 'not a palette image'
palette = im.getpalette()
used = set(im.getdata())
unused = [i for i in range(len(palette)//3) if i not in used]
for c,name in enumerate('RGB'):
    data = bytes(palette[3*i+c] for i in unused)
    Path(f'unused-{name}.bin').write_bytes(data)
    print(name, repr(data))
```

For JPEG DQT, `Image.open('carrier.jpg').quantization` exposes tables. Examine which table IDs the frame components reference before calling any table “unused”; IDs ≥2 are not automatically unused. Pillow exposes table order differently from raw JPEG zigzag storage, so test the format-defined order if a packed bitstream is scrambled. Re-saving a JPEG can remove or rewrite these tables.

F5-like embedding changes quantized AC coefficient statistics. Compare a suspect to matched clean images at the same encoder/quality, exclude DC coefficients by their **block positions**, and examine counts near zero. There is no universal ±1/±2 threshold that proves F5. Use this as triage; the unapproved named DCT toolkit is not an extraction route.

For JPEG block slack, inspect frame dimensions and sampling factors: MCU dimensions depend on chroma subsampling and can exceed 8×8. Ordinary resizing does not reveal encoded padding. If justified, alter dimensions in a copy within the existing MCU grid, retain compressed coefficients, and validate decoder output; ImageMagick's decode-size hint is not a general uncrop operation.

For a clue-defined pixel chain, **WSL**:

```python
from PIL import Image
im = Image.open('carrier.png').convert('RGB')
x,y = 0,0  # starting coordinate from the clue
seen, out = set(), bytearray()
while (x,y) not in seen:
    if not (0 <= x < im.width and 0 <= y < im.height):
        raise ValueError('next coordinate outside image')
    seen.add((x,y))
    value,nx,ny = im.getpixel((x,y))
    if value == 0: break
    out.append(value)
    x,y = nx,ny
print(repr(out))
```

For seeded permutations, reproduce the exact generator, shuffle algorithm, seed, traversal order, and channel conversion. NumPy `RandomState` and `default_rng` produce different permutations. Extract multiple bitplanes in the order specified by the encoder, then test the result's framing/checksum.

## QR reconstruction and geometric transforms

Use **WSL ZBar** (Windows row 26) to decode locally. Start with finder patterns in three corners, alternating timing lines, and module count `21 + 4*(version-1)`. Add a four-module quiet zone. Do not smooth module boundaries.

For a manually transcribed grid, save equal-width lines of `0` and `1` in `qr.txt`, where `1` means dark:

```python
from pathlib import Path
from PIL import Image, ImageOps
rows = Path('qr.txt').read_text().splitlines()
n = len(rows)
assert n >= 21 and all(len(r) == n and set(r) <= {'0','1'} for r in rows)
im = Image.new('L',(n,n),255)
im.putdata([0 if c=='1' else 255 for r in rows for c in r])
im = ImageOps.expand(im,border=4,fill=255)
im.resize((im.width*12,im.height*12),Image.Resampling.NEAREST).save('qr.png')
```

```bash
zbarimg -q qr.png
```

If decoding fails, check mirror/rotation, grid size, quiet zone, and damaged format bits. Error-correction percentages refer to recoverable codewords under specific conditions, not a guarantee that an arbitrary percentage of the image can be erased. For curved reflections, pick the sharpest frame, correct mirroring, estimate grid intersections, and record uncertain modules instead of inventing a flag prefix.

For colored QR carriers with few exact colors, enumerate binary assignments to those colors and scan each candidate. Six colors means 64 assignments. Do not enumerate millions of JPEG-noise colors; first justify a palette from the image. Multiple valid results can carry different messages.

Jigsaw pieces: score adjacent borders with the sum of absolute pixel differences after converting to signed integers. Anchor known corners/finder patterns and require each piece once. Greedy placement can trap the search; retain several best placements and backtrack when seams disagree. A 4×4 brute-force permutation search is far too large to recommend blindly.

Nearest-neighbor carriers: sample each grid phase, `array[y_offset::step, x_offset::step]`, and inspect the resulting low-resolution image. A chained resize can select different source pixels from a single direct resize; reproduce the entire size sequence if given.

For Arnold's cat map on a square image, iterate this **WSL** transform until the state repeats or a defined limit is reached:

```python
from PIL import Image
import numpy as np
a = np.array(Image.open('scrambled.png').convert('RGB'))
n = len(a); assert a.shape[1] == n
y,x = np.indices((n,n))
start = a.copy()
for step in range(1, 1001):
    b = np.empty_like(a)
    b[(x+y)%n,(2*x+y)%n] = a
    Image.fromarray(b).save(f'cat-{step:04d}.png')
    a = b
    if np.array_equal(a,start): break
```

Map orientation is a hypothesis; use the challenge's matrix if provided. The period depends on the matrix and dimensions, not a universal multiple of the image size.

For an autostereogram, compute `abs(image[:,shift:] - image[:,:-shift])` in signed arithmetic over a small range of repeat widths. Structured contours suggest a useful shift. This is ordinary image processing; no unapproved magic-eye tool or learned classifier is needed.

For a frequency-domain image clue, render a **grayscale** 2-D FFT magnitude in WSL. Applying `fft2` to an RGB array without specifying axes can accidentally transform a color axis.

```python
from PIL import Image
import numpy as np
a=np.asarray(Image.open('carrier.png').convert('L'),dtype=float)
spectrum=np.log1p(np.abs(np.fft.fftshift(np.fft.fft2(a))))
span=np.ptp(spectrum)
assert span>0,'constant spectrum'
view=np.rint((spectrum-spectrum.min())/span*255).astype('uint8')
Image.fromarray(view).save('fft-magnitude.png')
```

Measure any rings/peak grids before sampling bits; choose radii, angular order, and threshold from the image, not the historical challenge's constants. Fourier symmetry may duplicate rather than add message bits.

If equal plaintext pixels were replaced with equal ciphertext tokens, preserve token equality and render each distinct token as a different color to reveal shapes. A 256-entry hash-to-pixel lookup works only for a known **unkeyed hash** of single-byte grayscale values; it does not decrypt arbitrary keyed AES. For Angecryption clues, use the supplied/recovered cipher/key/IV and test full format validity in both directions; two valid images alone do not prove a relationship.

## PDF, SVG, and office documents

**WSL** tools, Windows rows 21, 22, 33:

```bash
exiftool -a -u -g1 document.pdf
pdftotext -layout document.pdf document.txt
qpdf --check document.pdf
qpdf --show-xref document.pdf
qpdf --qdf --object-streams=disable document.pdf expanded.pdf
qpdf --show-object=12 --filtered-stream-data document.pdf > object12.bin
```

Replace object `12` with an observed stream object. Inspect text extraction, metadata, link URI annotations, attachments, page contents, and incremental revisions. Keep the original: rewriting a PDF can discard unreferenced objects or normalize a covert xref channel. A black rectangle may overlay readable content; real redaction may remove it entirely.

**Kali** Didier Stevens Suite (row 37):

```bash
python3 /opt/tools/DidierStevensSuite/pdfid.py document.pdf
python3 /opt/tools/DidierStevensSuite/pdf-parser.py --stats document.pdf
python3 /opt/tools/DidierStevensSuite/pdf-parser.py --object 12 --filter --dump object12.bin document.pdf
```

A hidden page must be a valid Page object with content/resources; arbitrarily adding a content-stream number to `/Kids` is not sufficient. Inspect page-tree reachability and inherited resources before repairing a copy. For rectangle-based QR drawings, parse `re` coordinates from a decompressed content stream, account for transformation matrices, and map centers onto a measured module grid.

For classic textual xref entries, inspect generation numbers before qpdf rewrites them. Nonzero generations are legitimate after object reuse; treat unusual patterned values as a hypothesis. Match an actual `xref` section, not the substring inside `startxref`. Xref streams need their `/W` field widths and filters decoded first.

For SVG, read it as XML/text before opening active content. Inspect `<animate>` values/keyTimes, extremely small coordinate clusters, hidden groups, and transforms. To reveal micro-coordinate art, change a **copy's** `viewBox` to the small observed coordinate range. Animation timing can encode Morse; use actual key-time differences and duration.

For XLSX numeric carriers, export cells to CSV using approved Kali LibreOffice (row 88), keeping row/column order. Reimplement any macro's arithmetic without enabling it. Frequency-ranked values are only a hypothesis: tied frequencies make ordering ambiguous. Check all candidate mappings against file signatures rather than assuming 256 distinct values imply a correct byte map.

## Text, terminal, and archive channels

View suspicious terminal captures as bytes before displaying their escape sequences. ANSI can move the cursor and overwrite text; stripping CSI codes recovers underlying text but does not simulate the final screen.

**WSL**, inspect invisible characters without normalizing them away:

```python
from pathlib import Path
import re, unicodedata
s = Path('art.txt').read_text(encoding='utf-8')
for i,c in enumerate(s):
    if ord(c) < 32 or ord(c) > 126:
        print(i, f'U+{ord(c):04X}', unicodedata.name(c,'CONTROL'))
clean = re.sub(r'\x1b\[[0-?]*[ -/]*[@-~]', '', s)
print(repr(clean))
bits = ''.join('0' if c==' ' else '1' for c in s if c in ' \t')
print(bytes(int(bits[i:i+8],2) for i in range(0,len(bits)-7,8)))
```

Only treat spaces/tabs as a bitstream if the challenge supports that interpretation. Preserve line endings and trailing spaces. **Kali** `stegsnow -C carrier.txt` handles SNOW's specific whitespace encoding (row 143); arbitrary whitespace is not automatically SNOW.

Kitty graphics begins with `ESC _ G` and ends with `ESC \`. Parse command headers, group chunks by image/transfer ID, and join base64 payloads until `m=0`. Respect `f=24` RGB versus `f=32` RGBA, dimensions `s`/`v`, and optional zlib compression `o=z`; PNG format `f=100` is already an encoded image. Validate decoded byte length before rendering. Joining every Kitty sequence can merge different images incorrectly.

For interleaved files, save `data[0::2]` and `data[1::2]`, identify both, then inspect alternating scanlines if the decoded images are striped. Try full byte reversal only when the other end has a meaningful reversed header. Nested PNG XOR carriers need per-layer keys and chunk CRC validation, not one global key. GZSteg/SpamMimic-specific external decoders from the source are not available defaults; inspect supplied encoder code and retain the unmodified gzip stream for any format-level investigation.

## Audio: hear, inspect, and preserve samples

**Kali** FFmpeg row 47, SoX row 136, multimon-ng row 98:

```bash
ffprobe -hide_banner recording.mkv
ffmpeg -i recording.mkv -map 0:a:0 -c:a pcm_s16le track0.wav
ffmpeg -i recording.mkv -map 0:a:1 -c:a pcm_s16le track1.wav
sox track0.wav reversed.wav reverse
sox track0.wav -n spectrogram -o spectrogram.png
sox track0.wav -t raw -r 22050 -e signed-integer -b 16 -c 1 - | multimon-ng -t raw -a DTMF -
```

`0:a:1` means the second audio stream; only use it if ffprobe lists one. Converted WAV is useful for listening but **not** an exact substitute for original PCM when testing LSB data. Spectrogram window size trades time resolution against frequency resolution; inspect both full-band and a suspected band in Sonic Visualiser (Kali row 135).

Standard DTMF uses row frequencies 697/770/852/941 Hz and columns 1209/1336/1477/1633 Hz. For custom tones, split into measured symbol windows, apply a Hann window, and select one peak from each observed frequency group. A note sequence must be decoded in time order; sorting all frequencies alphabetically destroys the message. Musical note number is `round(69 + 12*log2(f/440))`, but a harmonic peak may not be the fundamental.

For MIDI files, parse events rather than rendered audio. With WSL non-AI `mido`, iterate each track's events in order, retain channel and delta-time, and distinguish Note Off from Note On with velocity zero. If the challenge deliberately alternates pairs with different pitches, test sum, XOR, or high/low-nibble combination. Do not pair two independently collected pitch lists when overlaps, channels, or unmatched notes exist.

For two almost-identical aligned tracks, subtract sample values in a wider datatype. Sample-rate mismatch, gain differences, or a one-sample delay can swamp the hidden difference. **WSL**, on original 16-bit PCM WAVs:

```python
import wave
import numpy as np
with wave.open('track0.wav','rb') as f:
    params = f.getparams(); raw0 = f.readframes(f.getnframes())
with wave.open('track1.wav','rb') as f:
    assert f.getparams() == params
    raw1 = f.readframes(f.getnframes())
assert params.sampwidth == 2
a = np.frombuffer(raw0,dtype='<i2').astype('int32')
b = np.frombuffer(raw1,dtype='<i2').astype('int32')
delta = a-b
peak = max(1,int(np.max(np.abs(delta))))
pcm = np.rint(delta * (30000/peak)).astype('<i2')
with wave.open('difference.wav','wb') as f:
    f.setparams(params); f.writeframes(pcm.tobytes())
```

Generate a spectrogram of `difference.wav`. Normalization is for viewing/listening after subtraction; preserve the raw difference if it carries exact numeric data.

For sample LSB extraction, **WSL**, original 16-bit PCM only:

```python
import wave
from pathlib import Path
import numpy as np
with wave.open('original.wav','rb') as f:
    assert f.getsampwidth()==2 and f.getcomptype()=='NONE'
    channels = f.getnchannels()
    a = np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').reshape(-1,channels)
for ch in range(channels):
    for depth in (1,2):
        bits = np.stack([(a[:,ch] >> bit) & 1 for bit in range(depth)],axis=1).ravel()
        Path(f'audio-ch{ch}-lsb{depth}.bin').write_bytes(np.packbits(bits).tobytes())
```

The bit order within each sample is a hypothesis; try its reverse if warranted. For eight-bit PCM, use unsigned samples. Inspect channel-interleaved and separate-channel layouts deliberately.

## SSTV, analog image lines, and signal caveats

**Kali row 140** calls its tool `sstv` but records installation as `pip (PySSTV)`. PySSTV is commonly an encoder package; that row does **not** prove a working decoder exists. Inspect the installed command/help before promising a decode. MMSSTV and RX-SSTV are unapproved (rows 46/69); do not replace a missing decoder with a public upload service.

A high sample rate alone does not make standard SSTV invalid. Determine actual tone frequencies, VIS/mode, sync timing, scan order, and channel durations from the signal. If a custom signal is FM-modulated, a usable **WSL SciPy/NumPy** diagnostic is instantaneous frequency from analytic phase:

```python
import numpy as np
from scipy.io import wavfile
from scipy.signal import hilbert
rate,x = wavfile.read('signal.wav')
assert x.ndim == 1, 'select the intended channel first'
x = x.astype(float)
x -= x.mean()
phase = np.unwrap(np.angle(hilbert(x)))
frequency = np.diff(phase) * rate / (2*np.pi)
np.save('instantaneous-frequency.npy',frequency)
```

Band-limit around the known carrier before phase estimation if needed. Edge transients and low-amplitude intervals are unreliable. Map frequency to intensity only after recovering sync and mode-specific line/channel boundaries. A derivative of `arccos(samples)` loses phase direction and is not a general FM decoder.

For Voyager-style amplitude images, detect separated sync pulses, measure consecutive line intervals, resample each interval to equal width, normalize globally, then try orientation/transposition. Validate against any supplied calibration image. For RF `.sub` files, `RAW_Data` normally contains signed pulse durations; cluster pulse/gap widths according to the protocol rather than discarding bytes ≥128 as “noise.”

DeepSound-like WAVs: the approved John jumbo installation may include `deepsound2john.py`; inspect its help and use it to confirm a format-specific hash before cracking. A recovered password is not an extraction implementation. DeepSound GUI is not separately approved; use a supplied encoder/format description or a permitted local non-AI implementation, and validate output length/checksums.

## Video, animation, and temporal channels

**Kali FFmpeg:**

```bash
ffprobe -hide_banner clip.mp4
mkdir frames
ffmpeg -i clip.mp4 -map 0:v:0 -fps_mode passthrough frames/frame-%06d.png
ffmpeg -i clip.mp4 -map 0:v:1 -frames:v 1 second-stream.png
```

Select `0:v:1` only if a second video stream exists. Frame extraction is for pixel analysis; it can discard hidden container padding or metadata. Keep original bytes for MJPEG post-EOI analysis and JPEG XL TOC investigation.

**WSL**, frame average, bright-pixel accumulation, and first/last difference:

```python
from pathlib import Path
from PIL import Image, ImageOps
import numpy as np
files = sorted(Path('frames').glob('*.png'))
assert files
first = np.array(Image.open(files[0]).convert('L'),dtype=float)
total, maximum, last = first.copy(), first.copy(), first
for p in files[1:]:
    last = np.array(Image.open(p).convert('L'),dtype=float)
    assert last.shape == first.shape
    total += last
    maximum = np.maximum(maximum,last)
average = Image.fromarray(np.rint(total/len(files)).astype('uint8'))
ImageOps.autocontrast(average).save('average.png')
Image.fromarray(maximum.astype('uint8')).save('maximum.png')
Image.fromarray(np.abs(last-first).astype('uint8')).save('difference.png')
```

If dark marks on a white background carry data, use per-pixel minimum instead of maximum. For consecutive-frame bit channels, compare lossless decoded frames, distinguish exact `+1` from all other changes, and retain unchanged carrier positions. Lossy compression can destroy such a channel.

GIF/APNG frames need disposal/blending semantics. Pillow's `ImageSequence.Iterator` can export displayed frames; it may convert palette modes. If the channel is in **raw GIF local color tables**, parse the original GIF table blocks; re-encoding frames to PNG is not guaranteed to preserve palette bytes. A huge number of one-pixel frames may encode a square bitmap in colors, but verify the count and ordering before reshaping.

For blinking LEDs, crop a small stable region, compute brightness per frame, threshold into on/off states, then run-length encode using actual frame timestamps. Estimate dots/dashes/gaps from the duration clusters, and include the final run. Do not assume fixed frame rate from the container alone.

For MJPEG, inspect the container's frame boundaries and JPEG markers; preserve bytes after each true EOI before the next frame. Naively splitting at every `FFD8` can encounter thumbnails or unrelated bytes. For JPEG XL progressive ordering, a full decode hides the order channel. The source's `djxl` is not listed: if the approved ImageMagick build supports JXL, inspect its format support and whether partial decodes are usable; otherwise retain TOC analysis as a format-reading task, without installing a missing decoder. Do not reuse a stale output image after a failed partial decode.

## Printing, punched cards, and optical media

Binary G-code starts `GCDE`; read version and checksum type before walking blocks. Each block has type, compression, lengths, and type-specific fields. A checksum is not always an unconditional four bytes. Heatshrink parameters and G-code text encodings depend on the format version; a decompressed block can still need decoding. WSL non-AI `heatshrink2` is permitted by Windows row 14 when needed, but validate output against declared length. `qoif` thumbnails contain big-endian width/height and RGB/RGBA channel metadata.

For **plain G-code with absolute XYZ/extrusion**, save this **WSL** projection as `gcode.svg`. It tracks modal coordinates and draws only increasing-extrusion moves. It rejects relative-coordinate modes instead of silently rendering them incorrectly.

```python
from pathlib import Path
import re
state = dict(X=0.,Y=0.,Z=0.,E=0.)
segments = []
for line in Path('print.gcode').read_text().splitlines():
    line = line.split(';',1)[0].strip()
    if not line: continue
    command = line.split()[0]
    if command in ('G91','M83'):
        raise ValueError('relative mode: extend parser before proceeding')
    values = {k:float(v) for k,v in re.findall(r'([XYZE])\s*(-?\d+(?:\.\d+)?)',line)}
    previous = state.copy()
    if command in ('G0','G1','G92'): state.update(values)
    if command == 'G1' and state['E'] > previous['E']:
        segments.append((previous['X'],previous['Z'],state['X'],state['Z']))
assert segments
xs = [s[i] for s in segments for i in (0,2)]
zs = [s[i] for s in segments for i in (1,3)]
x0,z0 = min(xs)-1,min(zs)-1
w,h = max(xs)-x0+1,max(zs)-z0+1
body = ''.join(f'<line x1="{a}" y1="{-b}" x2="{c}" y2="{-d}"/>' for a,b,c,d in segments)
Path('gcode.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0} {-z0-h} {w} {h}"><g stroke="black" stroke-width="0.1">{body}</g></svg>')
```

Switch projection to XY/YZ or restrict Y ranges when side lettering overlaps. Arc moves G2/G3 need interpolation; the script intentionally handles only G0/G1/G92.

Punched cards: calibrate the 80-column ×12-row grid, label rows `12,11,0,1,…,9`, and record hole combinations per column. Map digit single-punches and zone+digit letters using the supplied code chart; row 12 alone is not “A.” Contrast, perspective, and punctuation variants need manual verification.

CDDA with only two dominant byte values can encode a disc image rather than normal audio. A specialized encoder may pre-interleave bytes to compensate for CIRC; this is not a general raw-audio decoder. Use the supplied calibration pair to establish the 24-byte channel permutation/delays, then render polar rings with increasing bytes-per-revolution. Tune initial circumference and radial increment against calibration before decoding the unknown file. Preserve sample order; assuming every `.cdda` uses one historical tool's constants produces plausible but wrong images.

## Statistical traces without AI

For power traces, determine axes from the challenge data description. Average repeated measurements, inspect per-sample variance, and compare hypotheses using an explicit leakage model. “Largest power is the correct digit” is only valid for a challenge whose implementation has that behavior. Report stability across separate trace subsets rather than one maximum.

For keyboard audio, manually segment keypress transients, compare waveform/spectral shapes to supplied labeled references, and corroborate uncertain positions with context. The source's KNN/scikit-learn route is excluded by the AI/ML restriction. Do not replace it with another learned classifier under a different name.

Source material adapted: `ctf-forensics/steganography.md`, `stego-image.md`, `stego-advanced.md`, `stego-advanced-2.md`, `3d-printing.md`, and media portions of `signals-and-hardware.md`/`SKILL.md`. Unsupported online decoders, blanket installers, genetic/ML solvers, and sample-specific assumptions were removed or replaced with bounded local workflows.
