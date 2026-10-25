import json
from pathlib import Path

def rol8(value, amount):
    amount %= 8
    return ((value << amount) | (value >> ((8 - amount) % 8))) & 0xff

def ror8(value, amount):
    return rol8(value, -amount)

for value in range(256):
    for amount in range(8):
        assert ror8(rol8(value, amount), amount) == value
print('all byte rotations round-trip')

j = json.loads(Path(__file__).with_name('checker.json').read_text())
key = bytes.fromhex(j['key_hex'])
candidate = bytes(ror8(y, j['rotation']) ^ key[i % len(key)] for i, y in enumerate(j['expected']))
print('candidate:', candidate.decode('ascii'))
forward = [rol8(x ^ key[i % len(key)], j['rotation']) for i, x in enumerate(candidate)]
print('forward:', forward)
assert forward == j['expected']
print('comparison matches')
