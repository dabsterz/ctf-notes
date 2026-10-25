"""Walk PNG chunk boundaries and save bytes after IEND. CRC issues are reported, not repaired."""
import argparse
import struct
import zlib
from pathlib import Path


def inspect(data):
    if data[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError('bad PNG signature')
    pos, checks = 8, []
    while pos+12 <= len(data):
        size = struct.unpack_from('>I', data, pos)[0]
        kind = data[pos+4:pos+8]
        end = pos+12+size
        if end > len(data):
            raise ValueError('chunk extends beyond file')
        crc = struct.unpack_from('>I', data, pos+8+size)[0]
        checks.append((kind, size, zlib.crc32(data[pos+4:pos+8+size]) == crc))
        pos = end
        if kind == b'IEND':
            if size != 0:
                raise ValueError('IEND must have length zero')
            return data[pos:], checks
    raise ValueError('no complete IEND chunk')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('input')
    ap.add_argument('--out', default='png-trailer.bin')
    args = ap.parse_args()
    try:
        path = Path(args.input)
        if path.stat().st_size > 64_000_000:
            raise ValueError('input exceeds 64 MB budget')
        tail, checks = inspect(path.read_bytes())
        for kind, size, valid in checks:
            print(kind, size, 'CRC OK' if valid else 'BAD CRC: inspect before trusting the structure')
        Path(args.out).write_bytes(tail)
        print('trailing bytes:', len(tail), 'preview:', repr(tail[:200]))
        print('saved:', args.out)
        print('Chunk walk only; not a full PNG validity check.')
    except (ValueError, OSError) as exc:
        ap.exit(1, f'PNG inspection stopped: {exc}\n')


if __name__ == '__main__':
    main()
