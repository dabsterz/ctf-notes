# Network captures and hardware signals

**Quick route:** [Short commands](../QUICKSTART.md#network-conversation) · [Tool strengths and weaknesses](../TOOL-CHOOSER.md#network). Use this chapter for deeper explanations.

Start by identifying the conversation, direction, and transport framing. Then recover application bytes. Most failed network solves come from decoding packet fragments as if they were already a complete file.

## Machine and scope

**Windows native:** Wireshark and TShark, Windows workbook rows 9 and 43. **WSL:** Zeek and can-utils, Windows rows 25 and 23; Python standard-library scripts, Windows row 14. **Kali:** tcpdump row 149; aircrack-ng row 10; hashcat row 66; John row 80; rtptools row 129. These are distinct inventories: TShark's Windows listing does not imply a Kali installation.

All capture operations below are offline. Do not replay packets, poison ARP, reset other teams' connections, or contact a captured C2 address. Only challenge-designated endpoints are in scope under the [event rules](https://ajccbc.ncsa.or.th/cyber-sea-game-2026/). Public upload analysis is prohibited.

In **PowerShell**, define TShark once and work inside your case directory:

```powershell
$tshark = 'C:\Program Files\Wireshark\tshark.exe'
New-Item -ItemType Directory -Force out | Out-Null
& $tshark --version
& $tshark -r capture.pcapng -q -z io,phs
& $tshark -r capture.pcapng -q -z conv,tcp
& $tshark -r capture.pcapng -q -z conv,udp
& $tshark -r capture.pcapng -q -z endpoints,ip
```

`capture.pcapng` is your supplied capture. Record endpoints, byte-heavy flows, unusual protocols, and interface IDs. A protocol label is a dissector's interpretation; TLS on port 443 can still be a fake label over custom bytes.

## Read filters correctly

| Question | Wireshark/TShark display filter |
|---|---|
| All traffic involving one IPv4 host | `ip.addr == 192.0.2.10` |
| One direction only | `ip.src == 192.0.2.10` |
| One reconstructed TCP conversation | `tcp.stream == 3` |
| HTTP uploads | `http.request.method == "POST"` |
| DNS queries without replies | `dns.flags.response == 0` |
| ICMP echo requests | `icmp.type == 8` |
| SYN-ACK responses | `tcp.flags.syn == 1 && tcp.flags.ack == 1` |
| One pcapng interface | `frame.interface_id == 2` |

The IP and stream values above are examples; replace them with observed values. TShark `-Y` uses display filters. tcpdump uses a different capture-filter language:

```bash
# Kali: read only the supplied capture, do not capture a live interface.
tcpdump -nn -r capture.pcap 'host 192.0.2.10 and tcp port 80'
tcpdump -nn -A -r capture.pcap 'tcp port 80'
```

Disabling name resolution avoids unexpected external lookups. A SYN-ACK suggests a responding TCP listener, not the identity or version of its application. In Wireshark, disable network name resolution when reviewing unknown addresses.

## HTTP, credentials, and files

**Windows PowerShell:**

```powershell
& $tshark -n -r capture.pcapng -Y http.request -T fields -E header=y `
  -e frame.number -e tcp.stream -e http.request.method -e http.host -e http.request.uri
& $tshark -n -r capture.pcapng --export-objects http,out/http
& $tshark -n -r capture.pcapng -q -z 'follow,tcp,ascii,3'
```

Expected result: a short list of requests and exported response objects. For POST uploads, inspect the request's reassembled body and multipart boundaries; **Export Objects is not guaranteed to export every upload**. In Wireshark, select the relevant stream, **Follow → TCP Stream**, choose one direction, select **Raw**, and save to `out/request.bin`.

For a saved HTTP request with MIME `Content-Type` and an already dechunked body, this **WSL Python** script extracts attachment parts without trusting their filenames:

```python
from pathlib import Path
from email import policy
from email.parser import BytesParser

raw = Path('out/request.bin').read_bytes()
head, sep, body = raw.partition(b'\r\n\r\n')
assert sep, 'HTTP header terminator missing'
headers = head.split(b'\r\n')[1:]  # remove HTTP request line
if any(h.lower().startswith(b'transfer-encoding:') for h in headers):
    raise ValueError('dechunk the HTTP body first')
message = BytesParser(policy=policy.default).parsebytes(
    b'MIME-Version: 1.0\r\n' + b'\r\n'.join(headers) + b'\r\n\r\n' + body)
assert message.is_multipart(), 'not a multipart body'
for i, part in enumerate(message.iter_parts()):
    payload = part.get_payload(decode=True)
    if payload is not None:
        Path(f'out/part-{i:03d}.bin').write_bytes(payload)
        print(i, part.get_filename(), len(payload))
```

Inspect HTML/XML/JSON exports for application names, version hints, usernames, and configuration files. A captured shell stream may show `.env`, `wp-config.php`, or database passwords. Those are evidence; do not test them outside the challenge. For email, preserve the full headers, MIME boundaries, and transfer encoding; decode each attachment individually with Python's `email` parser.

## TCP reassembly is not hex concatenation

Concatenating every `tcp.payload` duplicates retransmissions, interleaves both directions, and ignores gaps. Prefer Wireshark's Follow Stream reassembly. To investigate failures, export sequence metadata:

```powershell
& $tshark -n -r capture.pcapng -Y 'tcp.stream == 3 && tcp.len > 0' `
  -T fields -E header=y -E separator=, -E quote=d `
  -e frame.number -e ip.src -e tcp.seq_raw -e tcp.len -e tcp.payload |
  Set-Content -Encoding ascii out\segments.csv
```

Look for identical sequence ranges, overlaps with conflicting bytes, and missing sequence ranges. A saved Follow Stream file containing gap markers is not a byte-perfect recovered file. Handle sequence-number wraparound and keep each direction separate unless the **application implementation** proves shared cipher state.

For split archive transfers, export each object, find the first fragment's magic, and recover ordering from explicit part indices or captured directory-listing timestamps. Saved local modification times usually describe your export, not the sender. Concatenate using a deliberately written manifest:

```python
from pathlib import Path
names = Path('parts-order.txt').read_text().splitlines()
assert names and len(names) == len(set(names))
with open('out/reassembled.bin', 'xb') as dst:
    for name in names:
        p = Path('out/http') / name
        assert p.resolve().is_relative_to(Path('out/http').resolve())
        dst.write(p.read_bytes())
```

Validate the resulting archive with an approved archive tool. Uniform-size pieces and one short piece suggest splitting but do not prove order.

## TLS and RDP: use the right key material

**Windows TShark**, supplied NSS keylog file:

```powershell
& $tshark -n -r capture.pcapng -o 'tls.keylog_file:session.keys' -Y http
& $tshark -n -r capture.pcapng -o 'tls.keylog_file:session.keys' `
  --export-objects http,out/decrypted-http
```

In Wireshark: **Preferences → Protocols → TLS → (Pre)-Master-Secret log filename**. TLS 1.2 keylogs often use `CLIENT_RANDOM`; TLS 1.3 uses traffic-secret labels. Confirm the keylog's client random matches the captured handshake. Capturing only application data can make decryption impossible even with useful secrets.

A server RSA private key works only for supported **RSA key exchange**, not ECDHE/DHE or TLS 1.3. For a challenge-provided PFX, **WSL OpenSSL**, Windows row 31:

```bash
openssl pkcs12 -in challenge.pfx -nocerts -nodes -out out/server-key.pem
openssl x509 -in certificate.der -inform DER -noout -text
```

Set the RSA-key list's IP, port, application protocol, and PEM path in Wireshark. For RDP, the application may be `tpkt`. A PFX appearing in a capture does not automatically make all RDP sessions decryptable.

For a core-dump secret search, locate handshake randoms or session IDs in the dump, then use the **exact TLS-library version's structure layout** to identify candidate secret buffers. The historical rule “48 bytes immediately before the session ID” is not portable. Validate a candidate by successfully decrypting/authenticating records, not by its length. Use locally supported crypto methods for weak-key challenges; do not send moduli or captures to public analysis services.

## Authentication evidence: NTLM, SMB, RADIUS, SNTP

**Windows TShark:**

```powershell
& $tshark -n -r capture.pcapng -Y ntlmssp -V > out\ntlm-details.txt
& $tshark -n -r capture.pcapng -Y 'smb2 || dcerpc || ntp || radius' -V > out\auth-details.txt
```

For NTLMv2, pair the server challenge from Type 2 with Type 3's username, domain, 16-byte proof, and remaining response blob **in the same authentication exchange**. The offline hashcat format is:

```text
USER::DOMAIN:SERVER_CHALLENGE_HEX:NTPROOF_HEX:BLOB_HEX
```

**Kali hashcat**, row 66:

```bash
hashcat -m 5600 ntlmv2.txt challenge-words.txt
hashcat -m 5600 ntlmv2.txt --show
```

Passwords alone are not the final SMB decryption key. NTLM negotiation flags determine whether the exported session key is encrypted; SMB dialect determines KDF labels and context. SMB 3.1.1 uses preauthentication integrity state and direction-specific keys. Prefer Wireshark's SMB2 protocol key settings and verify the negotiated dialect. Do not uppercase the domain automatically: NTLMv2's identity is `UpperCase(user) + domain` with the actual domain representation.

Repeated LSARPC SID lookups with sequential RIDs reveal account enumeration. Record the queried SID and returned account name; avoid assuming Guest access always works. A 68-byte MS-SNTP response can contain 48 bytes of NTP header, a 4-byte little-endian RID, and a 16-byte digest. Export the **server responses**, then parse:

```powershell
& $tshark -n -r capture.pcapng -Y 'ntp && ip.src == 192.0.2.20' `
  -T fields -e udp.payload | Set-Content -Encoding ascii out\sntp.hex
```

**WSL Python:**

```python
from pathlib import Path
records = set()
for line in Path('out/sntp.hex').read_text().splitlines():
    d = bytes.fromhex(line.replace(':', '').strip())
    if len(d) != 68:
        continue
    rid = int.from_bytes(d[48:52], 'little')
    records.add(f'{rid}:$sntp-ms${d[52:].hex()}${d[:48].hex()}')
Path('out/sntp.hashes').write_text('\n'.join(sorted(records)) + '\n')
```

**Kali:** `hashcat -m 31300 --username out/sntp.hashes challenge-words.txt`. Verify the installed mode's example format first. Real machine-account passwords are often long random values; recovery is not guaranteed.

For RADIUS, locate the installed John jumbo `radius2john` extractor (Kali row 80), inspect its help, and use its output with John. Apply a recovered shared secret in Wireshark's RADIUS preferences; verify corresponding requests/responses. Do not treat every UDP/1812 packet as a usable crackable exchange.

## DNS and ICMP covert channels

**Windows PowerShell:** export one direction and keep packet order.

```powershell
& $tshark -n -r capture.pcapng -Y 'dns.flags.response == 0' `
  -T fields -e frame.number -e dns.qry.name |
  Set-Content -Encoding ascii out\dns.tsv
& $tshark -n -r capture.pcapng -Y 'icmp.type == 8' `
  -T fields -e frame.number -e icmp.ident -e icmp.seq -e data.data |
  Set-Content -Encoding ascii out\icmp.tsv
```

For DNS, test hex/base32 labels, label initials/final characters, TXT records, and bytes after the parsed question. Do not include both queries and their echoed questions in responses. Retries need sequence-aware deduplication: repeated content can also be legitimate data.

This **WSL** script decodes hex labels under one explicitly chosen suffix. It preserves frame numbers for later reordering rather than guessing a protocol header length:

```python
from pathlib import Path
suffix = '.tunnel.challenge.test'  # replace with observed carrier suffix
with open('out/dns-chunks.tsv', 'w') as out:
    for line in Path('out/dns.tsv').read_text().splitlines():
        fields = line.split('\t')
        if len(fields) != 2:
            continue
        frame, name = fields
        name = name.rstrip('.')
        if not name.lower().endswith(suffix.lower()):
            continue
        encoded = name[:-len(suffix)].replace('.', '')
        try:
            payload = bytes.fromhex(encoded)
        except ValueError:
            continue
        out.write(f'{frame}\t{payload.hex()}\t{payload[:40]!r}\n')
```

For dnscat-like traffic, parse message type, session, sequence, and acknowledgement fields from the actual framing. Header length varies by message type; a universal “strip nine bytes” rule corrupts some traffic. Reassemble each session/direction by sequence, reject inconsistent overlaps, then identify the payload format.

For trailing DNS bits, walk DNS labels (including compression pointers) and the question's QTYPE/QCLASS. A raw `len(qname)` calculation is not a general wire-length parser. Compare the dissector's byte selection with the UDP payload to find the unexplained tail.

For ICMP, test payload lengths, identifier/sequence values, byte rotations, and timing separately. IPv4 payload length is total IP length minus actual IP-header length minus the eight-byte echo header; do not use Ethernet frame length. Exclude replies when requests alone carry data. Preserve leading zero bytes when packing bits.

## Timing and flag channels

**Windows**, isolate the suspected flow/interface before exporting:

```powershell
& $tshark -n -r capture.pcapng -Y 'frame.interface_id == 2 && icmp.type == 8' `
  -T fields -e frame.time_epoch | Set-Content -Encoding ascii out\times.txt
& $tshark -n -r capture.pcapng -Y 'tcp.dstport == 5748' `
  -T fields -e tcp.flags | Set-Content -Encoding ascii out\flags.txt
```

**WSL**, save as `timing.py`; the threshold is a measured hypothesis in seconds:

```python
from pathlib import Path
from collections import Counter
times = [float(x) for x in Path('out/times.txt').read_text().split()]
deltas = [b-a for a, b in zip(times, times[1:])]
print('gap distribution:', Counter(round(d, 3) for d in deltas))
threshold = 0.05  # choose between observed modes
bits = [int(d > threshold) for d in deltas]
for invert in (0, 1):
    for alignment in range(8):
        b = bits[alignment:]
        result = bytes(sum((v ^ invert) << (7-j) for j, v in enumerate(b[i:i+8]))
                       for i in range(0, len(b)-7, 8))
        print(invert, alignment, repr(result[:200]))
```

Two timing modes can arise naturally; require structured decoded output and context. Do not insert a guessed leading bit merely to force a flag. For echo reply delays, pair by source/destination, identifier, sequence, and nearby time; sequence alone can collide after wraps or across hosts.

TCP's six low flag bits can index Base64 when otherwise nonsensical flag combinations repeat:

```python
from pathlib import Path
import base64
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
encoded = ''.join(alphabet[int(x, 16) & 63]
                  for x in Path('out/flags.txt').read_text().split())
print(base64.b64decode(encoded + '=' * (-len(encoded) % 4), validate=True))
```

Also inspect BCD: both nibbles must be decimal digits. Pair or triple the resulting digits according to explicit framing; greedy two/three-digit ASCII decoding can produce ambiguous results.

## Wi-Fi, voice, and secondary protocols

**Kali**, supplied wireless capture only:

```bash
aircrack-ng capture.cap
aircrack-ng -a 2 -w challenge-words.txt capture.cap
airdecap-ng -p 'RECOVERED_PASSPHRASE' -e 'EXACT_SSID' capture.cap
```

Use the tool's reported output filename. WPA/WPA2-PSK recovery needs a usable handshake/PMKID and matching ESSID; it is not a generic WPA3 decoder. WEP recovery needs sufficient IV material. Inspect key changes per time interval before concluding a recovered password is wrong. No deauthentication or live handshake collection is needed for a supplied capture.

For RTP, use Wireshark **Telephony → RTP → RTP Streams**, inspect codec and sequence gaps, then export audio. rtptools is listed on Kali row 129, but rtppayload bytes are not automatically WAV PCM. For TFTP, reassemble by block number and suppress retransmitted blocks; only apply `CRLF→LF` and `CRNUL→CR` if the negotiated transfer mode was `netascii`.

For USB audio, isolate one isochronous endpoint/direction and export `usb.iso.data` if available in the installed dissector. Use descriptor-declared channels, sample width, signedness, and rate when importing raw PCM in approved Kali Audacity (row 17). Remove USB framing, not arbitrary leading bytes.

For 5G NAS/RLC/PDCP/MAC records or SAP traffic, inspect **Analyze → Enabled Protocols** and **Decode As** for installed dissectors. Capture encapsulation and direction affect parsing. SMS user-data headers can contain animation or ringtone data, but those bytes need the declared data-coding scheme. The historical SAP-specific external tools are not assumed approved.

## USB keyboard reports

Use the HID **report descriptor** to confirm layout. Standard boot keyboards use an eight-byte report; other devices use report IDs, NKRO bitmaps, or custom structures. **Windows:**

```powershell
& $tshark -n -r capture.pcapng -Y 'usb.transfer_type == 1 && usb.capdata' `
  -T fields -e usb.capdata | Set-Content -Encoding ascii out\hid.hex
```

Restrict this further to the observed device and input endpoint. The following **WSL** decoder handles a standard US boot keyboard, fresh key presses, shift, Caps Lock, Enter, and Backspace:

```python
from pathlib import Path
normal = dict(zip(range(4, 30), 'abcdefghijklmnopqrstuvwxyz'))
normal.update(dict(zip(range(30, 40), '1234567890')))
normal.update({40:'\n',43:'\t',44:' ',45:'-',46:'=',47:'[',48:']',
               49:'\\',51:';',52:"'",53:'`',54:',',55:'.',56:'/'})
shifted = dict(zip('1234567890-=[]\\;\'`,./', '!@#$%^&*()_+{}|:"~<>?'))
previous, caps, output = set(), False, []
for line in Path('out/hid.hex').read_text().splitlines():
    raw = bytes.fromhex(line.replace(':','').strip())
    if len(raw) != 8:
        continue
    keys = set(raw[2:]) - {0}
    if keys & {1,2,3}:  # HID error/rollover reports
        previous = set()
        continue
    for key in raw[2:]:
        if not key or key in previous:
            continue
        if key == 57:
            caps = not caps
        elif key == 42:
            if output: output.pop()
        elif key in normal:
            ch = normal[key]
            shift = bool(raw[0] & 0x22)
            if ch.isalpha(): ch = ch.upper() if caps ^ shift else ch
            elif shift: ch = shifted.get(ch, ch)
            output.append(ch)
        else:
            output.append(f'<KEY:{key:02x}>')
    previous = keys
print(''.join(output))
```

For arrows (`4f` right, `50` left, `51` down, `52` up), maintain a line/column cursor and insert into the current text buffer. This decoder deliberately prints them as markers rather than inventing an editor's behavior. Held-key repeats cannot always be inferred from duplicate state reports. Multiple simultaneous keys may be stenographic chords; preserve the whole set and use a supplied dictionary, not an unapproved external application.

Linux `input_event` dumps use a different keycode set. A common 64-bit little-endian record is `struct.unpack('<qqHHi', record)` over 24 bytes: seconds, microseconds, type, code, value. A 32-bit timeval layout can be 16 bytes (`<iiHHi`). Validate timestamp ranges and record alignment before choosing. For `type==1`, value 1 is press, 0 release, and 2 repeat; map codes using the matching supplied/Linux input-event header, not the USB HID map.

## Mouse, LEDs, Bluetooth, and MIDI

Mouse reports need signed delta fields from the descriptor. Accumulate motion even while the button is up, but draw a segment only while the pen/button is down. Keep custom drawing modes separate; connecting separate strokes creates false letters. Render with a WSL Python SVG writer or Pillow (Windows row 14).

For keyboard LEDs, isolate host-to-device `SET_REPORT`, decode the appropriate output bit, and measure actual on/off transitions. Standard Morse uses approximate 1-unit dots, 3-unit dashes/letter gaps, and 7-unit word gaps. Calibrate from the observed duration distribution; raw offset 30 and a fixed 300 ms threshold are capture-specific, not USB standards.

Bluetooth RFCOMM sits above L2CAP. Export dissector payloads for one channel; do not strip a fixed eight-byte header from every packet. Reassemble application frames from their own lengths and group/order fields. For USB MIDI, strip the USB-MIDI event packet header, then parse MIDI messages: Note On with velocity zero is Note Off. On a verified Launchpad mapping, `row=note//16`, `column=note%16`; save the accumulated grid before clearing at a separator. Different models use different note layouts.

For console framebuffer transfers, recover all blocks by their destination memory offsets before rendering. GBA native color is commonly 15-bit BGR555 in 16-bit words, while adapters may convert it to RGB565: determine the format from the actual protocol. Dimensions and a visually plausible image alone do not validate byte order.

## UART and synchronous logic captures

Use exported CSV or challenge-documented raw samples. A `.sal` file's internal format is not the same as Saleae's export format; an archive signature does not make a guessed transition parser correct. No Saleae/PulseView installation is assumed by this workbook.

For `uart.csv` containing a header `time,level` and samples at known times, this **WSL** decoder samples 8N1 UART in the middle of each bit. Set `baud` and invert polarity if measurements require it:

```python
import csv, bisect
from pathlib import Path
with open('uart.csv', newline='') as f:
    rows = list(csv.DictReader(f))
t = [float(r['time']) for r in rows]
level = [int(r['level']) for r in rows]
baud = 9600
period = 1 / baud
def sample(when):
    k = bisect.bisect_right(t, when) - 1
    if k < 0 or when > t[-1]: raise EOFError('capture ends mid-byte')
    return level[k]
out, next_start = bytearray(), -1.0
for i in range(1, len(t)):
    if t[i] < next_start or (level[i-1], level[i]) != (1,0): continue
    start = t[i]
    try:
        if sample(start + .5*period) != 0: continue
        bits = [sample(start + (1.5+j)*period) for j in range(8)]
        if sample(start + 9.5*period) != 1: continue
    except EOFError:
        break
    out.append(sum(b << j for j,b in enumerate(bits)))
    next_start = start + 9.5*period  # stop-bit centre; tolerate timestamp rounding
Path('out/uart.bin').write_bytes(out)
print(repr(out))
```

Expected result: stable bytes across nearby baud hypotheses and valid stop bits. If output drifts, use fractional sample times, check idle polarity/parity/stop count, and ensure sample rate exceeds baud sufficiently. For WAV, 8-bit PCM is unsigned centered at 128; 16-bit PCM is signed little-endian. Do not round samples-per-bit to an integer prematurely.

For I²C, SDA falling while SCL remains high is START; SDA rising while SCL remains high is STOP. Sample SDA on SCL rising edges, collect eight MSB-first data bits, then retain the ninth ACK/NACK bit separately. Decode address/RW first; repeated START is a new address phase. For SPI or parallel RGB CSVs, determine clock edge/polarity from a known preamble and sample each data lane at that edge.

For VGA, use HSync/VSync transitions to locate active rows and frames; 800×525 total/640×480 active is only one mode. For HDMI TMDS, separate control symbols before decoding video symbols. The inverse data chain uses **adjacent encoded bits**, not the previously recovered source bit:

```python
def tmds_video(symbol):
    assert 0 <= symbol < 1024
    q = symbol & 255
    if symbol & 512: q ^= 255
    xor_mode = bool(symbol & 256)
    value = q & 1
    for bit in range(1, 8):
        v = ((q >> bit) ^ (q >> (bit-1))) & 1
        if not xor_mode: v ^= 1
        value |= v << bit
    return value
```

For DisplayPort, first establish lane alignment and valid 8b/10b control symbols/running disparity, then apply the specified scrambler bit order and reset behavior. Transport-unit size and stuffing are negotiated; do not assume “60 data bytes plus four overhead” for every stream. A supplied encoder is the most useful reference for a custom signal challenge.

## Corruption and compression troubleshooting

For a classic PCAP, inspect its 24-byte global header, endian/nanosecond magic, link type, and every record's included/original length. For pcapng, use block lengths, section endian marker, and interface link types; it has a different format. Change only fields supported by surrounding evidence, then reopen the copy. The source's `pcapfix` installer is not an approved default.

IP/TCP checksums can constrain missing bytes, but capture offload may cause apparently bad checksums in genuine packets. Validate IPv4 header checksum over its actual IHL; TCP includes its pseudoheader and payload. Two missing bytes can have many checksum-equivalent solutions, so use application framing too.

Brotli has no universal fixed file magic. An anomalous repeated compressed block may mark a useful seam, but decoding at an arbitrary middle offset usually fails because decompression state depends on preceding bytes. Decode from a valid stream boundary with output limits; inspect the supplying program if the expansion is huge. Do not decompress a bomb unboundedly to RAM or disk.

Source material adapted: `ctf-forensics/network.md`, `network-advanced.md`, `peripheral-capture.md`, `signals-and-hardware.md`, plus network portions of `linux-forensics.md` and `SKILL.md`. PDF overlap is covered in the steganography chapter. Active interception, third-party vendor lookups, public decryption services, and unsupported installers were removed.
