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
