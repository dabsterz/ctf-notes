# Contest quick reference

**Pick one task. Run its command. Check the result.** Use the [tool chooser](TOOL-CHOOSER.md) when deciding between programs; open a full chapter only when you need more depth.

**Run:** replace example filenames and use the named machine. Open a terminal in the extracted guide folder so `recipes/` is beside you. [Terminal and download setup](COMPETITION.md#open-this-guide).

**Competition:** notes and prepared scripts are allowed. Flags typically use `CSG_FLAG{...}`; submit the full value to CTFd. [Access, limits and rules](COMPETITION.md).

| What you have | Jump straight to |
| --- | --- |
| URL, cookie or request | [Web paths](#web-paths), [JWT role](#jwt-role) |
| Password hashes or encrypted archive | [Hash cracking](#hash-cracking), [tool choice](TOOL-CHOOSER.md#passwords-and-hashes) |
| PNG, tar or Windows events | [PNG trailer](#png-trailer), [duplicate tar files](#duplicate-tar-files), [process event](#process-event) |
| Packet capture | [Network conversation](#network-conversation) |
| RSA numbers or Base64 text | [RSA](#rsa), [decode layers](#decode-layers) |
| Binary or byte checker | [Static reversing](#static-reversing), [XOR and rotation](#xor-and-rotation), [small VM](#small-vm) |
| Crash bytes | [Crash offset](#crash-offset) |
| Suspicious script, image clue, restricted interpreter | [Malware](#malware), [OSINT](#osint), [miscellaneous](#miscellaneous) |

## Web paths

**Use when:** you have a challenge URL and want hidden routes. **Kali.** Use a short list based on observed links/source; replace these example names. Discovery words are different from password guesses.

```bash
curl -i 'http://challenge.example/a-name-that-should-not-exist'
printf '%s\n' profile export status > words.txt
ffuf -u 'http://challenge.example/FUZZ' -w words.txt -ac -t 1 -rate 1 -timeout 10 -maxtime 30
```

**Look for:** a response that differs from the fake-path baseline. Open a candidate with `curl -i 'http://challenge.example/candidate'`. A 200 alone can be a custom error page. If results disappear, inspect the baseline and retry without `-ac`; automatic filtering can hide valid pages. [More web recipes](chapters/02-web-exploitation.md).

## JWT role

**Use when:** evidence suggests a JWT signature is not checked. Changing a payload does not forge its signature. **WSL Python** edits the token; **Kali curl** or **WSL Burp Repeater** sends it.

Save only the captured token in `token.txt`. The default edit is the JSON claim `"role":"admin"`:

```bash
python3 recipes/jwt_claim.py token.txt
```

**Kali:** keep the two token files on Kali for these requests; replace `/flag` with the observed endpoint. Do not assume WSL files are on the remote machine.

```bash
curl -i -H "Authorization: Bearer $(cat token.txt)" 'http://challenge.example/flag'
curl -i -H "Authorization: Bearer $(cat edited-token.txt)" 'http://challenge.example/flag'
```

**WSL GUI alternative:** Burp → captured request → Send to Repeater → replace its Bearer token with `edited-token.txt` → Send. If the app uses a cookie, edit that cookie instead.

**Success:** the server grants the requested access and returns the real answer. **Rejected:** signature verification may be working; inspect the actual auth flow instead of repeatedly changing role names. [JWT detail](chapters/02-web-exploitation.md#5-jwt-and-jwe-inspect-before-changing).

## Hash cracking

**Use when:** you have an offline hash and know its algorithm. **Kali.** This example is **raw MD5 only**, not every 32-character string.

```bash
john --format=raw-md5 --wordlist=words.txt hashes.txt
john --show --format=raw-md5 hashes.txt
```

**Success:** `--show` prints the recovered password. Verify it against the challenge. **No hashes loaded:** check file syntax and the format; do not assume the wordlist is the problem. **No password found:** the list may miss it. Use [the comparison table](TOOL-CHOOSER.md#passwords-and-hashes) for hashcat, archive extractors and online login guessing.

## PNG trailer

**Use when:** a PNG may have a second file appended. **WSL Python.**

```bash
python3 recipes/png_tail.py carrier.png
```

**Look for:** nonzero trailing bytes and a recognizable header/text. The script previews text and reports CRCs. If unclear, inspect with `xxd -l 128 png-trailer.bin` or `strings -a png-trailer.bin`. Zero bytes means try metadata or pixel channels; a bad CRC means inspect structure before trusting it. This does not test pixel steganography. [Other image tools](TOOL-CHOOSER.md#steganography-and-audio).

## Duplicate tar files

**Use when:** a tar archive contains repeated filenames or a previous version matters. **WSL Python.**

```bash
python3 recipes/tar_keep.py evidence.tar --out tar-parts
```

**Look for:** two printed entries with the same original name but different numbered output files. `tar-parts/manifest.jsonl` maps names to saved files; previews show the first 120 bytes. Inspect a chosen member:

```bash
strings -a tar-parts/000000.bin
```

**If it stops:** read the error. Existing output directory? Choose a new `--out` name. Extraction budget exceeded? Earlier members are retained; list the archive before extracting more. [Disk and archive workflows](chapters/03-forensics.md).

## Process event

**Use when:** asked what program ran and when. **Windows PowerShell, JSON input:**

```powershell
Get-Content -Raw events.json | ConvertFrom-Json | Format-List
```

**EVTX input instead:**

```powershell
Get-WinEvent -FilterHashtable @{Path='.\Security.evtx'; Id=4688} | ForEach-Object {
  [xml]$eventXml = $_.ToXml()
  $fields = @{}
  $eventXml.Event.EventData.Data | ForEach-Object { $fields[$_.Name] = $_.'#text' }
  [pscustomobject]@{
    UTC = $eventXml.Event.System.TimeCreated.SystemTime
    Program = $fields['NewProcessName']
    Command = $fields['CommandLine']
  }
} | Format-List
```

| Field in the supplied record | Read it as |
| --- | --- |
| Security provider, event 4688 | A process started; not a file-creation event |
| `SystemTime` (often exported as `TimeCreated`) ending in `Z` | UTC timestamp; preserve it before converting time zones |
| `NewProcessName` | Executable path |
| `CommandLine` (some exports rename it `ProcessCommandLine`) | Arguments, if command-line auditing captured them |

For JSON in **WSL**, use `jq . events.json`. An export without a timezone needs its settings checked. A blank command line does not prove no arguments. This event alone does not prove malicious intent, successful completion or payload effects. [Microsoft's event definition](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4688).

## Network conversation

**Windows Wireshark:** File → Open capture → Statistics → Conversations → TCP. Right-click the relevant conversation → Apply as Filter → Selected → A ↔ B. Close the dialog, then right-click a displayed packet → Follow → TCP Stream. Search the stream for the clue; change the display to Raw before saving binary data.

**Windows PowerShell with TShark installed at the workbook's Windows location:**

```powershell
& 'C:\Program Files\Wireshark\tshark.exe' -r .\capture.pcapng -q -z conv,tcp
& 'C:\Program Files\Wireshark\tshark.exe' -r .\capture.pcapng -Y 'http.request' -T fields -e tcp.stream -e http.host -e http.request.uri
```

**Look for:** host/path and stream number associated with the clue. No HTTP output can mean TLS, another protocol, or the wrong capture; it does not mean no traffic. [Recover an HTTP download](chapters/04-network.md#http-credentials-and-files) · [Network tools](TOOL-CHOOSER.md#network).

## RSA

**Use when:** raw RSA supplies `n`, `e`, `c`, and you know the prime factors or suspect they are close. **WSL Python.** Save these values in `rsa.json`; decimal numbers or quoted `0x...` strings are accepted. Add `p` and `q` if known.

```json
{"n": 3233, "e": 17, "c": 2790, "p": 61, "q": 53}
```

```bash
python3 recipes/rsa.py rsa.json
```

**Success:** `re-encryption: OK`, candidate bytes and `rsa-plain.bin`; this tiny example yields `b'A'`. Without `p,q`, the script tries at most 100,000 Fermat steps. **No close factors:** switch to another RSA attack, not a longer blind wait. Padding remains; leading zero bytes need a known `length`. Factors must be distinct primes. [Other RSA routes](chapters/07-cryptography.md).

## Decode layers

**Use when:** text looks like Base64, possibly wrapping zlib/gzip. **WSL Python.**

```bash
python3 recipes/layers.py message.txt --out decoded
```

**Look for:** `layer1.bin` plus `layer2.bin` when a compression header is recognized, with a preview printed. The original is preserved. Any bytes after the compressed stream go to `trailing.bin`. **Strict Base64 error:** if the line is `payload=VALUE`, save only VALUE in a new text file, keeping final `=` padding; rerun with that filename. Otherwise check for hex or URL-safe Base64. **Existing directory:** choose a fresh output name. [Other encodings](chapters/11-miscellaneous.md).

## Static reversing

**Kali radare2:** `r2 -A challenge.bin`, then type these inside r2:

```text
iz
afl
s main
pdf
q
```

**Look for:** strings, input-reading calls and the comparison deciding success. `main` may be missing in stripped files; select a function address from `afl`, then `pdf @ 0xADDRESS`. **Windows/WSL alternative:** Ghidra → New Project → Import File → open in CodeBrowser → Analyze → Search → for Strings → references to the success/failure string. This is static inspection; no target execution is required. [Reverse tool choices](TOOL-CHOOSER.md#reverse-engineering).

## XOR and rotation

**Use only for:** `stored[i] = ROL8(input[i] XOR repeated_key[i], rotation)`. Undo rotation, then XOR. **WSL Python.** Put the recovered constants in `checker.json`:

```json
{"key_hex":"6b6579", "rotation":3, "expected":[81,57,209]}
```

```bash
python3 recipes/transform.py checker.json
```

**Success:** `forward check: OK` and recovered bytes (`b'ABC'` in this example). The script verifies every byte against the stored table. **Different transform/order:** change the model first; this is not a universal decryptor. [Inversion rules](chapters/06-reverse-engineering.md#8-write-down-the-transform-before-solving-it).

## Small VM

**Use when:** you have already recovered a straight-line VM operating on one input byte. **WSL Python.** Save decoded instructions in `vm.json`:

```json
{"program":[["LOAD_INPUT"],["XOR",35],["ADD",7],["CMP",111],["HALT"]]}
```

```bash
python3 recipes/vm_byte.py vm.json
```

**Success:** decimal `75`, hex `0x4b`, byte `b'K'`; every comparison matches. The helper checks all 256 bytes with fresh state. Supported operations: LOAD_INPUT, XOR, ADD, ROL, CMP, HALT; arithmetic wraps at 8 bits. **No match or unsupported opcode:** correct the decoded semantics; branches, memory and multiple inputs need a different model. [Full VM workflow](chapters/06-reverse-engineering.md#10-custom-vms-and-emulation).

## Crash offset

**Use when:** you generated input with this exact pattern helper and recovered four crash bytes in memory order. **WSL Python.**

```bash
python3 recipes/pattern.py --length 512
python3 recipes/pattern.py --find 61616763 --sent pattern.bin
```

The first command writes `pattern.bin`; supply that file through the vulnerable program's actual input path. The second example returns **173** and verifies the bytes lie inside that file. Your crash bytes will differ. **`-1` or not verified:** wrong byte order, wrong generator, or bytes outside the sent input. An offset alone is not an exploit. [Pwn tools](TOOL-CHOOSER.md#binary-exploitation).

## Malware

**Start with static inspection. WSL:**

```bash
strings -a suspect.bin
xxd -l 64 suspect.bin
```

**Look for:** format, URLs, imports or encoded text. Strings are clues, not proof of execution. For Base64 scripts use [decode layers](#decode-layers); for macros use [oletools](TOOL-CHOOSER.md#malware). If strings are empty, check packing and encoding before considering an isolated runtime. [Detailed malware workflows](chapters/09-malware.md).

## OSINT

**Start with the supplied file. WSL:**

```bash
exiftool -a -G1 -s clue.jpg
```

**Look for:** GPS, timestamp offsets and device/software tags. Check a second clue such as signs, shadows or visible landmarks; metadata can be edited. No GPS is a reason to examine the picture, not to upload it. [OSINT tools](TOOL-CHOOSER.md#osint).

## Miscellaneous

**Encoded text?** [Decode layers](#decode-layers). **Audio?** [Audio tools](TOOL-CHOOSER.md#steganography-and-audio). **JSON? WSL:** `jq . challenge.json`.

For a restricted interpreter, first write down the allowed characters, available objects, input limit and intended output. Read supplied source before trying payloads: a Python jail, Bash restriction and arithmetic puzzle need different approaches. [Choose a matching miscellaneous recipe](chapters/11-miscellaneous.md).

## Before the event

Read [Competition setup](COMPETITION.md) once. During solving, use one matching card; open a full chapter only when it helps.
