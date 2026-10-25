"""Edit a JWT payload locally. This does NOT generate a valid signature."""
import argparse
import base64
import json
from pathlib import Path


def mutate(token, claim, value):
    header, payload, signature = token.strip().split('.')
    obj = json.loads(base64.urlsafe_b64decode(payload + '=' * (-len(payload) % 4)))
    if not isinstance(obj, dict):
        raise ValueError('JWT payload must be a JSON object')
    obj[claim] = json.loads(value)
    encoded = base64.urlsafe_b64encode(json.dumps(obj, separators=(',', ':')).encode()).rstrip(b'=').decode()
    return '.'.join((header, encoded, signature))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('input', help='text file containing only the captured JWT')
    ap.add_argument('--claim', default='role')
    ap.add_argument('--value', default='"admin"', help='JSON value; default is string admin')
    ap.add_argument('--out', default='edited-token.txt')
    args = ap.parse_args()
    try:
        token = mutate(Path(args.input).read_text(encoding='utf-8-sig'), args.claim, args.value)
        Path(args.out).write_text(token, encoding='ascii')
        print('saved:', args.out)
        print('Signature unchanged and invalid for edited payload. Only a server response can establish acceptance.')
    except (ValueError, TypeError, OSError) as exc:
        ap.exit(1, f'JWT stopped: {exc}\n')


if __name__ == '__main__':
    main()
