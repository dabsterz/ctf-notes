"""Keep every regular tar member, including duplicate names, without trusting archive paths."""
import argparse
import json
import tarfile
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('input')
    ap.add_argument('--out', default='tar-parts', help='new output directory')
    args = ap.parse_args()
    try:
        out = Path(args.out)
        out.mkdir(exist_ok=False)
        total = 0
        with tarfile.open(args.input, 'r:*') as tf, (out/'manifest.jsonl').open('w', encoding='utf-8') as log:
            for i, member in enumerate(tf):
                if i >= 10000:
                    raise ValueError('member-count budget exceeded')
                if not member.isfile():
                    continue
                total += member.size
                if member.size > 64_000_000 or total > 512_000_000:
                    raise ValueError('extraction budget exceeded; earlier members retained')
                src = tf.extractfile(member)
                if src is None:
                    raise ValueError('regular file has no readable body')
                with src:
                    data = src.read(member.size+1)
                if len(data) != member.size:
                    raise ValueError('truncated member')
                name = f'{i:06d}.bin'
                (out/name).write_bytes(data)
                log.write(json.dumps(dict(index=i, name=member.name, saved=name, size=len(data)))+'\n')
                print(name, repr(member.name), len(data), 'bytes; preview:', repr(data[:120]))
        print('manifest:', out/'manifest.jsonl')
    except (ValueError, OSError, tarfile.TarError) as exc:
        ap.exit(1, f'Tar extraction stopped: {exc}\n')


if __name__ == '__main__':
    main()
