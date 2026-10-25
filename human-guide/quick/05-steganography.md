# Steganography

[Tool placement and competition rules](00-tool-rules.md). Preserve originals. Enter paths when prompted; run `recipes/` commands from the extracted guide root.

## Quick: inspect metadata and embedded signatures

**WSL · ExifTool, xxd, strings, binwalk**

```bash
read -r -p 'Carrier file path: ' FILE
exiftool -a -u -g1 "$FILE"
xxd -l 256 "$FILE"
strings -a -n 6 "$FILE"
binwalk "$FILE"
```

For a JPEG thumbnail:

```bash
read -r -p 'JPEG path: ' FILE
exiftool -b -ThumbnailImage "$FILE" > thumbnail.jpg
```

**Look for:** comments, passwords, embedded headers and a different thumbnail crop.
**If not:** inspect structural boundaries; binwalk matches can be false positives.

## Quick: inspect PNG structure and appended bytes

**Kali · pngcheck**

```bash
read -r -p 'PNG path: ' FILE
pngcheck -v "$FILE"
```

**WSL · Python**

```bash
read -r -p 'PNG path: ' FILE
python3 recipes/png_tail.py "$FILE" --out png-trailer.bin &&
xxd -l 128 png-trailer.bin &&
strings -a -n 6 png-trailer.bin
```

**Look for:** chunk/CRC errors and nonempty data after the true IEND.
**If not:** inspect bitplanes; do not globally replace header-like byte strings.

## Quick: extract a promising PNG/BMP bitplane

**WSL · zsteg**

```bash
read -r -p 'PNG or BMP path: ' FILE
zsteg -a "$FILE"
```

Copy a promising selector from that output:

```bash
read -r -p 'PNG or BMP path: ' FILE
read -r -p 'Exact zsteg selector from analysis: ' SELECTOR
zsteg -E "$SELECTOR" "$FILE" > extracted.bin
xxd -l 128 extracted.bin
strings -a -n 6 extracted.bin
```

**Look for:** a valid file or structured message, not isolated printable fragments.
**If not:** inspect channels visually in Kali StegSolve: File → Open → cycle views with arrows.

## Quick: open a steghide carrier

**Kali · steghide**, JPEG/BMP/WAV/AU; enter the clue-derived password at the prompt.

```bash
read -r -p 'Carrier path: ' FILE
steghide info "$FILE"
steghide extract -sf "$FILE" -xf recovered.bin
```

**Kali · stegseek**, using your clue-derived local wordlist:

```bash
read -r -p 'Carrier path: ' FILE
read -r -p 'Password wordlist path: ' WORDS
stegseek "$FILE" "$WORDS" recovered-from-wordlist.bin
```

**Look for:** an extracted file with a valid format.
**If not:** a failed password does not prove absence; PNG needs another route.

## Quick: decode a visible barcode or QR

**WSL · ZBar**

```bash
read -r -p 'Barcode image path: ' FILE
zbarimg --raw "$FILE"
```

**Look for:** complete decoded text or a next-layer encoding.
**If not:** inspect orientation, missing finder patterns, contrast and quiet border; keep repairs separate.

## Quick: inspect a PDF beyond the rendered page

**WSL · pdftotext, qpdf**

```bash
read -r -p 'PDF path: ' FILE
pdftotext -layout "$FILE" pdf-text.txt
qpdf --check "$FILE"
qpdf --qdf --object-streams=disable "$FILE" expanded.pdf
strings -a -n 6 expanded.pdf > pdf-strings.txt
```

**Look for:** text hidden by layout, annotations, object streams and attachments.
**If not:** compare rendered pages with extracted text; consult the full reference for object-level recovery.

## Quick: reveal audio tones or spectrogram text

**Kali · SoX**

```bash
read -r -p 'Audio path: ' FILE
sox "$FILE" -n spectrogram -o spectrogram.png
sox "$FILE" reversed.wav reverse
```

For suspected standard DTMF:

```bash
read -r -p 'Audio path: ' FILE
sox "$FILE" -t raw -r 22050 -e signed-integer -b 16 -c 1 - |
  multimon-ng -t raw -a DTMF -
```

**Kali · Audacity:** File → Open → select audio → track dropdown → Spectrogram; zoom the suspicious interval.

**Look for:** letter shapes, reversed speech or stable tone pairs.
**If not:** inspect separate channels; preserve original PCM for sample-bit analysis.

## Quick: extract video frames and audio tracks

**Kali · FFmpeg** — inspect stream listings before selecting tracks.

```bash
read -r -p 'Video path: ' FILE
ffprobe -hide_banner "$FILE"
read -r -p 'New frames directory: ' OUT
mkdir "$OUT" && ffmpeg -i "$FILE" -map 0:v:0 -fps_mode passthrough "$OUT/frame-%06d.png"
ffmpeg -i "$FILE" -map 0:a:0 -c:a pcm_s16le track0.wav
```

**Look for:** single-frame messages, secondary streams and changing pixels.
**If not:** compare frames/channels using the full reference; pixel exports omit container padding.
