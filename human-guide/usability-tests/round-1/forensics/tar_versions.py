import tarfile
from pathlib import Path

out = Path('out/tar-members')
out.mkdir(parents=True, exist_ok=True)
total = 0
with tarfile.open('evidence.tar') as tf:
    for i, member in enumerate(tf):
        if not member.isfile():
            continue
        total += member.size
        if member.size > 64_000_000 or total > 512_000_000:
            raise ValueError('extraction budget exceeded')
        src = tf.extractfile(member)
        assert src is not None
        data = src.read(member.size + 1)
        assert len(data) == member.size
        (out / f'{i:06d}.bin').write_bytes(data)
        print(i, repr(member.name), member.size)
