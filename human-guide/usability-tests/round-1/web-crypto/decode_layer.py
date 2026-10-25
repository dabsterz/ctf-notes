from pathlib import Path
import base64, zlib

encoded = ''.join(Path('message.txt').read_text().split())
raw = base64.b64decode(encoded, validate=True)
Path('layer1.bin').write_bytes(raw)
if raw.startswith(b'\x1f\x8b'):
    mode = 31  # gzip wrapper
elif len(raw) >= 2 and (raw[0]*256 + raw[1]) % 31 == 0 and raw[0] & 15 == 8:
    mode = 15  # plausible zlib wrapper; still requires validation
else:
    print('no supported compression wrapper; inspect layer1.bin')
    raise SystemExit
dec = zlib.decompressobj(mode)
out = dec.decompress(raw, 16_000_001)
if len(out) > 16_000_000 or dec.unconsumed_tail:
    raise ValueError('output limit reached')
assert dec.eof, 'incomplete compressed stream'
Path('layer2.bin').write_bytes(out)
print('decoded bytes:', len(out), 'unused trailing bytes:', len(dec.unused_data))
# Added basic text inspection; transformations above are from the guide.
print('layer 1 header:', raw[:2].hex(), 'length:', len(raw))
print('layer 2 bytes:', out)
print('layer 2 text:', out.decode('utf-8'))
