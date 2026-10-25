"""Parent-only checks of saved outputs and the frozen review snapshot."""
import base64
import hashlib
import json
from pathlib import Path
import struct
import tarfile
import zlib

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
snapshot = json.loads((HERE / 'snapshot.json').read_text())
changed = [name for name, digest in snapshot['sha256'].items()
           if hashlib.sha256((REPO / name).read_bytes()).hexdigest() != digest]
assert not changed, changed
checks = {}
f = HERE / 'forensics'
png = (f / 'holiday.png').read_bytes()
position = 8
while position < len(png):
    length = struct.unpack('>I', png[position:position + 4])[0]
    kind = png[position + 4:position + 8]
    position += length + 12
    if kind == b'IEND':
        break
checks['PNG trailer matches bytes after IEND'] = (f / 'png-trailer.bin').read_bytes() == png[position:]
with tarfile.open(f / 'backup.tar') as archive:
    versions = [archive.extractfile(member).read() for member in archive if member.isfile()]
for folder in ['tar-parts', 'tar-parts-retry']:
    recovered = [p.read_bytes() for p in sorted((f / folder).glob('*.bin'))]
    checks[folder + ': both versions retained in order'] = recovered == versions and len(versions) == 2

r = HERE / 'reverse'
model = json.loads((r / 'compare.json').read_text())
plain = (r / 'checker-plain.bin').read_bytes()
key = bytes.fromhex(model['key_hex'])
rotation = model['rotation']
transformed = []
for i, value in enumerate(plain):
    value ^= key[i % len(key)]
    transformed.append(((value << rotation) | (value >> (8 - rotation))) & 255)
checks['Recovered checker input forward-verifies'] = transformed == model['expected']
accepted = [value for value in range(256) if ((value ^ 43) + 17) & 255 == 116]
checks['Decoded VM has unique accepted byte 72'] = accepted == [72]
pattern = (r / 'pattern.bin').read_bytes()
needle = bytes.fromhex('61 61 68 62')
offset = pattern.find(needle)
checks['Crash bytes unique within 512-byte sent input'] = len(pattern) == 512 and offset >= 0 and pattern.count(needle) == 1

w = HERE / 'web-crypto'
rsa = json.loads((w / 'numbers.json').read_text())
p, q = 32416187567, 32416190071
assert p * q == rsa['n']
m = pow(rsa['c'], pow(rsa['e'], -1, (p - 1) * (q - 1)), rsa['n'])
checks['RSA output matches independent modular arithmetic'] = int.from_bytes((w / 'rsa-plain.bin').read_bytes(), 'big') == m and pow(m, rsa['e'], rsa['n']) == rsa['c']
expected = zlib.decompress(base64.b64decode((w / 'note.txt').read_bytes()))
checks['Layered output matches independent Base64/zlib decoding'] = (w / 'decoded-note/layer2.bin').read_bytes() == expected
expected = base64.b64decode((w / 'labeled.txt').read_text().strip().split('=', 1)[1])
checks['Labeled Base64 output matches independent decoding'] = (w / 'decoded-labeled-value/layer1.bin').read_bytes() == expected

scores = {}
for role in ['forensics', 'reverse', 'web-crypto']:
    rating = json.loads((HERE / role / 'rating.json').read_text(encoding='utf-8-sig'))
    values = rating['scores']
    assert set(values) == {'findability', 'commands', 'clarity', 'economy', 'recovery'}
    assert all(isinstance(value, (int, float)) and 0 <= value <= 10 for value in values.values())
    mean = sum(values.values()) / 5
    assert abs(mean - rating['overall']) < 0.051, (role, mean, rating['overall'])
    scores[role] = {'dimensions': values, 'mean': mean}
result = {'commit': snapshot['commit'], 'frozen_files': len(snapshot['sha256']),
          'changed_guide_files': changed, 'artifact_checks': checks, 'crash_offset': offset,
          'scores': scores, 'overall_mean': sum(s['mean'] for s in scores.values()) / 3,
          'scope': 'Parent verifies outputs, hashes and score arithmetic; qualitative judgments remain those of the independent reviewers. VM byte and event interpretation additionally cross-checked in written reports.'}
(HERE / 'validation.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result, indent=2))
assert all(checks.values())
