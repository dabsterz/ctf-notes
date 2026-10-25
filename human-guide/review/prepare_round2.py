"""Parent-only fixture preparation. Reviewers must not read this or answer-key.json."""
import base64
import io
import json
from pathlib import Path
import struct
import subprocess
import sys
import tarfile
import tempfile
import zlib

GUIDE = Path(__file__).resolve().parents[1]
ROOT = GUIDE/'usability-tests/round-2'
for folder in ('web-crypto','forensics','reverse-misc','reports'):
    (ROOT/folder).mkdir(parents=True,exist_ok=True)
key = dict(web='CTF{new_request_verified}',rsa='R2_RSA',layers='CTF{new_layer}',png='CTF{new_png_tail}',
           tar='CTF{older_tar_entry}',event='2026-10-25T03:04:05Z | C:\\Temp\\runner.exe --mode audit',
           checker='CTF{new_transform}',offset='281',vm='Z')
def write(folder,name,data):
    path = ROOT/folder/name
    path.write_text(json.dumps(data,indent=2),encoding='utf-8')
p,q=32416190071,32416187567
write('web-crypto','rsa.json',dict(n=p*q,e=65537,c=pow(int.from_bytes(key['rsa'].encode(),'big'),65537,p*q)))
(ROOT/'web-crypto/message.txt').write_bytes(base64.b64encode(zlib.compress(key['layers'].encode())))
def enc(data):return base64.urlsafe_b64encode(json.dumps(data).encode()).rstrip(b'=')
(ROOT/'web-crypto/token.txt').write_bytes(enc({'alg':'HS256'})+b'.'+enc({'sub':'round2','role':'user'})+b'.invalid')
def chunk(kind,data): return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data))
png=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',1,1,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(b'\0\x11\x22\x33'))+chunk(b'IEND',b'')
(ROOT/'forensics/carrier.png').write_bytes(png+key['png'].encode())
with tarfile.open(ROOT/'forensics/evidence.tar','w') as tf:
    for value in (key['tar'].encode(),b'The later copy contains no answer.'):
        info=tarfile.TarInfo('note.txt');info.size=len(value);tf.addfile(info,io.BytesIO(value))
write('forensics','events.json',dict(Provider='Microsoft-Windows-Security-Auditing',EventID=4688,
      TimeCreated='2026-10-25T03:04:05Z',NewProcessName='C:\\Temp\\runner.exe',CommandLine='C:\\Temp\\runner.exe --mode audit'))
secret=b'newkey';r=5
def rol(x,r):return ((x<<r)|(x>>(8-r)))&255
write('reverse-misc','checker.json',dict(key_hex=secret.hex(),rotation=r,
      expected=[rol(x^secret[i%len(secret)],r) for i,x in enumerate(key['checker'].encode())]))
with tempfile.TemporaryDirectory() as tmp:
    subprocess.run([sys.executable,str(GUIDE/'recipes/pattern.py'),'--length','512'],cwd=tmp,check=True)
    pattern=(Path(tmp)/'pattern.bin').read_bytes()
(ROOT/'reverse-misc/crash.bin').write_bytes(pattern[281:285])
write('reverse-misc','vm.json',dict(program=[['LOAD_INPUT'],['XOR',18],['ADD',9],['CMP',81],['HALT']]))
(ROOT/'answer-key.json').write_text(json.dumps(key,indent=2),encoding='utf-8')
briefs={
 'web-crypto': '1. token.txt is the captured JWT from a loopback app known to omit signature verification. Its flag endpoint is http://127.0.0.1:18766/flag. Recover the flag, recording baseline and edited responses.\n2. Recover raw RSA plaintext from rsa.json; try a bounded close-prime test.\n3. Decode message.txt (Base64 wrapping compressed bytes).\n4. Choose tools for hidden web paths, an offline password hash, and a live SSH login. Explain the differences; do not perform network guessing.\n',
 'forensics': '1. Recover bytes appended after the real PNG end in carrier.png.\n2. Recover the earlier version of note.txt from evidence.tar, keeping both occurrences.\n3. Read events.json and state timestamp, full command line, what the event establishes and what it cannot establish.\n4. Choose tools/environments for disk images, memory dumps and a PCAP; explain one weakness each.\n',
 'reverse-misc': '1. checker.json gives expected[i] = ROL8(input[i] XOR repeated key[i], rotation). Recover input and verify forward.\n2. crash.bin is four bytes in memory order from the guide pattern; the input sent was 512 bytes. Find and verify the offset.\n3. vm.json contains a straight-line 8-bit input-check VM. LOAD_INPUT loads one byte; XOR and ADD modify it; CMP must match; HALT ends. Recover input.\n4. Choose an approved static Windows/WSL alternative to radare2; compare tools for native, .NET and Android binaries.\n'}
for folder,brief in briefs.items():
    (ROOT/folder/'START.md').write_text('# Round 2 assigned tasks\n\n'+brief,encoding='utf-8')
server=(GUIDE/'usability-tests/round-1/server.py').read_text(encoding='utf-8')
server=server.replace('18765','18766').replace('CTF{verify_the_signature}',key['web'])
(ROOT/'server.py').write_text(server,encoding='utf-8')
print('Prepared nine new tasks. Hidden key is for parent verification only.')
