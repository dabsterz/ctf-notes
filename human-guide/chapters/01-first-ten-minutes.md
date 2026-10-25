# First ten minutes: get evidence before guessing

Your aim is to turn an unfamiliar challenge into one precise question. “Something is hidden in this file” is too broad. “There are ZIP bytes after the PNG end marker” gives you a next action.

## 1. Record the question and protect your starting point

Write down the exact task, flag format, target address/port, supplied files, and any attempt limit. Keep one untouched copy and work on another. You do not need to install a case-management application.

In **Kali or WSL**, from the directory containing the attachment:

```bash
mkdir -p case/original case/work case/notes
cp -- challenge.bin case/original/
cp -- challenge.bin case/work/
cd case/work
python3 -c "import hashlib,pathlib; p=pathlib.Path('challenge.bin'); print(hashlib.sha256(p.read_bytes()).hexdigest(), p.name)"
```

Replace `challenge.bin` before running. `mkdir -p` permits an existing directory; choose a new case name for each challenge so you do not overwrite another case. The hash lets you check later whether a tool changed the input.

On **Windows**, use the same folder discipline in Explorer. If PowerShell is available as part of the provided environment, the equivalent native hashing operation is:

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath '.\challenge.bin'
```

For very large images, stream the hash instead of loading the whole file into RAM. Save as `hash_file.py` and run `python3 hash_file.py challenge.bin` in WSL or Kali:

```python
import hashlib
import sys
from pathlib import Path

path = Path(sys.argv[1])
digest = hashlib.sha256()
with path.open('rb') as stream:
    for chunk in iter(lambda: stream.read(1024 * 1024), b''):
        digest.update(chunk)
print(digest.hexdigest(), path.name)
```

## 2. Identify the bytes, not just the extension

**Kali** (`file` is Kali row 49):

```bash
file -- challenge.bin
```

**WSL** (`xxd` and `strings` are Windows rows 35 and 18):

```bash
xxd -l 128 challenge.bin
strings -a -n 6 challenge.bin > strings.txt
```

Read `strings.txt` in an approved editor. Search for the challenge's actual flag prefix, filenames, paths, function names, and error messages. A flag-shaped string is a lead, not proof: repositories and captures can contain decoys or old runs. Do not truncate the only copy of useful output with `head` and forget the rest.

This **Python standard-library** check works without `file` or `xxd`:

```bash
python3 -c "from pathlib import Path; p=Path('challenge.bin'); f=p.open('rb'); b=f.read(128); print('bytes:',p.stat().st_size); print('hex:',b.hex(' ')); print('raw:',repr(b))"
```

| Leading bytes | Likely container | Next question |
| --- | --- | --- |
| `7f 45 4c 46` | ELF executable | Architecture? Input-checking logic or corruption bug? |
| `4d 5a` | DOS/Windows executable family | Is a PE header present? Native or .NET? |
| `50 4b 03 04` | ZIP family | Ordinary ZIP, Office file, APK, or another ZIP-based container? |
| `89 50 4e 47 0d 0a 1a 0a` | PNG image | Valid chunks? Metadata? Appended data? |
| `ff d8 ff` | JPEG image | Metadata, embedding, or trailing bytes? |
| `25 50 44 46` | PDF | Text, attachments, objects, or active content? |
| `53 51 4c 69 74 65` | SQLite | Which tables, and are WAL files supplied? |
| `0a 0d 0d 0a` | PCAPNG section | Which hosts, protocols, and conversations? |

A header match is a hint, not full validation. A ZIP header can occur inside another file. A text-looking file may hold Base64, hex, JSON, or source code.

## 3. Inspect containers before extraction

**Kali** has 7-Zip (`C9`) and unzip (`C155`):

```bash
7z l challenge.zip
7z x challenge.zip -oextracted
```

Read the listing first. Extract into a new working directory, watch expanded size, and avoid executing recovered programs. Password-protected archives need an evidence-backed password or a local cracking workflow, not random format conversion.

For a ZIP file in **WSL**, Python can list members without extraction:

```bash
python3 -m zipfile -l challenge.zip
```

Notice path traversal names, duplicate filenames, timestamps, comments, and suspicious size ratios. If the archive is nested repeatedly, identify the compression at each layer and keep intermediate outputs rather than deleting your trail.

## 4. Read source before attacking a service

If source is supplied, locate the input, transformation, and success check. Do not start by installing more tools. On **Kali**, search a source directory with ripgrep (`C126`):

```bash
rg -n -i 'flag|secret|password|verify|compare|eval|exec|pickle|subprocess' source/
```

On **Windows**, use Notepad++ **Search → Find in Files** on the source directory. In a web challenge, inspect HTML and referenced JavaScript as well as backend source. Follow the actual data flow; a keyword match alone does not prove a vulnerability.

## 5. Make one baseline connection

Only use the exact host and ports provided for the exercise. A URL such as `http://challenge.example:8000` below is a placeholder.

**Kali** (`curl`, row 30):

```bash
TARGET='http://challenge.example:8000'
curl --max-time 15 -sS -D headers.txt -o body.html "$TARGET/"
```

Inspect `headers.txt` and `body.html`. Status codes, redirects, content type, cookies, and linked scripts often tell you more than a scanner. A timeout may be a VPN or service problem; it does not prove an exploit worked.

**WSL Python** alternative, saving response body and showing status/headers:

```python
from urllib.request import urlopen
from pathlib import Path

target = 'http://challenge.example:8000/'  # Replace with the supplied target.
with urlopen(target, timeout=15) as response:
    print(response.status)
    print(response.headers)
    Path('body.html').write_bytes(response.read())
```

This follows redirects by default. If redirects are part of your hypothesis, use Burp or the web chapter's more explicit request workflow instead. An HTTP error raises an exception here; use that status as evidence rather than suppressing it.

For a plain TCP service on **Kali**, use Ncat (part of Nmap, row 101):

```bash
ncat --idle-timeout 15s challenge.example 31337
```

Read its banner and prompts. Do not paste a binary payload into a text prompt until you know its framing. TLS services may need Ncat's `--ssl`; use that only when the challenge specifies TLS.

## 6. Keep a hypothesis log

Use a small table in `notes.md`:

| Observation | Hypothesis | Smallest test | Result and next step |
| --- | --- | --- | --- |
| A cookie has three dot-separated segments | It may be a JWT | Decode the first two segments locally | Read `alg`, claims, expiry; decoding is not signature verification. |
| A PNG ends before the physical file does | A second artifact may be appended | Inspect the bytes after IEND | Extract from a confirmed boundary, then identify again. |
| Two RSA moduli share a factor | Bad key generation reused a prime | Compute `gcd(n1, n2)` | A nontrivial factor gives a direct private-key calculation. |

Change one variable at a time. Save the baseline so you can compare. Do not treat a changed response length as proof without checking the actual body.

## 7. Know when to pivot

After three actions that produce no new evidence, stop and state the blocker. Is the file format wrong? Are you on the wrong machine? Is a key, symbol table, protocol detail, or dependency missing? A human teammate can help faster if you give them those facts.

Suggested timeboxes, not event rules: spend about five minutes on triage and ten to fifteen minutes on the first plausible path. Continue when you have measurable progress. Park a challenge when two reasonable approaches add no evidence and easier work is available.

Keep this handoff note:

```text
Challenge:
Exact question / flag format:
Files and hashes:
Permitted target:
Verified facts:
Tests tried and what they ruled out:
Working primitive:
Exact blocker:
Best next test:
Relevant output files:
```

This replaces the source's AI model-routing ladder with a practical team handoff. No model choice or token budget belongs in the human workflow.

## 8. Verify before submitting

Reproduce the candidate from the original input. Check the required prefix, encoding, capitalization, whitespace, and question wording. Keep its derivation. If attempts are limited, get a teammate to check the arithmetic or extraction independently rather than submitting cosmetic variations.

For a candidate in `candidate.txt`, show hidden characters before submission:

```bash
python3 -c "from pathlib import Path; b=Path('candidate.txt').read_bytes(); print(repr(b)); print('length:',len(b))"
```

Submit through the organizer's normal interface and record its verdict. A successful local script is not the same as an accepted answer. Avoid publishing event answers or artifacts; follow organizer confidentiality requirements.

## 9. Leave a short reproducible solve note

```text
Title / category:
Question:
Key observation:
Steps and exact commands:
Input file hash:
Relevant tool and version:
Recovered answer:
How it was checked:
Platform verdict:
```

One clear solve path is enough. Include failed ideas only when they prevent a teammate repeating a costly mistake.

Adapted from `solve-challenge/SKILL.md`, `solve-challenge/difficulty-routing.md`, `ctf-writeup/SKILL.md`, and the repository's fixture lessons about decoys, reading JavaScript, checking protections, and inspecting complete output.
