"""Synthetic usability-test fixtures. Reviewers must not read this generator."""
import base64
import hashlib
import json
import struct
import zlib
from pathlib import Path

root = Path(__file__).resolve().parent
answers = {}

def write(group, filename, data):
    folder = root / group
    folder.mkdir(exist_ok=True)
    (folder / filename).write_bytes(data if isinstance(data, bytes) else data.encode())

def answer(name, value):
    answers[name] = {'expected': value, 'sha256': hashlib.sha256(value.encode()).hexdigest()}

write('web-crypto', 'START.md', '''# Test brief
You have three independent local practice tasks. Use only the human guide as your technical reference.
1. An HTTP challenge runs at http://127.0.0.1:18765. GET /session gives your token. GET /flag expects Authorization: Bearer TOKEN. Obtain the flag using a weakness you can explain. Source review established that the server decodes the JWT payload without signature verification; it requires role=admin. Do not inspect the server implementation.
2. rsa.json contains an RSA ciphertext and its public key. Source confirms raw textbook RSA with no padding. Recover the plaintext bytes.
3. message.txt contains a message that a supplied sender encoded as Base64 after compressing with zlib. Recover the text, preserving each layer.
Common lookup: you are at the Windows workstation, need radare2, and cannot find it in WSL. Determine which supplied environment lists radare2 and name one listed local alternative for static reverse engineering on Windows/WSL.
''')
p, q = 32416190071, 32416187567
message = b'CTF{rsa}'
n = p*q
assert int.from_bytes(message,'big') < n
assert pow(pow(int.from_bytes(message,'big'),65537,n),pow(65537,-1,(p-1)*(q-1)),n) == int.from_bytes(message,'big')
write('web-crypto', 'rsa.json', json.dumps({'n':n, 'e':65537, 'c':pow(int.from_bytes(message,'big'),65537,n)}, indent=2))
answer('rsa', message.decode())
message = 'CTF{layers_are_bytes}'
write('web-crypto', 'message.txt', base64.b64encode(zlib.compress(message.encode())))
answer('layers', message)
answer('web', 'CTF{verify_the_signature}')

def chunk(kind, data):
    return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data))
png = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR',struct.pack('>IIBBBBB',1,1,8,2,0,0,0)) + chunk(b'IDAT',zlib.compress(b'\0\xff\0\0')) + chunk(b'IEND',b'')
write('forensics', 'START.md', '''# Test brief
You have three independent local practice tasks. Use only the human guide as your technical reference.
1. carrier.png is a valid tiny image, but its size is larger than its visible content suggests. Recover the hidden text.
2. evidence.tar contains multiple versions of a document under the same member name. Recover all versions and identify the flag from the earlier version without overwriting it.
3. events.json is an exported Windows process-creation event. Find the UTC creation time and full command line for the suspicious executable. Explain what this event proves.
Common lookup: you are at the Windows workstation, need radare2, and cannot find it in WSL. Determine which supplied environment lists radare2 and name one listed local alternative for static reverse engineering on Windows/WSL.
''')
message = 'CTF{after_the_real_iend}'
write('forensics','carrier.png',png+message.encode())
answer('png',message)
import io
import tarfile
with tarfile.open(root/'forensics/evidence.tar','w') as archive:
    for data in [b'CTF{keep_duplicate_members}',b'Latest revision: no useful text.']:
        info=tarfile.TarInfo('report.txt');info.size=len(data)
        archive.addfile(info,io.BytesIO(data))
answer('tar','CTF{keep_duplicate_members}')
write('forensics','events.json',json.dumps({'EventID':4688,'TimeCreated':'2026-10-25T01:02:03Z','NewProcessName':r'C:\Temp\odd.exe','ProcessCommandLine':r'C:\Temp\odd.exe --config C:\Temp\settings.ini'},indent=2))
answer('event',r'2026-10-25T01:02:03Z | C:\Temp\odd.exe --config C:\Temp\settings.ini')

write('reverse-misc','START.md', '''# Test brief
You have three independent local practice tasks. Use only the human guide as your technical reference.
1. checker.json describes the byte transform extracted from a native checker. Recover its accepted ASCII input. For each input byte x at position i: y=ROL8(x XOR key[i % key_length], 3); compare y with expected[i].
2. crash.bin contains four bytes copied in increasing memory-address order from a corrupted return slot. The input was generated with the exact de_bruijn(b'abcdefgh',4) pattern in the human guide, truncated to 512 bytes. Find the offset.
3. payload.json is a short custom VM program. It starts with accumulator zero and has instructions: LOAD byte, XOR byte, ADD byte (wrap at 8 bits), CMP byte, HALT. Determine the required input byte and verify the comparison. The program reads your input through LOAD_INPUT (no operand).
Common lookup: you are at the Windows workstation, need radare2, and cannot find it in WSL. Determine which supplied environment lists radare2 and name one listed local alternative for static reverse engineering on Windows/WSL.
''')
message=b'CTF{invert_in_order}'
key=b'key'
rol=lambda x: ((x<<3)|(x>>5))&255
write('reverse-misc','checker.json',json.dumps({'key_hex':key.hex(),'rotation':3,'expected':[rol(x^key[i%len(key)]) for i,x in enumerate(message)]},indent=2))
answer('checker',message.decode())
def debruijn():
    a=[0]*32; result=[]
    def visit(t,p):
        if t>4:
            if 4%p==0: result.extend(a[1:p+1])
        else:
            a[t]=a[t-p];visit(t+1,p)
            for j in range(a[t-p]+1,8):a[t]=j;visit(t+1,t)
    visit(1,1)
    return bytes(b'abcdefgh'[x] for x in result)
write('reverse-misc','crash.bin',debruijn()[173:177])
answer('offset','173')
write('reverse-misc','payload.json',json.dumps({'program':[['LOAD_INPUT'],['XOR',35],['ADD',7],['CMP',(ord('K')^35)+7],['HALT']]},indent=2))
answer('vm','K')
(root/'answer-key.json').write_text(json.dumps(answers,indent=2),encoding='utf-8')
print('Prepared nine synthetic tasks in three isolated fixture directories.')
