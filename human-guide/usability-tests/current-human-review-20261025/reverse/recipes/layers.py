"""Strict Base64 decode; optionally decompress one zlib/gzip layer, keeping both."""
import argparse
import base64
import zlib
from pathlib import Path


def decode(raw, limit=16_000_000):
    if len(raw) > limit:
        raise ValueError('encoded input exceeds size budget')
    first = base64.b64decode(b''.join(raw.split()), validate=True)
    gzip = first.startswith(b'\x1f\x8b')
    zheader = len(first) >= 2 and first[0] & 15 == 8 and first[0] >> 4 <= 7 and int.from_bytes(first[:2], 'big') % 31 == 0
    if not (gzip or zheader):
        return first, None, b''
    dec = zlib.decompressobj(31 if gzip else 15)
    second = dec.decompress(first, limit+1)
    if len(second) > limit or dec.unconsumed_tail:
        raise ValueError('decompressed output exceeds size budget')
    if not dec.eof:
        raise ValueError('compressed stream is truncated or needs a different format')
    return first, second, dec.unused_data


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('input')
    ap.add_argument('--out', default='decoded', help='new output directory; existing directory is refused')
    args = ap.parse_args()
    try:
        path = Path(args.input)
        if path.stat().st_size > 16_000_000:
            raise ValueError('input exceeds 16 MB budget')
        first, second, trailer = decode(path.read_bytes())
        out = Path(args.out)
        out.mkdir(exist_ok=False)
        (out/'layer1.bin').write_bytes(first)
        print('layer1:', len(first), 'bytes; header:', first[:8].hex())
        if second is not None:
            (out/'layer2.bin').write_bytes(second)
            print('layer2:', len(second), 'bytes; preview:', repr(second[:200]))
            if trailer:
                (out/'trailing.bin').write_bytes(trailer)
            print('complete compressed stream; extra trailing bytes:', len(trailer))
        else:
            print('no zlib/gzip header; inspect layer1:', repr(first[:200]))
        print('saved in:', out)
    except (ValueError, OSError, zlib.error) as exc:
        ap.exit(1, f'Decoding stopped: {exc}\n')


if __name__ == '__main__':
    main()
