# Cyber SEA Game 2026 · Human CTF Handbook

Prepared for Windows/WSL and Kali from the supplied repository and tool workbook.

- [Start here: the human solver's field guide](#00-start-here)
- [Tools and competition rules](#00-tool-rules)
- [First ten minutes: get evidence before guessing](#01-first-ten-minutes)
- [Web exploitation: follow the request to the trust boundary](#02-web-exploitation)
- [Disk, memory, and host forensics](#03-forensics)
- [Network captures and hardware signals](#04-network)
- [Steganography, documents, and media](#05-steganography)
- [Reverse engineering: turn a program into a checkable explanation](#06-reverse-engineering)
- [Cryptography: recover the structure before the secret](#07-cryptography)
- [Binary exploitation: prove the primitive, then build the chain](#08-binary-exploitation)
- [Malware analysis and configuration recovery](#09-malware)
- [OSINT from supplied evidence](#10-osint)
- [Miscellaneous: turn unfamiliar artifacts into a small model](#11-miscellaneous)
- [Excluded workflows and advanced material](#12-excluded-and-advanced)
- [Pwn practice atlas: 43 cases, each with a specific lesson](#13-pwn-practice-atlas)
- [Advanced cryptography: choose a model you can verify](#14-advanced-crypto)
- [Tool matrix: the complete supplied list](#tool-matrix)
- [Source coverage and editorial decisions](#source-coverage)



---

<a id="00-start-here"></a>

# Start here: the human solver's field guide

This is a practical companion to the CTF skills repository: find the symptom you have, run a small test, interpret the result, and choose the next step. You do not need to know the vulnerability name before opening a chapter.

**Built for both Windows/WSL and Kali.** Commands tagged `bash` belong in a Linux terminal, including WSL. Commands tagged `powershell` belong in Windows PowerShell. A `python` block is a script: save it under the filename given, then run it using the Python interpreter in that environment. Never paste a multiline Bash command straight into PowerShell.

## What to read tonight

1. Read **Tools and competition rules** and check the tools you expect to use.
2. Work through **First ten minutes** with one small local file.
3. Choose two of the six main subjects: web, forensics, network, steganography, reverse engineering, and cryptography. Read their opening workflows, then try a concrete recipe.
4. Keep the **tool matrix** handy when a familiar program is missing. Approved does not mean installed correctly.
5. Use the supplementary pwn, malware, OSINT, miscellaneous, and advanced sections when the evidence calls for them.

The official 2026 event page identifies AJCCBC and Trend Micro, lists the six main categories, and gives 26–27 October in Bangkok. This guide prioritizes those subjects; the vendor's identity does not reveal tomorrow's challenges. [Official event page, checked 25 October 2026](https://ajccbc.ncsa.or.th/cyber-sea-game-2026/).

## Find your starting point

| What you have | First useful question | Open |
| --- | --- | --- |
| A website, cookie, request, or source archive | Where does my input reach a trust decision? | Web exploitation |
| A disk image, event log, registry hive, or memory dump | Which artifact answers the question, and in what time zone? | Forensics |
| A PCAP or stream of packets | Which conversation carries the relevant data? | Network |
| An image, audio file, PDF, or suspicious whitespace | Is it damaged, appended, encoded, or hiding a second layer? | Steganography |
| An ELF, EXE, APK, DLL, WASM, or bytecode file | Where is the input compared with the expected value? | Reverse engineering |
| Large numbers, ciphertext, an oracle, or encryption source | Which assumption does the implementation break? | Cryptography |
| A native program with an established corruption bug | What can I read or overwrite, and what protections matter? | Binary exploitation |
| A packed script or suspicious executable | Can I recover the behavior without executing it? | Malware |
| A clue about a place, identity, or domain | What independent evidence would distinguish the candidates? | OSINT |
| A restricted interpreter, layered encoding, game, or signal | What are the exact rules and data representation? | Miscellaneous |

Categories overlap. Recover a file from a packet capture, identify its format, then switch to the appropriate chapter. A remote port alone does not make a challenge pwn.

## How each recipe works

**Recognize:** the clues that justify trying it. **Run:** a command or complete small script. **Read the result:** what success, failure, and misleading output look like. **Next:** the cheapest evidence-backed follow-up.

Examples use names such as `challenge.bin`, `capture.pcapng`, and `image.png`. Replace them with your actual filenames. Addresses such as `challenge.example` are placeholders, not live targets. Addresses, offsets, stream numbers, process IDs, database names, and flags in examples are illustrative unless explicitly called a self-contained toy.

Commands are recipes, not a script to run top to bottom against every challenge. Read the surrounding paragraph before copying a block. Some blocks contain several alternatives; choose the one that matches your evidence.

## Read this guide in either format

- **Website:** open `index.html` in Chrome. It embeds all content, styles, and search data. It makes no network requests. Search accepts several words, such as `RSA shared prime` or `Windows event log`. Press `/` to focus search and Escape to return to the chapter.
- **Markdown:** open `HANDBOOK.md` for the whole guide, or a file in `chapters/` for a smaller topic. Obsidian, VS Code, Notepad++, or a plain text editor can read it.
- **Print:** the website's print button prints the current chapter. Search results can also be printed. Code blocks wrap in print but preserve their original text when copied.
- **Tool matrix:** look up the exact program name and its environment. The workbook is the authority for the supplied list, not a package's popularity.

The guide is prepared study material. The supplied list does not establish whether bringing this handbook, prepared scripts, or removable media is permitted. Check that specific point with the organizers before using it during the event. No AI service is needed to read it.

## Useful vocabulary

| Term | Meaning in a solve |
| --- | --- |
| Artifact | A file or record you can examine: capture, dump, log, image, or executable. |
| Baseline | A normal request or input whose output you record before changing one thing. |
| Primitive | A specific ability you have proved, such as reading one file or leaking one address. |
| Offset | A distance from a known starting point. State whether it is bytes, sectors, or a virtual address. |
| Endianness | The order of bytes in a number. x86 commonly stores the least significant byte first. |
| Encoding | A reversible representation, such as hex or Base64. It does not require a secret key. |
| Encryption | A keyed transformation. Correct decoding alone does not decrypt it. |
| Oracle | A service whose answers reveal something about a hidden value. |
| False positive | An output that resembles your answer without enough evidence to support it. |
| Pivot | Changing approach because a result points somewhere else. |

## What this edition preserves

The original repository remains available alongside this folder. Repeated agent instructions have been consolidated into human workflows. Advanced and historical material has its own sections, with prerequisites rather than promises that old exploits work on new systems. The source coverage appendix records where each original file went and what was excluded. Original examples are not all validated exploits; this edition is also not a guarantee that an organizer's installation will run every command unchanged.


---

<a id="00-tool-rules"></a>

# Tools and competition rules

The supplied workbook is `AJCCBC_CTF2026_Tool_Review_List_261015r11.xlsx`. All three sheets were inspected, including their introductory notes and installation remarks. There are **39 Windows/WSL entries, 161 Kali entries, and 82 unapproved entries**. These are row counts, not counts of unique executable names.

## Read approval and availability separately

| Label | What it means | What to do |
| --- | --- | --- |
| Approved · Windows | Listed on the Windows sheet and installed natively according to its location column. | Use the Windows GUI or PowerShell invocation shown. |
| Approved · WSL | Listed on the Windows sheet, but installed in WSL. | Enter the existing WSL environment first. |
| Approved · Kali | Listed on the Kali sheet for the supplied AWS environment. | Use that environment and check the recorded location. |
| Approved · availability uncertain | Listed, but version/path is missing or startup failed. | Check availability early; keep the documented alternative ready. |
| Unapproved | Appears on the unapproved sheet, even when the reason is installation trouble. | Use the approved alternative. Do not reinstall it by another route. |
| Not listed | No explicit entry was found. | Do not assume approval just because it is common in CTFs. |

The sheet titled “Unapproved List” says its entries could not be installed; individual reasons distinguish unsupported, unnecessary, licensing, and explicitly prohibited tools. Preserve that distinction. An installation failure is not the same explanation as a rule prohibition, but neither gives you approval to use the tool.

Routine shell syntax and basic filesystem commands are used as operating-system facilities. They are not individually certified by this guide. Approval of a host application does not establish approval for every extension or online service it can access.

## The important restrictions

The official rules prohibit AI tools and unapproved software, limit activity to the permitted challenge targets, and prohibit publishing challenge content or uploading it to public analysis services. They also prohibit obtaining outside help during the competition. [Official rules, sections 7 and 9](https://ajccbc.ncsa.or.th/cyber-sea-game-2026/).

The workbook's Windows `B5`, Kali `B4`, and Windows `H14:H15` specifically prohibit AI/ML libraries and tools. The Python and uv notes permit non-AI libraries, but this does **not** certify that any particular library is already installed, allow an explicitly rejected tool, or authorize a remote service. Keep permission, installation, and service access as three separate checks.

There are no agent/MCP instructions in the working recipes. Do not use the original repository's agent installer, AI model routing, promptfoo evaluations, Tavily search, or AI/ML attack tooling during the competition. Read the exclusions chapter for their dispositions.

The unapproved sheet explicitly rejects online analysis services and online decompilers/compilers (`B51:C52`), including examples such as VirusTotal and CrackStation. Do decompilation, decoding, hashing, and cracking locally with listed tools. The locally installed `factordb-python` entry does not resolve permission to upload a challenge modulus to FactorDB. Similarly, the listed local AperiSolve checkout does not authorize the public upload website.

## Windows is not the same thing as WSL

The workbook lists these as native Windows tools: Chrome, Wireshark/TShark, a PDF viewer, OpenVPN Client, x64dbg, Autopsy, HxD, Notepad++, dnSpyEx, and Eric Zimmerman's Tools. CyberChef is a browser bookmark. WSL itself is installed on Windows.

Python 3, uv, GDB, objdump, strings, zsteg, binwalk, ExifTool, pdftotext, can-utils, cannelloni, Zeek, ZBar, Burp Community, jq, Ghidra, Sleuth Kit, OpenSSL, xz, qpdf, llvm-mc, xxd, fsck.fat, RsaCtfTool, and Volatility 3 are marked as installed **in WSL**. The OpenSSH recovery plugin is marked as installed in Volatility 3. See Windows `C14:I39`.

Run this in **PowerShell** to see the existing distributions. It does not install anything:

```powershell
wsl --list --verbose
wsl
```

Use the existing distribution. A Windows path such as `C:\Users\YourName\Downloads\challenge.bin` normally becomes `/mnt/c/Users/YourName/Downloads/challenge.bin` inside WSL. Quote paths with spaces. Do not assume that files on the remote Kali AWS machine also exist on the Windows laptop.

Inside **WSL**, check the tools you will need:

```bash
python3 --version
command -v gdb objdump strings exiftool xxd binwalk
python3 -c "import sys; print(sys.executable)"
```

Inside **Kali**, check its separate installation:

```bash
command -v file curl rg r2 checksec ffuf sqlmap
r2 -v
python3 --version
```

Output paths prove that a command is discoverable. A missing path means it is not on `PATH`, not necessarily that it is absent. Check the tool matrix for `/opt/tools/...` locations before giving up. Running `--help` is often more reliable than `--version`; the workbook records several tools that do not support a version option.

## Predictable problems and approved alternatives

| Problem | Better route |
| --- | --- |
| IDA Free or Binary Ninja is unavailable | Ghidra in WSL, or radare2 on Kali. |
| Windows Procmon/WinDbg is unavailable | Use the specific x64dbg workflow or inspect offline artifacts with Autopsy/Zimmerman tools. Linux strace observes Linux programs only. |
| ImHex or an image-mounting utility is unavailable | HxD on Windows; xxd in WSL; Sleuth Kit extraction without mounting. |
| Copy As Python-Requests / JWT Editor / Hackvertor is unavailable | Burp Repeater, curl on Kali, Python standard library in WSL. |
| Dirsearch is unavailable | Approved ffuf, Gobuster, or Feroxbuster with a small, relevant wordlist and bounded rate. |
| SageMath is listed but does not start | Basic RSA/XOR/modular arithmetic recipes use Python; advanced lattice work still needs a working supported environment. |
| A Python package imports in one tool but not in `python3` | pipx isolates environments. Use the installed application entry point; do not assume every module is globally importable. |
| A GDB plugin fails or conflicts | Use `gdb -nx` for plain GDB; GEF is separately recorded at `/opt/tools/gef.py`. |
| Volatility reports missing symbols | Record the exact OS/build and existing symbols. The full Volatility 3 symbol-table ZIP collection is unapproved (`B82:C82`). Use other artifacts instead of promising a fix. |
| The listed SSTV command does not decode | The Kali entry says decoder but records PySSTV, which may be an encoder package. Check its help; use the audio diagnostic workflow and do not assume MMSSTV/RX-SSTV approval. |

## Non-AI Python package checks

Prefer standard-library recipes. For an optional library, verify it without running an installer:

```bash
python3 -c "import importlib.util; print({m: importlib.util.find_spec(m) is not None for m in ('Crypto', 'sympy', 'PIL', 'pwn', 'z3')})"
```

`True` means the active interpreter can find a module, not that its version is compatible or that every capability is permitted. `Crypto` is the import name typically provided by PyCryptodome; `PIL` comes from Pillow; `pwn` from pwntools; `z3` from z3-solver. These names are not interchangeable with package installation names. No blanket installation commands are included.

If a recipe specifically needs PyCryptodome and it is missing, the Windows sheet's non-AI-library permission provides a targeted **WSL-only** route using the listed uv installation. First confirm `command -v python3` prints an existing interpreter. From your working directory, create a separate environment rather than changing the organizer's system packages:

```bash
uv venv --python "$(command -v python3)" .ctf-venv
uv pip install --python .ctf-venv/bin/python pycryptodome
.ctf-venv/bin/python -c 'from Crypto.Cipher import AES; print(AES.block_size)'
```

Expected output from the last command: `16`. Run the relevant saved script with `.ctf-venv/bin/python your_script.py`, replacing the filename. Creating a new environment does not copy every package from system Python. This setup needs access to an allowed package source; if unavailable, use the standard-library route or existing approved tool. It does not establish a separate Kali installation permission. Syntax reference: [uv environments](https://docs.astral.sh/uv/pip/environments/) and [package management](https://docs.astral.sh/uv/pip/packages/).

## Do not lose time to the repository installer

The source's `scripts/install_ctf_tools.sh all` is designed for an unrestricted agent workstation. It is not a competition setup step. It installs a broad collection that does not match this event's whitelist. Likewise, the original generated catalog loads external analytics and links to agent skills; this offline website does neither.

Use the tool matrix to resolve a concrete need. Use the organizer's existing environment. Preserve the organizer's recorded versions even if a tool's public website now advertises a different one.


---

<a id="01-first-ten-minutes"></a>

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


---

<a id="02-web-exploitation"></a>

# Web exploitation: follow the request to the trust boundary

Use this chapter for an organizer-provided web challenge. A successful probe changes one controlled input and explains one observable difference. Record the request, response, account, and prerequisite before trying a longer chain.

The official event categories include Web. This chapter also retains useful web material from the repository's miscellaneous and historical notes. Historical payloads are hypotheses: the deployed language, library version, parser, and challenge source decide whether they apply.

## Where the commands run

| Environment | Use here | Do not assume |
|---|---|---|
| Windows desktop | Chrome and its DevTools; approved editor | Native Python, curl, or Burp installation |
| Windows WSL | Python 3, Burp Community, jq, OpenSSL; these are in the Windows approved sheet | ffuf, sqlmap, Node.js, or Burp extensions |
| Organizer Kali | curl, ffuf, sqlmap, Git, ripgrep, Node.js and listed tools, after a version check | Every Windows-sheet tool is also installed; best-effort installations may fail |

All `bash` blocks below run in WSL or Kali unless labelled **Kali only**. Start WSL from PowerShell with `wsl`; use `/mnt/c/...` for Windows files. Save Python blocks as the named `.py` file, then run `python3 filename.py`. The Windows sheet permits adding non-AI Python libraries, but they are not all preinstalled and the same installation permission is not inferred for Kali; the examples use the standard library unless a dependency is explicitly identified.

Use Burp Community manually. The workbook rejects Copy As Python-Requests, GraphQL Raider, Hackvertor, and JWT Editor extensions. MCP automation, AI agents, public webhook services, and public challenge uploads are not part of this workflow.

## 1. Establish a baseline you can reproduce

1. Read the challenge description and supplied source. Write down the permitted host, port, and any separate bot or callback service.
2. Open the application once in Chrome. Record the URL after redirects, page title, visible forms, and the account you used.
3. In DevTools → Network, preserve the log and perform one normal action. Open the request's Headers, Payload, Response, and Cookies views.
4. Look for route names and API calls in supplied JavaScript. Identify data the server trusts: user IDs, prices, filenames, URLs, template text, serialized objects, and roles.
5. In Burp, start a temporary project, open Proxy → Open browser, and browse the challenge. If that GUI is unavailable on the WSL workstation, use Chrome DevTools and the Python request below.
6. Send the interesting request from Proxy HTTP history to Repeater. Send it unchanged twice. Dynamic nonces and timestamps should be understood before interpreting length differences.

Keep TLS verification enabled. If the organizer supplies a challenge CA, configure that CA in the client. A certificate failure is a connection problem, not a vulnerability signal.

**Kali only**, replace the URL with the challenge URL:

```bash
curl --version
curl --max-time 10 --dump-header baseline.headers --output baseline.body 'https://challenge.example/'
```

The two files contain response headers and body separately. This request does not follow redirects; read `Location` first. A `302` to login means the baseline is unauthenticated. A `429` means pause and obey `Retry-After`.

**WSL/Kali Python alternative**, save as `fetch_once.py`:

```python
import sys
import urllib.request
import urllib.error
from pathlib import Path

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

if len(sys.argv) != 2:
    raise SystemExit('usage: python3 fetch_once.py https://CHALLENGE/path')
opener = urllib.request.build_opener(NoRedirect)
req = urllib.request.Request(sys.argv[1], headers={'User-Agent': 'CTF-manual/1.0'})
try:
    response = opener.open(req, timeout=10)
except urllib.error.HTTPError as exc:
    response = exc
with response:
    body = response.read(2_000_001)
    if len(body) > 2_000_000:
        raise SystemExit('response exceeds local review limit')
    Path('baseline.body').write_bytes(body)
    Path('baseline.headers').write_text(str(response.headers), encoding='utf-8')
    print(response.status, len(body), response.headers.get('Location', ''))
```

Expected output is a status, byte count, and possibly a redirect. This script deliberately makes one request. Compare the saved body with what Chrome displays; JavaScript may fetch the actual data later.

## 2. Build a small route and parameter map

Use evidence already present in the application before guessing names. A linked `/api/profile`, source comment, JavaScript route, exposed source archive, or a challenge hint is a useful starting point.

| Evidence | One next action | Interpretation |
|---|---|---|
| JavaScript calls `/api/items/17` | Replay the exact request | Learn the response structure and authentication |
| An object contains `ownerId` | Compare objects belonging to two challenge accounts | Separate authentication from ownership checks |
| Source uses a pathname parameter | Request one known permitted filename | Establish the file-read baseline |
| Response has `Server`, framework cookies, or stack trace | Match against supplied dependency files | Headers alone do not prove a version |
| `robots.txt` links a route | Open that listed route once | Disallowed crawling is not an access control |
| Supplied `.git` directory | Inspect locally; do not clone unrelated organizations | Deleted challenge files may remain in history |

**Kali only**, with a supplied repository:

```bash
git -C challenge-source log --oneline --all -20
git -C challenge-source log --all --oneline -- config.py
git -C challenge-source show COMMIT:config.py
rg -n 'fetch\(|axios|/api/|SECRET|verify|unserialize|render_template_string' challenge-source
```

Replace `COMMIT` with a commit from the log. A hit is a lead; verify whether the running challenge uses that code. Do not print credentials into shared notes unnecessarily.

If source reveals a route prefix and a short set of plausible names, make a small local list. **Kali only**:

```bash
printf '%s\n' profile export status > routes.txt
ffuf -w routes.txt -u 'https://challenge.example/api/FUZZ' -t 1 -rate 1 -timeout 10 -maxtime 30 -mc all -of json -o routes.json
```

Run this only after recording why `/api/` and these three names are plausible. Inspect every response manually. A site may return `200` with the same error page for all paths. Stop on rate limiting or repeated server errors. Avoid recursive scans and large default dictionaries; this chapter does not use the repository's high-concurrency fuzzer.

For a confirmed technique, the Kali workbook includes an offline PayloadsAllTheThings copy. Search its relevant chapter rather than downloading or spraying a bulk payload collection:

```bash
rg -n -i 'sqlite|union' '/opt/tools/PayloadsAllTheThings/SQL Injection'
rg -n -i 'jinja|flask' '/opt/tools/PayloadsAllTheThings/Server Side Template Injection'
```

Read the nearby explanation and match its parser/version assumptions to your challenge. A missing directory is an environment limitation; the repository's automatic clone instructions are not needed.

## 3. Repeater as the main experiment notebook

Create tabs called `baseline`, `candidate`, and `negative-control`. Disable automatic redirect following while investigating login or access checks. Let Burp update `Content-Length` when you edit a body.

Example request, with your own session cookie substituted:

```http
GET /api/notes/17 HTTP/1.1
Host: challenge.example
Cookie: session=YOUR_CHALLENGE_SESSION
Accept: application/json

```

Change only `17` to the ID of an object made by your second challenge account. Compare status, body, owner, and whether a new `Set-Cookie` appears. A `200` with `{"error":"forbidden"}` is denied access; status alone is not proof.

For a POST, preserve content type and CSRF handling:

```http
POST /api/profile HTTP/1.1
Host: challenge.example
Cookie: session=YOUR_CHALLENGE_SESSION
Content-Type: application/json

{"displayName":"ctf-marker-17"}
```

A CSRF token may be single-use or session-bound. If a replay fails, obtain a new normal request before blaming your changed field. Keep raw bytes: form data, JSON, multipart, URL percent encoding, and HTML entities are different decoding layers.

## 4. Authentication and access control

### Ownership and mass assignment

Use two accounts you control. Compare a request from each, then substitute an object identifier without changing the session. If the application accepts an extra `role`, `owner`, or `balance` field, verify the value with a separate read request. An echoed field can be ignored by the database.

For WebSocket or server-sent events, connect normally, log out in another tab, then send one benign message on the existing connection. Acceptance after logout is evidence of stale authorization only if the operation actually needs a current session. Inspect the upgrade handshake and subsequent frames separately.

### Cookies and state

Record the cookie name, domain, path, Secure, HttpOnly, SameSite, and expiration. HttpOnly prevents JavaScript reading a cookie; it does not prevent a browser sending authenticated requests. Cookie `Path` is not an authorization mechanism. A base64-looking cookie may be signed, encrypted, or just encoded; decode a copy before changing it.

Distinguish these observations:

- Editing a role and receiving rejection suggests an integrity check.
- Editing a role and seeing the old role suggests the server ignores the field.
- Replaying an old signed balance after spending suggests state rollback; verify with a fresh balance query.
- Receiving a session at a public admin-login route is normal unless that session already authorizes an admin action.

### Normalization and parser disagreements

When source compares strings differently from the framework, compare one encoded representation with its decoded equivalent: `/admin/item` versus `/%61dmin/item`, for example. Preserve the raw path in Burp. A browser may normalize it before transmission.

Do not spray all encodings. First determine which component validates the input and which component uses it. Relevant source patterns include `startswith`, regex anchors, repeated URL decoding, `basename`, route middleware, Unicode case folding, and delimiter-based account records.

For username normalization, create two ordinary test names that differ by case or a documented normalization rule. Confirm which account is returned. Do not assume provider-specific email alias handling is universal.

### Password and OTP hypotheses

Do not start with a login brute force. First check whether the challenge supplies a small candidate space, source-generated passwords, a timestamp seed, or an offline verifier. Prefer testing candidates locally. One failed login with a known wrong password establishes the failure signature; a second known account establishes whether username enumeration exists.

If an online candidate test is necessary, use a few challenge-derived candidates, one at a time, and stop on lockout or rate limiting. A redirect, response length, or missing error string alone does not establish login success; fetch the authenticated account page afterwards. Recreate any frontend password transform from the supplied JavaScript before testing.

## 5. JWT and JWE: inspect before changing

JWT normally has three base64url segments. JWE compact serialization normally has five. Encryption with a public key does not authenticate who created the ciphertext; a challenge that accepts arbitrary encrypted claims may need an independent signature or server-side authorization check.

Save this local decoder as `decode_token.py`. It does not verify signatures:

```python
import base64
import json
import sys

def decode(segment):
    return base64.urlsafe_b64decode(segment + '=' * (-len(segment) % 4))

token = sys.argv[1]
parts = token.split('.')
print('segments:', len(parts))
for i in ([0, 1] if len(parts) == 3 else [0]):
    try:
        print(i, json.dumps(json.loads(decode(parts[i])), indent=2))
    except (ValueError, IndexError) as exc:
        print('not a JSON segment:', i, exc)
```

```bash
python3 decode_token.py 'PASTE_YOUR_CHALLENGE_TOKEN'
```

Look at `alg`, `kid`, `jku`, embedded `jwk`, issuer, audience, subject, expiration, and role. Do not conflate the identity claim with the authorization claim. Compare tokens from two accounts to understand which fields matter.

If source omits signature verification, edit a harmless display claim and observe a separate authenticated page. If it explicitly accepts `alg: none`, the missing signature is the hypothesis. If it accepts both HMAC and RSA, check whether the same raw key bytes are mistakenly used for both; modern libraries often prevent this confusion.

`kid` traversal requires a file-based key loader; `jku` injection requires the verifier to fetch an untrusted key URL. A header existing is not enough. Any URL used must be organizer-provided infrastructure, not a public JWKS or callback host.

**Kali only:** `jwt_tool --help` can show the installed command's inspection syntax. Prefer the decoder above for transparent inspection. Do not assume the rejected JWT Editor Burp extension is available.

## 6. SQL injection: prove the expression boundary

Start from a parameter that plausibly reaches SQL and a stable baseline. Read source if supplied. Numeric, quoted string, identifier, and `ORDER BY` contexts require different syntax.

Example numeric context, tested separately in Repeater:

```http
GET /item?id=1%20AND%201=1 HTTP/1.1
Host: challenge.example

```

```http
GET /item?id=1%20AND%201=2 HTTP/1.1
Host: challenge.example

```

Expected evidence: the first response matches item 1, the second gives the application's normal no-result page, and the unchanged baseline remains stable. This pair does not work if input is parsed as an integer before querying; that failure narrows the hypothesis.

For a single-quoted string, adapt to the actual query. A trailing SQL comment must be valid for the database, and MySQL's `--` comment requires following whitespace. Do not copy a payload from a different DBMS and treat its error as proof of a WAF.

### Visible results

After a boolean difference is confirmed, find the projection width with a small number of `ORDER BY` or `UNION SELECT NULL` probes appropriate to the query. Use a unique marker in one compatible text column. Retrieve only the challenge-relevant table or row indicated by schema or source.

Common failures are mismatched column counts, incompatible types, pagination hiding your row, and the original query returning before your injected row. Store each successful intermediate request.

### Blind results

Define a reliable true/false predicate before extracting text. Check both outcomes several times. Measure lengths only after removing dynamic tokens. For timing, alternate true and false probes and compare repeated measurements; network jitter can exceed the intended delay. Avoid expensive expressions such as huge `randomblob` allocations.

A local binary search rehearsal makes the extraction logic clear:

```python
# Save as oracle_search.py; this toy does not contact a server.
secret = 73
queries = 0
def is_at_most(value):
    global queries
    queries += 1
    return secret <= value

lo, hi = 0, 255
while lo < hi:
    mid = (lo + hi) // 2
    if is_at_most(mid):
        hi = mid
    else:
        lo = mid + 1
assert lo == secret
assert queries <= 8
print(lo, queries)
```

Expected output is `73 8`. The real oracle must answer the same mathematical predicate; mixing `>` and `>=` causes off-by-one failures. Determine string length and character encoding before iterating positions.

### Targeted sqlmap after manual confirmation

**Kali only:** save the confirmed request from Burp as `request.txt`, with its current session and token. Check that it points only at the challenge host.

```bash
sqlmap --version
sqlmap -r request.txt -p id --level=1 --risk=1 --technique=B --threads=1 --delay=1 --timeout=10 --retries=0 --batch
```

This confines testing to the observed `id` parameter and boolean technique. Review detected DBMS and the exact injection evidence. A token-expiration error is not a negative SQLi result. Do not add `--dump-all`, OS shells, tamper chains, or unrelated parameters automatically. For TLS requests, preserve the correct target scheme when exporting or use the installed help's TLS option.

### Less obvious SQL input paths

| Pattern in source | Diagnostic | What to do after a positive result |
|---|---|---|
| Stored name used in a later query | Put a unique marker in the stored field; trigger the later view | Test the later query boundary, not only registration |
| Sort key inserted unquoted | Compare a permitted column with a simple expression | Map identifier/expression context |
| `INSERT` or duplicate-key update | Inspect all inserted columns and conflict handling | Track which field can shift or overwrite another |
| Image metadata, QR, DNS answer, or header reaches SQL | Follow that exact data path with a marker | Capture decoded input before testing SQL syntax |
| Escaping plus multibyte conversion | Identify charset and order of operations | Reproduce the conversion locally on bytes |
| Two passes of formatting | Compare literal `%` and a benign format marker | Separate application formatting from SQL parsing |
| Keyword replacement filter | Inspect whether replacement repeats | Model one transformation; do not assume comment fragmentation works |

MySQL process-list tricks, historical `PROCEDURE ANALYSE`, backtracking limits, and column truncation are version- and configuration-dependent. Check the supplied schema and DBMS version; do not treat old writeup dates as applicability evidence.

## 7. NoSQL, LDAP, XPath, and GraphQL

JSON is not automatically safe. If a MongoDB query directly uses an input object, test whether a field accepts an operator-shaped value instead of a string. Compare a known account with a non-matching condition first. If validation rejects objects, pivot rather than spraying `$where` JavaScript.

LDAP and XPath use different grammar from SQL. Locate a concatenated filter or XPath expression in source, then test one matching/non-matching predicate while preserving balanced syntax. A wildcard returning multiple directory records is an enumeration signal only if that endpoint was meant to return one.

GraphQL inspection in Repeater needs no extension:

```http
POST /graphql HTTP/1.1
Host: challenge.example
Content-Type: application/json

{"query":"{ __typename }"}
```

If this returns a JSON `data` object, consult the supplied schema or the application's own queries. Introspection may be disabled. Request a single known field before attempting nested queries or aliases. An alias changes the response key; it does not itself bypass access checks. Compare authorization for the same object through two resolvers.

## 8. File reads, paths, and uploads

Use a file already identified by the challenge source or description. A request for an arbitrary operating-system file may prove traversal, but the shortest useful proof is usually a challenge-specific configuration or marker.

If `file=welcome.txt` is the normal input, try one relative traversal suggested by the source directory layout. Distinguish reading raw bytes, template inclusion, archive extraction, and executable upload: they are different capabilities.

PHP `php://filter` is relevant only when a PHP stream function accepts a wrapper. In Repeater, a source-reading hypothesis might use:

```http
GET /view?file=php://filter/convert.base64-encode/resource=index.php HTTP/1.1
Host: challenge.example

```

Expected evidence is base64 that decodes to the application's PHP source. Decode locally and verify syntax and route names. A rendered login page or literal error string is not source disclosure. Wrapper restrictions, suffix appending, and include paths can invalidate the probe.

For uploads, begin with a harmless text or image marker. Record original filename, multipart content type, saved filename, destination URL, and response content type. Check whether the file is renamed or re-encoded. Re-encoding destroys many appended polyglots.

Archive traversal checks start with listing members, not extracting over your working tree:

```python
# Save as inspect_zip.py; run with the challenge ZIP path.
import sys
import zipfile
from pathlib import PurePosixPath

with zipfile.ZipFile(sys.argv[1]) as archive:
    for item in archive.infolist():
        p = PurePosixPath(item.filename.replace('\\', '/'))
        mode = item.external_attr >> 16
        unsafe = p.is_absolute() or '..' in p.parts or bool(p.parts and ':' in p.parts[0])
        symlink = (mode & 0o170000) == 0o120000
        print(item.filename, 'size=', item.file_size,
              'traversal=', unsafe, 'symlink=', symlink)
```

A symlink member followed by a file through that link is a different risk from a `../` filename. Windows drive paths and separators need separate review. Challenge upload extraction may behave differently from your local ZIP library.

Historical `.htaccess`, `.phar`, `zip://`, short-name, null-byte, and double-extension tricks need the matching server and language version. Prove how the stored file is handled before trying code execution.

## 9. Template, format-string, and command injection

### Template arithmetic first

For a field rendered by a template engine, submit `ctf-{{7*7}}-end` and compare it with a literal control. A response containing `ctf-49-end` suggests evaluation. It does not uniquely identify Jinja2; several engines use similar syntax.

Read the stack trace, template source, or dependency file. Map the exact context: template source versus a variable passed to a fixed template, expression versus statement, and server-side versus client-side rendering. Then use the engine's documented syntax to inspect one harmless available value.

Python `str.format` is not Jinja2 and does not evaluate arbitrary expressions. Its field traversal can still expose attributes or dictionary entries if sensitive objects are passed into the format operation. A literal `{7*7}` remaining unchanged is expected there.

### Command and argument boundaries

If source concatenates input into a shell command, a benign marker distinguishes command execution from validation. Adapt one separator to the proven shell context, for example a URL-encoded newline followed by `printf CTF_PROBE_17` in a challenge-controlled command parameter.

Do not send a reverse shell as the first test. Determine whether output appears in the response, a generated file, or a challenge-provided log. If output is suppressed, a small bounded timing control can be tested repeatedly, but ordinary slowness is not sufficient evidence.

An argument array can prevent shell parsing while still accepting dangerous program options. A filename beginning with `-` can be an option if the called program lacks `--`. Inspect the complete command construction, including archive, mail, Git, image metadata, and renderer subprocesses.

Languages matter: Ruby `eval`, Perl two-argument `open`, Lisp reader macros, Prolog queries, Lua interpolation, PHP legacy evaluation functions, and LaTeX shell escapes have different entry points. Modern runtimes remove some historical features. Reproduce the input-to-evaluator transformation locally before constructing a longer payload.

## 10. SSRF and XML: identify the fetcher

An SSRF candidate is a URL or hostname that the server fetches. First use an organizer-provided callback or an allowed URL within the challenge. Compare a known reachable path with a known missing path. Record response status, fetched content, or callback logs. Do not use public webhook services or cloud metadata endpoints outside the assigned challenge.

Write down the sequence:

```text
input bytes → URL parser → allowlist → DNS resolution → redirect handling → HTTP client
```

Parser disagreement only helps when the validator and fetcher disagree. Test one discrepancy supported by source: userinfo `@`, encoded path separators, host normalization, redirects, or an unanchored hostname regex. A fetch failure might be TLS, DNS, firewall, scheme restriction, or parsing; distinguish these using a normal URL.

If the challenge explicitly includes an internal service, first request its harmless health or version endpoint. Docker APIs, Redis, SMTP, MySQL, and renderer attachments require protocol-specific behavior; HTTP SSRF alone does not imply arbitrary TCP access. A `gopher` string is useless if the actual client does not support that scheme.

For XML, begin with an internal entity that expands to a marker:

```xml
<?xml version="1.0"?>
<!DOCTYPE note [<!ENTITY probe "CTF_XML_MARKER">]>
<note>&probe;</note>
```

If the parser expands it, inspect whether external entities are enabled. Internal expansion does not prove external file/network access. For a challenge that explicitly provides a marker file, the next entity may reference that exact file. Save parser errors: disabled DTDs, missing root elements, namespace requirements, and conversion pipelines change the behavior.

Office documents, SVG, PDF renderers, XMLDecoder, XSLT, and SOAP can hide XML parsing inside uploads or conversions. Follow the actual conversion chain. Avoid publishing external DTDs; use only provided infrastructure where an out-of-band test is necessary and allowed.

## 11. Deserialization and prototype pollution

Never deserialize an unknown challenge object in your normal working interpreter just to inspect it. Python pickle, marshal-derived code, Java objects, PHP magic methods, .NET polymorphic objects, and XML object decoders can invoke behavior.

For a suspected pickle, disassemble bytes without loading objects:

```bash
python3 -m pickletools suspect.pickle
```

Look for `GLOBAL`, `STACK_GLOBAL`, `REDUCE`, object construction, and `STOP`. Decode any outer base64 or ROT13 layer into a new file first. A pickle stream may contain appended objects; the first `STOP` can hide data ignored by a simple loader.

For other formats, identify the entry function and allowed classes from source. The repository's generic Java gadget-tool invocation is not an approved-tool assumption. A useful local proof can be a harmless object whose known hook writes a marker in the challenge sandbox, only after the matching class exists.

Prototype pollution requires a controllable merge or path setter plus a reachable gadget. Send an inert property such as `ctfProbe`, inspect an independently created object in a supplied local reproduction, and determine whether the property is inherited. Do not infer code execution from accepting a `__proto__` key.

**Kali only**, a local JavaScript distinction:

```javascript
// Save as prototype-demo.js, run: node prototype-demo.js
const parsed = JSON.parse('{"__proto__":{"ctfProbe":17}}');
console.log(Object.hasOwn(parsed, '__proto__')); // true
console.log(({}).ctfProbe);                    // undefined
```

Parsing JSON alone does not pollute the global prototype. The vulnerable merge, inherited configuration lookup, and template/VM gadget must each be demonstrated. Node's `vm` and browser-like DOM packages have version-specific boundaries; old constructor chains are not universal escapes.

## 12. Browser-side execution and origin boundaries

### Reflection is not execution

Put `CTF_MARKER_17` into the suspected field. Find it in the response source and live DOM. Identify whether it appears in text, an attribute, a JavaScript string, a URL, CSS, or a template. Choose one benign context-appropriate proof that changes the document, such as setting a visible marker. Avoid cookie collection as a first test.

Inspect CSP in both response headers and console errors. A policy blocking inline script may still permit an existing script gadget, but merely seeing a CDN domain is not proof of a bypass. `base-uri`, nonces, strict-dynamic, MIME type, and actual resource behavior matter.

If a challenge supplies an admin bot, reproduce its browser actions manually: start URL, authentication state, allowed schemes, navigation steps, and timeout. A payload working in your privileged browser might fail in the bot's fresh session. Use only the challenge's report interface and provided callback endpoints.

### DOM sources and sinks

| Source or behavior | Inspect | Common failure |
|---|---|---|
| `location.hash` | jQuery selector or HTML insertion call | Modern selector handling differs from historical versions |
| `postMessage` | Exact origin and source-window check | Checking only a substring or accepting `null` origin |
| `window.open` / opener | Navigation and cross-window references | Cross-origin property access is restricted |
| `Blob`, `data`, uploaded HTML | Resulting origin and MIME type | Opaque origins differ from normal same-origin pages |
| DOM clobbering | Named elements used as global configuration | The expected property may be a string, not a node |
| Client-side path construction | URL before and after normalization | Traversal may occur in the browser before the server |
| CSS selectors or font loads | Which condition causes a resource request | Character-set leaks do not reveal order or count |

Timing and XS-Leak tests require repeated positive/negative controls. Cache, fonts, network warmup, and bot startup are confounders. First demonstrate a one-bit distinction before attempting recovery of a longer value.

Do not run obfuscated JavaScript from a challenge in your everyday browser context. Read its strings and transformations in the provided challenge context or an isolated local reproduction. JSFuck, AAEncode, and JJEncode are encodings/obfuscation patterns, not automatic evidence of malicious behavior or a particular exploit.

## 13. OAuth, SAML, CORS, and signatures

Capture a complete normal login flow using your challenge accounts. Record authorization URL, redirect URI, state, nonce, callback, issuer, audience, and resulting session. A callback parameter is not necessarily trusted simply because it is present.

For state binding, initiate two flows in separate sessions and compare their callbacks. For email canonicalization, compare two controlled identities. For open redirects, use a harmless organizer-provided destination and verify the final browser URL. Do not register external provider accounts or take over public subdomains as part of this handbook.

For SAML, inspect the supplied XML and verifier configuration. Determine which element is signed and which element supplies the identity. Signature-wrapping and digest-confusion hypotheses need that mismatch; a valid signature on an unrelated element proves nothing about the consumed assertion.

CORS checks require a browser. A server reflecting an `Origin` header is not sufficient: check credentials, allowed methods, preflight, and whether JavaScript can read a sensitive response. `Access-Control-Allow-Origin: *` cannot authorize credentialed reads in the usual browser CORS model.

For custom signatures, identify the construction exactly. `hash(secret || message)` may permit length extension for some hashes; HMAC is different. CRC is not a cryptographic authenticator. Base64 leniency plus duplicate parameters can cause two parsers to verify and consume different messages. See [Cryptography](#07-cryptography) for byte-level verification examples.

## 14. Races, caches, and protocol parsing

Start race analysis from source showing a check and later update, or from a reproducible inconsistent result. Establish a sequential baseline, then attempt a pair of concurrent requests in the challenge only. Reset the challenge state if possible. A timeout is not a successful race, and widespread parallel retries obscure the cause.

For cache behavior, use a unique cache-busting key and your own challenge object. Inspect `Age`, cache status, `Vary`, ETag, and whether authenticated and anonymous responses differ. A static-looking suffix can influence caching; the origin route may still return dynamic content. Do not poison shared unrelated pages.

Request smuggling needs two HTTP parsers that disagree on request boundaries. Identify proxy and backend behavior from supplied configuration. Do not send ambiguous requests at the competition platform or shared infrastructure. In a dedicated local challenge reproduction, compare how each parser interprets length, transfer coding, headers, and connection reuse. Burp's displayed request is not proof of exact bytes sent over HTTP/2.

HTTP method changes and header tricks require a route-specific hypothesis. TRACE, Range, forwarded host, and proxy headers do not inherently bypass authorization. A server error may be a parsing discrepancy; save the exact raw response before following a chain.

## 15. Advanced source material: practical starting points

| Source family | Start with | Constraint and next step |
|---|---|---|
| Framework CVEs, RSC/Flight, Next middleware | Supplied lockfile, route architecture, middleware behavior | Match affected version and configuration using the offline advisory; do not infer a CVE from branding |
| Image/HTML/PDF renderer exploitation | Renderer name/version and one marker document | Observe whether content is fetched, embedded, or executed; avoid unapproved exploit generators |
| Debugger consoles | Actual debug page and supplied deployment config | A PIN prompt is not authorization; determine the intended challenge path and secret derivation |
| Serializer length changes | Before/after bytes and declared length fields | Reproduce expansion or truncation on a toy value before altering object structure |
| Regex timing and backtracking | Pattern, input limit, fail-open handling | Use short timed controls; never send uncontrolled resource-exhaustion payloads |
| Client HMAC or public-key encryption | Key origin and verification code | A client-visible symmetric secret cannot establish client trust; public encryption alone proves no sender identity |
| WebAuthn replay | Challenge generation, session binding, expiration | Replay only your captured challenge response and verify the server's state transition |
| Web3 contracts | Supplied source, ABI, storage layout, call authorization | Static review can expose delegatecall context, reentrancy order, signature replay, or unchecked calldata |
| Solidity storage/compiler quirks | Exact compiler version and generated artifact | No online compiler; unlisted toolchains are not assumed approved. Use source and supplied bytecode or organizer clarification |
| JA4/TLS fingerprints | Captured client hello and expected browser | Header ordering cannot reproduce all TLS fingerprints; prefer the intended approved browser |
| Host/service pivots | Explicit challenge service map | Stop at the challenge boundary; organizer workstations, scoring platform, and unrelated networks are outside scope |

Old cloud-takeover, CI credential-harvesting, public callback, AI-chatbot, and large-scale automation recipes are not runnable event workflows here. Their relevant trust-boundary concepts are retained above; exclusions are explained in [Excluded and advanced material](#12-excluded-and-advanced).

## 16. Turn a confirmed primitive into the challenge answer

The diagnostics above should lead to a concrete recovery step. Use the narrowest demonstrated primitive and the flag location or table indicated by the challenge. These examples are for the assigned challenge, with your observed parameter names and current session.

### Confirmed SQLi → selected flag column

**Kali only.** Start with the manually confirmed `request.txt` from section 6. Replace `challenge_db`, `flags`, and `flag_value` below with names learned in the preceding output. Preserve the technique that actually worked; `B` here means the demonstrated boolean oracle.

```bash
sqlmap -r request.txt -p id --technique=B --level=1 --risk=1 --threads=1 --delay=1 --timeout=10 --retries=0 --batch --dbs
sqlmap -r request.txt -p id --technique=B --level=1 --risk=1 --threads=1 --delay=1 --timeout=10 --retries=0 --batch -D challenge_db --tables
sqlmap -r request.txt -p id --technique=B --level=1 --risk=1 --threads=1 --delay=1 --timeout=10 --retries=0 --batch -D challenge_db -T flags --columns
sqlmap -r request.txt -p id --technique=B --level=1 --risk=1 --threads=1 --delay=1 --timeout=10 --retries=0 --batch -D challenge_db -T flags -C flag_value --dump --start=1 --stop=1
```

Expected progression: database list → selected table list → column names/types → one flag cell. If supplied source already names the table and column, skip discovery. If the first row is not the intended row, inspect the schema and use a known challenge identifier as a `--where` predicate rather than dumping unrelated data. Stop if the session expires or the oracle becomes unstable.

Without sqlmap on WSL, use the confirmed boolean oracle and the binary-search logic from section 6 to recover a known column character by character, or use a visible `UNION SELECT` result. Derive the exact DBMS substring and character-code syntax from the supplied database/source, and first verify length and the first known prefix character manually.

### Confirmed traversal → supplied flag file

Suppose the supplied source says the application reads from `/app/public` and the flag is `/app/flag.txt`. After `file=welcome.txt` and the traversal boundary have been confirmed, send:

```http
GET /view?file=../flag.txt HTTP/1.1
Host: challenge.example
Cookie: session=YOUR_CHALLENGE_SESSION

```

Expected response: the actual file bytes, including the challenge flag. A literal `../flag.txt`, a generic error, or a login page is not success. If the source appends `.txt`, supply `../flag` instead. If it resolves a different base directory, calculate the path from that directory; do not blindly add dozens of `../` segments.

For a confirmed XML external-entity reader with the same explicit flag path:

```xml
<?xml version="1.0"?>
<!DOCTYPE note [<!ENTITY answer SYSTEM "file:///app/flag.txt">]>
<note>&answer;</note>
```

Submit this through the application's normal XML field or upload, preserving its required root/namespace. The result may appear in a generated document rather than the HTTP body. If the content contains characters illegal in XML, a direct text entity may fail; the failure is not permission to upload the file to an external DTD service.

### Confirmed Flask/Jinja evaluation → challenge file

Use this only when supplied source identifies Flask/Jinja, arithmetic evaluation succeeded, the context exposes `get_flashed_messages`, and the source specifies `/app/flag.txt`. In the template-source field, the read expression is:

```jinja2
{{ get_flashed_messages.__globals__.__builtins__.open('/app/flag.txt').read() }}
```

Expected rendered output is the flag file content. This relies on a Python globals/builtins traversal and fails in a properly sandboxed or different context. If `__builtins__` is a module/dictionary or lookup behavior differs, inspect the supplied function's environment in the local reproduction rather than assuming another engine shares Jinja semantics. Let Burp encode the form field exactly once; raw braces in JSON do not need URL encoding.

### Confirmed missing JWT verification → modified challenge claim

This self-contained local demonstration models the specific broken verifier that decodes a JWT payload without verifying its signature. It does not forge a valid signature. Save as `jwt_unverified_toy.py`:

```python
import base64
import json

def encode(value):
    raw = json.dumps(value, separators=(',', ':')).encode()
    return base64.urlsafe_b64encode(raw).rstrip(b'=').decode()

def broken_verify(token):
    payload = token.split('.')[1]
    return json.loads(base64.urlsafe_b64decode(payload + '='*(-len(payload) % 4)))

token = encode({'alg': 'HS256', 'typ': 'JWT'}) + '.' + encode({'sub': 'test', 'role': 'user'}) + '.invalid'
header, payload, signature = token.split('.')
claims = broken_verify(token)
claims['role'] = 'admin'
modified = header + '.' + encode(claims) + '.' + signature
assert broken_verify(token)['role'] == 'user'
assert broken_verify(modified)['role'] == 'admin'
print(modified)
```

For the challenge, use your captured token and only the role/identity claim the broken verifier actually consumes. Send the modified token to the known flag endpoint, then verify the returned flag. A decoder displaying `admin` locally proves nothing about the server: a correct verifier rejects this token.

## 17. Finish with a reproducible result

Save a short sequence: normal baseline, minimal changed request, response evidence, and final challenge-specific result. Remove session secrets from any shared writeup. Verify the flag format and submit it through the organizer interface. If a hypothesis fails, record the reason: wrong parser, insufficient privilege, signed state, unavailable dependency, blocked network path, or noisy oracle.

The source material merged here includes every file under `ctf-web/`: reconnaissance and field notes; authentication, JWT, OAuth and infrastructure; SQL and other injections; paths, uploads, templates, command execution, deserialization, SSRF and XML; browser, cache, race, protocol and Web3 patterns. The MCP guide and asynchronous fuzzer are explicitly replaced with the manual, bounded workflows above. Detailed file dispositions are in `human-guide/review/web-coverage.json`.


---

<a id="03-forensics"></a>

# Disk, memory, and host forensics

Recover the smallest artifact that answers the question, then explain where it came from. A file name, a timestamp, and a matching hash are more useful than a directory full of unexplained carvings.

## Choose the right machine

Workbook references below use **Windows** for `Approved Tool List for Windows`, **Kali** for `Approved Tool List for Kali`, and **Unapproved** for `Unapproved List`.

| Environment | Available route | Workbook evidence |
|---|---|---|
| Windows native | Autopsy, HxD, Eric Zimmerman's tools; PowerShell built-ins | Windows rows 41, 42, 46 |
| Windows WSL | Python 3, strings, Sleuth Kit, xz, Volatility 3 | Windows rows 14, 18, 30, 32, 38 |
| Kali | EWF tools, qemu-img, TestDisk/PhotoRec, foremost, SQLite, Git, Volatility 2 | Kali rows 41, 122, 150, 51, 138, 56, 158 |

Commands marked **WSL** run in its Linux shell, not PowerShell. Windows approval does not imply that the same tool is installed or approved on the separate Kali machine. Python snippets here use the WSL Python approval; non-AI libraries are allowed by Windows row 14, subject to named exclusions. There is no blanket install step.

The event prohibits AI tools and public analysis uploads. Keep evidence local and act only on challenge endpoints. See the [competition rules](https://ajccbc.ncsa.or.th/cyber-sea-game-2026/).

## Preserve a baseline

Use this before extraction. `evidence.img` means the challenge-supplied image; `work` and `out` are new local directories.

**Windows PowerShell:**

```powershell
New-Item -ItemType Directory -Path work,out
Copy-Item -LiteralPath .\evidence.img -Destination .\work\evidence.img
Get-FileHash -Algorithm SHA256 -LiteralPath .\evidence.img
Get-FileHash -Algorithm SHA256 -LiteralPath .\work\evidence.img
Get-Item -LiteralPath .\evidence.img | Select-Object Name,Length,LastWriteTimeUtc
```

The hashes should match. Record the original size and hash in your notes. The download's modification time is not necessarily the suspect's file timestamp.

**WSL, quick identification:**

```bash
xxd -l 128 work/evidence.img
strings -a -n 8 work/evidence.img > out/strings-ascii.txt
strings -a -e l -n 8 work/evidence.img > out/strings-utf16.txt
```

Search these text files in your editor. On Kali, `file work/evidence.img` is available (Kali row 49). A suffix such as `.dmp` does not distinguish full physical memory from a single-process minidump; inspect the signature before selecting a parser.

## Partition offsets and targeted recovery

**Use when:** the input is a raw disk or partition image. Sleuth Kit avoids mounting and journal replay. Run these in **WSL** (Windows row 30).

```bash
mmls work/evidence.img
```

Read the units printed above the table. Set `START` to the filesystem's start sector, not its byte offset. `SECTOR` is the image's sector size; 512 is an example, not a universal value. A partition-only image generally uses `START=0`.

```bash
START=2048
SECTOR=512
fsstat -b "$SECTOR" -o "$START" work/evidence.img > out/fsstat.txt
fls -b "$SECTOR" -o "$START" -r -p work/evidence.img > out/files.txt
fls -b "$SECTOR" -o "$START" -r -d -p work/evidence.img > out/deleted.txt
```

Choose an address printed by `fls`; `42` below is a placeholder. NTFS addresses can include attribute type and ID, for example `66-128-4`.

```bash
ADDR=42
istat -b "$SECTOR" -o "$START" work/evidence.img "$ADDR" > out/inode.txt
icat -b "$SECTOR" -o "$START" work/evidence.img "$ADDR" > out/recovered.bin
xxd -l 64 out/recovered.bin
```

Expected result: recovered bytes match the file's format and declared length. For a deleted FAT file, the directory entry may survive while the FAT cluster chain has been cleared. Contiguous recovery can work; fragmented recovery may require carving or extent reconstruction. A deleted name is not a promise that its contents survive.

If `fsstat` rejects the image, check offset units, sector size, compression/container format, and filesystem support before assuming corruption. `fls` puts a colon after every address; searching for `:` alone does **not** reliably identify alternate streams.

## Missing partitions, carving, and virtual disks

**Kali** (rows 150, 51, 122, 41):

```bash
testdisk /log work/evidence.img
photorec /log /d out/carved work/evidence.img
foremost -i work/evidence.img -o out/foremost
qemu-img info --backing-chain disk.vmdk
qemu-img convert -f vmdk -O raw disk.vmdk out/disk.raw
ewfinfo disk.E01
```

In TestDisk, use **Analyse**, then **Quick Search** and file listing/copying. Do not select **Write** on the evidence. Carve into a separate output directory. File carving loses original paths, timestamps, and often fragmented data; it complements filesystem recovery.

For VMDK, provide all split extents and backing snapshots in their expected relative paths. Converting only a delta file without its parent gives incomplete or incorrect results. OVA is a tar container; on Kali use `tar -tf machine.ova` before extracting selected members. A VM snapshot can contain separate `.vmem` and state files; retain both, and try the supported memory parser before assuming a converter is available.

Sparse VMDK fallback: read the header's sector-based grain size, grain-directory offset, and entries-per-table. A directory entry points to a grain table; a table entry points to a physical grain. Translate virtual sector to grain index and in-grain offset; zero entries represent unallocated grains. Do not concatenate sparse extents as if they were raw sectors.

## A reusable extent and byte-transform extractor

**WSL Python standard library.** Save as `carve.py`. Use when a verified filesystem record or format header gives a byte offset and length. This handles large inputs without loading the whole disk.

```python
import argparse
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('image')
p.add_argument('output')
p.add_argument('offset', type=lambda x: int(x, 0))
p.add_argument('length', type=lambda x: int(x, 0))
p.add_argument('--stride', type=int, default=1)
p.add_argument('--phase', type=int, default=0)
a = p.parse_args()
assert a.offset >= 0 and a.length >= 0
assert a.stride > 0 and 0 <= a.phase < a.stride
assert a.offset + a.length <= Path(a.image).stat().st_size
with open(a.image, 'rb') as src, open(a.output, 'xb') as dst:
    src.seek(a.offset)
    remaining, consumed = a.length, 0
    while remaining:
        block = src.read(min(1024 * 1024, remaining))
        if not block:
            raise EOFError('short read')
        first = (a.phase - consumed) % a.stride
        dst.write(block[first::a.stride])
        remaining -= len(block)
        consumed += len(block)
```

```bash
python3 carve.py work/evidence.img out/extent.bin 0x400000 0x10000
python3 carve.py out/extent.bin out/even.bin 0 65536 --stride 2 --phase 0
python3 carve.py out/extent.bin out/odd.bin 0 65536 --stride 2 --phase 1
```

Null interleaving often makes every second byte zero and doubles the apparent size. Check both phases and validate the result with a parser. For fragmented files, extract each verified extent in **logical file order**, insert sparse holes where specified, and trim to the recorded file size.

XFS extent fields are packed and include allocation-group addressing: a filesystem block value cannot always be multiplied directly by block size without decoding the AG component. HFS+ resource forks have their own extents and logical size; examine both forks. ISO 9660 directory records contain extent LBA and data length; the usual logical block size is 2048, but read the volume descriptor. These are parsing workflows, not permission to install missing filesystem tools.

## Archives: list, test, then recover

**Kali:** `7z` row 9, `tar` row 148, `unzip` row 155, `bkcrack` row 20, John row 80. **WSL:** Python row 14 and xz row 32.

```bash
7z l archive.zip
7z t archive.zip
tar -tvf archive.tar.xz
unzip -l document.docx
```

OOXML documents are ZIPs: inspect `word/media/`, `xl/worksheets/`, embedded objects, and relationships. Do not enable macros. For repeated tar names, standard extraction overwrites earlier versions. This **WSL** script preserves each regular-file occurrence under a generated name, so archive paths cannot overwrite your workspace:

```python
import tarfile
from pathlib import Path

out = Path('out/tar-members')
out.mkdir(parents=True, exist_ok=True)
total = 0
with tarfile.open('archive.tar.xz') as tf:
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
```

For nested archives, record each layer's input/output hash and stop when the format no longer matches. Limit depth and output size. A `.model` beside many compressed files can indicate dictionary compression such as FemtoZip; the dictionary is required and the original source's installer is not event-approved. Preserve the model and inspect supplied decompressor source rather than guessing a normal ZIP decoder.

ZIP repair must respect both local headers and central-directory records. Local filename length is at header `+26`; central-directory filename length at `+28`. Verify filename and extra-field boundaries before changing a copy. Bit 3 means sizes may appear in a later data descriptor, so a generic local-header parser cannot trust zero size fields. CRC32 and uncompressed size should match after recovery.

For an XZ file whose 12-byte header alone is damaged, the last footer can supply stream flags. **WSL**, save as `repair_xz.py`:

```python
from pathlib import Path
import struct, zlib

d = bytearray(Path('broken.xz').read_bytes())
assert len(d) >= 24 and d[-2:] == b'YZ'
footer = d[-12:]
assert zlib.crc32(footer[4:10]) == int.from_bytes(footer[:4], 'little')
flags = bytes(footer[8:10])
d[:12] = b'\xfd7zXZ\0' + flags + struct.pack('<I', zlib.crc32(flags))
Path('out/repaired.xz').write_bytes(d)
```

```bash
python3 repair_xz.py
xz -t out/repaired.xz
xz -dc out/repaired.xz > out/decompressed.bin
```

This assumes one stream with no trailing stream padding; account for padding or concatenated streams first. A valid footer does not prove the body is intact.

ZipCrypto known-plaintext attack, **Kali**, with an unencrypted reference ZIP containing the same compressed member:

```bash
bkcrack -C secret.zip -c report.txt -P known.zip -p report.txt
```

It needs at least 12 known plaintext bytes, including 8 contiguous bytes, at the encryption layer. For a compressed member, a file's uncompressed PNG magic alone is not enough. This does not apply to WinZip AES.

Replace `K0 K1 K2` with the three hexadecimal keys printed by the successful attack. Create a separate archive with a chosen local password, test it, then extract into a new directory. This assumes its members share the recovered original password. The `-U` operation is documented in the [official bkcrack usage](https://github.com/kimci86/bkcrack#change-password).

```bash
bkcrack -C secret.zip -k K0 K1 K2 -U out/unlocked.zip RecoveredOnly
7z t out/unlocked.zip -pRecoveredOnly
7z x out/unlocked.zip -pRecoveredOnly -oout/unlocked
```

If the original password was recovered independently, skip key recovery and use `7z t secret.zip` followed by `7z x secret.zip -oout/unlocked`; enter that password at the prompt. A CRC failure after unlocking suggests wrong plaintext alignment, a different member password, or damaged archive data.

## Memory: establish what the dump supports

**WSL Volatility 3**, Windows row 38:

```bash
vol --help
vol --offline -f memory.dmp windows.info
vol --offline -f memory.dmp windows.pslist
vol --offline -f memory.dmp windows.pstree
vol --offline -f memory.dmp windows.cmdline
vol --offline -f memory.dmp windows.netscan
vol --offline -f memory.dmp windows.filescan > out/filescan.txt
```

Use the installed plugin names printed by help; names can be versioned. `--offline` prevents automatic symbol retrieval. The symbol ZIP bundles are explicitly unavailable (**Unapproved row 82**). Existing matching symbols may or may not be present. An unsatisfied symbol requirement is an environment limitation, not proof the dump is empty. Keep the diagnostic and pivot to raw bytes or supported supplied profiles.

Choose a PID and address from the results; these values are examples:

```bash
PID=1234
PHYS=0x12345000
vol --offline -f memory.dmp -o out windows.memmap --pid "$PID" --dump
vol --offline -f memory.dmp -o out windows.dumpfiles --physaddr "$PHYS"
vol --offline -f memory.dmp windows.mftscan
```

Search recovered process bytes in ASCII and UTF-16LE. A process dump can be a virtual-address mapping, not a complete runnable executable. Match suspicious parentage, command line, network endpoints, and mapped regions before selecting a process.

**Kali Volatility 2** (rows 158–160) is a separate path for matching legacy profiles. Use `python2 /opt/tools/volatility/vol.py --info` to inspect available profiles/plugins. Run `imageinfo`, then validate the proposed profile using plausible process names and timestamps. `clipboard`, `consoles`, and `mftparser` are legacy plugin routes; do not translate their flags directly into Volatility 3 commands.

```bash
python2 /opt/tools/volatility/vol.py -f memory.raw imageinfo
PROFILE=Win7SP1x64
python2 /opt/tools/volatility/vol.py -f memory.raw --profile="$PROFILE" pslist
python2 /opt/tools/volatility/vol.py -f memory.raw --profile="$PROFILE" clipboard
python2 /opt/tools/volatility/vol.py -f memory.raw --profile="$PROFILE" consoles
python2 /opt/tools/volatility/vol.py -f memory.raw --profile="$PROFILE" mftparser > out/mft-memory.txt
```

`Win7SP1x64` is an example, not a default to force on every dump. Use a compatible profile that the installation actually lists. Empty clipboard output may mean unavailable pages or an unsupported OS artifact; it does not prove nothing was copied.

For an ELF core, **WSL GDB** (Windows row 16):

```bash
gdb -nx -nh -c core.dump
```

```text
info files
info proc mappings
info registers
x/32gx $sp
find 0x400000, 0x410000, "flag{"
dump binary memory out/region.bin 0x400000 0x410000
quit
```

Replace both addresses with a mapped region from this core. A universal 32-bit search range misses 64-bit heaps. GDB opens the core for analysis; do not run a recovered executable to inspect its strings.

## Keys, framebuffers, and unusual memory remnants

For ransomware, identify the cipher, key length, IV location, padding, and file layout from the recovered program. An AES key may remain near path strings or a configuration structure. Restrict candidates to those regions and test against **two independent known file signatures**. A successful authentication tag is much stronger evidence than printable plaintext. A timestamp-derived key search must reproduce the exact PRNG implementation and seed units; Python's random generator is not interchangeable with C, Ruby, or .NET PRNGs.

Full-disk encryption keys may appear as expanded AES schedules, but the source's key-finder and volume-mounting tools are not listed. Do not modify encryption headers or add passwords to evidence. Record key candidates and use only a supported approved decoder for the challenge format.

For possible screen remnants, render a bounded region as pixels. **WSL**, Pillow is a non-AI library under Windows row 14:

```python
from PIL import Image

offset, width, height = 0x100000, 1024, 256  # set from evidence/hypothesis
with open('memory.dmp', 'rb') as f:
    f.seek(offset)
    raw = f.read(width * height * 4)
assert len(raw) == width * height * 4
Image.frombytes('RGB', (width, height), raw, 'raw', 'BGRX').save('out/screen.png')
```

Try documented RGB/BGR/BGRA layouts and row stride; recognizable fragments can be partial or stale. In a minidump, file offsets differ from process virtual addresses. Parse its memory descriptors before translating an address into a file slice.

## Windows artifact timeline

**Windows native**, built-in PowerShell, on an exported EVTX file:

```powershell
Get-WinEvent -Path .\Security.evtx -Oldest |
  Where-Object { $_.Id -in 1102,4624,4688,4720,4726,4781 } |
  Select-Object TimeCreated,Id,ProviderName,Message |
  Export-Csv -NoTypeInformation -Encoding UTF8 .\out\security.csv
```

Missing message resources can produce blank descriptions. Export `ToXml()` to retain named event fields and UTC `SystemTime`. Event IDs are provider-specific: Security 1102 is audit clearing; 4720 account creation; 4781 account rename. RDP authentication event 1149 belongs to RemoteConnectionManager; LocalSessionManager 21/24/25 describe logon/disconnect/reconnect. Authentication success alone does not prove an interactive desktop was used.

Zimmerman tools are approved on **Windows row 46**. From their installed directory:

```powershell
.\MFTECmd.exe -f 'C:\case\$MFT' --csv C:\case\out
.\PECmd.exe -d C:\case\Prefetch --csv C:\case\out
.\AmcacheParser.exe -f C:\case\Amcache.hve --csv C:\case\out
.\EvtxECmd.exe -f C:\case\Security.evtx --csv C:\case\out
```

Replace `C:\case` with your evidence-copy directory. Confirm each executable's help if a version changes output flags. Amcache indicates file inventory/presence and may support an activity timeline; it is not by itself proof of execution. Prefetch run times require context. `$MFT` does not record the name of the process that created a file.

| Artifact | What to inspect | Next correlation |
|---|---|---|
| `$MFT` | Resident data, names, SI/FN timestamp differences | USN, logs, file contents |
| `$Extend\$UsnJrnl:$J` | Create/delete/rename/data-extension reasons | MFT reference + sequence number |
| `$Recycle.Bin\SID` | Pair `$I` metadata with matching `$R` content | Original path and deletion time |
| `NTUSER.DAT` | Run keys, MRU, user application settings | Process and file evidence |
| `SYSTEM` + `SAM` | Computer config, user/RID records | Account events; challenge hash task |
| `ConsoleHost_history.txt` | Typed PowerShell command text | Script-block/process events |
| Defender `Support\MPLog-*` | Detection, quarantine, ASR activity | DetectionHistory and file hashes |
| WMI `Repository\OBJECTS.DATA` | Consumer commands and filter/binding strings | WMI and process events |

USN writes can be coalesced; they do not assign an exact execution timestamp to each history line. Registry last-write time is a key modification time, not always account creation. SI/FN disagreement suggests a question to investigate, not automatic proof of timestomping. `EFSTMPWP` can indicate a free-space wipe attempt; it does not prove every free cluster was overwritten.

For ADS on an extracted NTFS file, **Windows native**:

```powershell
Get-Item -LiteralPath .\suspect.txt -Stream *
Get-Content -LiteralPath .\suspect.txt -Stream Zone.Identifier
```

For image-level ADS, examine `istat`'s named `$DATA` attributes and extract the complete `inode-type-id` address with `icat`. Copying a file to a filesystem without ADS support may discard the extra streams.

**Kali** SAM hash extraction (Impacket row 75), only from challenge-provided hives:

```bash
impacket-secretsdump -sam SAM -system SYSTEM LOCAL > out/sam-hashes.txt
```

This is offline extraction. Do not reuse recovered credentials against services outside the challenge.

## Browser, SQLite, Android, and Linux evidence

Work on a copied database alongside its `-wal` and `-shm` files. The WAL may hold the newest or deleted material. Opening only the main database can miss it. **Kali SQLite**, row 138:

```bash
sqlite3 -readonly History '.tables'
sqlite3 -readonly History '.schema urls'
sqlite3 -readonly History "SELECT url,title,datetime(last_visit_time/1000000-11644473600,'unixepoch') FROM urls ORDER BY last_visit_time;"
sqlite3 -readonly places.sqlite "SELECT url,title,datetime(last_visit_date/1000000,'unixepoch') FROM moz_places ORDER BY last_visit_date;"
```

Chrome uses microseconds since 1601; Firefox places uses microseconds since 1970. Schema differs by browser version. Password ciphertext is not decryptable merely because `Local State` exists: older `v10/v11` AES-GCM records require the actual master key; newer app-bound formats need their own supported recovery route. Verify authentication tags.

For supplied Android app directories, inspect `shared_prefs/*.xml`, `databases/*`, and backups before APK reversal. ALEAPP/iLEAPP are listed on Kali rows 11/73 but have no recorded installation information: do not promise they run. On Linux, correlate exported `auth.log`, shell history, service logs, cron definitions, and binaries. Shell history may lack timestamps or omit noninteractive commands.

SQLite edit-history tables can retain text removed later. After inspecting the actual schema, replay operations and inspect every intermediate state:

```python
import sqlite3
db = sqlite3.connect('file:notes.db?mode=ro', uri=True)
text = ''
for ident, op, pos, value in db.execute(
        'SELECT id,type,position,text FROM diffs ORDER BY id'):
    assert isinstance(pos, int) and 0 <= pos <= len(text)
    if op == 'insert':
        text = text[:pos] + value + text[pos:]
    elif op == 'remove':
        assert text[pos:pos + len(value)] == value
        text = text[:pos] + text[pos + len(value):]
    else:
        raise ValueError(op)
    if 'flag{' in text.lower():
        print(ident, repr(text))
```

Positions might be UTF-16 code units or bytes instead of Python characters; use the application's convention. For raw SQLite differences, decode record-header varints: serial types 0–9 have special meanings; even types ≥12 are blobs of `(type-12)/2` bytes, odd types ≥13 are text of `(type-13)/2` bytes. Changed type bytes can change interpretation without changing the visible payload.

## Git and container history

**Kali Git**, row 56, on a supplied local repository:

```bash
git -C recovered log --all --format=fuller --stat
git -C recovered reflog --all
git -C recovered fsck --full --unreachable --no-reflogs
git -C recovered show COMMIT:path/to/file
```

Replace `COMMIT` with an object ID printed by the earlier commands. `git log --all` excludes dangling commits; inspect the IDs from `fsck` explicitly. Recover deleted `.git/objects/xx/...` files with `icat` first and preserve their paths. Do not run garbage collection. For a corrupted loose object, decompress zlib and hash the full `type size\0content` record; matching the expected object ID validates a single-byte repair. If the repository uses SHA-256, do not assume SHA-1.

For a Docker save archive, inspect `manifest.json`, its config's `history`, and every layer tar in order. OCI archives instead use `index.json` and content-addressed descriptors. Whiteouts (`.wh.name`, `.wh..wh..opq`) remove earlier content from the final view but leave earlier layer bytes recoverable. Build history is useful but does not necessarily retain every command or secret after squashing/metadata changes. The tar extraction script above works without starting containers.

## Advanced filesystem cases: know the limits

| Pattern | Usable local approach | Validation and limitation |
|---|---|---|
| GPT GUID payload | Read LBA size and GPT header; entry-array LBA at `+72`, count `+80`, entry size `+84`; concatenate unique-GUID bytes at entry `+16` | Check header/table CRCs; GUID text representation changes byte order |
| FAT free space | Derive cluster size, rounded root-directory sectors, and data start from BPB; read clusters whose FAT entry is zero | Bound by data-region cluster count; preserve physical offsets instead of silently joining fragments |
| RAID 5 missing member | XOR corresponding bytes from all surviving aligned members | Equal sizes/offsets required; recovered member is not the logical array; stripe order and parity rotation still matter |
| APFS/Btrfs/ZFS snapshots | Identify historical roots and transaction/generation IDs; compare same file across roots | Installed TSK support varies; raw `APSB` hits are candidates, not valid snapshot proof |
| Damaged ZFS metadata | Preserve copies of labels/nvlists; validate block pointers and checksums before reconstruction | Fletcher4 uses 64-bit accumulators over 32-bit input words; source's 32-bit version was wrong |
| Kyoto Cabinet key damage | Record table slots/value offsets; reproduce the documented hash mapping with candidate keys | First binary difference is often a header/counter, not the target slot; no approved manager assumed |
| BSON chunk documents | Validate each 32-bit LE document length and trailing NUL; decode with non-AI `pymongo` in WSL | Sort by explicit chunk index, reject gaps/duplicates, then base64-decode |
| KeePass | Identify KDBX version/KDF, inspect installed John's extractor support | Never label all KDBX4/Argon2 material as a single hashcat mode |

For aligned equal-size RAID members, this **WSL** script creates the missing physical member in bounded chunks:

```python
from pathlib import Path
assert Path('disk1.img').stat().st_size == Path('disk3.img').stat().st_size
with open('disk1.img','rb') as a, open('disk3.img','rb') as b, open('out/disk2.img','xb') as out:
    while x := a.read(1024 * 1024):
        y = b.read(len(x))
        assert len(x) == len(y)
        out.write(bytes(i ^ j for i, j in zip(x, y)))
```

Do not create a live RAID array or run repair tools on the evidence. Filesystem repairs can overwrite the very orphaned records you want. Use supported read-only extraction, then a separate expendable copy if a justified repair path is available.

## Finish with a reproducible result

Record the input hash, partition/stream offset, inode or process ID, exact command, output hash, and the evidence supporting the answer. Keep observations separate from interpretations. A copied flag-shaped string can be a decoy; verify its relationship to the challenge question.

Source material adapted: `ctf-forensics/SKILL.md`, `disk-and-memory.md`, `disk-advanced.md`, `disk-recovery.md`, `linux-forensics.md`, and `windows.md` within `ctf-forensics/`. Network, media, and malware overlaps continue in the neighboring chapters. Historical installers, cloud CLI enumeration, unsupported snapshot mounters, and collision-generator recipes were removed from the competition workflow.


---

<a id="04-network"></a>

# Network captures and hardware signals

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


---

<a id="05-steganography"></a>

# Steganography, documents, and media

Treat each file as a container before treating it as pixels or sound. Read metadata, inspect structural boundaries, enumerate frames/tracks, then test a specific hiding hypothesis. Keep every recovered layer and its extraction settings.

## Tools and execution environment

| Environment | Approved tools | Workbook rows |
|---|---|---|
| Windows native | HxD, PDF viewer | Windows 42, 10 |
| Windows WSL | Python 3, strings, zsteg, binwalk, ExifTool, pdftotext, ZBar, qpdf, xxd | Windows 14, 18–22, 26, 33, 35 |
| Kali | Audacity, FFmpeg, ImageMagick, pngcheck, SoX, Sonic Visualiser, steghide, stegseek, stegsnow, StegSolve | Kali 17, 47, 74, 115, 136, 135, 141–144 |

Python examples run in **WSL**; Pillow, NumPy, SciPy, and other non-AI libraries fall under Windows row 14. Check availability before choosing a recipe; do not install a toolkit wholesale. Python permission does not override the explicit unapproved list. In particular, do not use ML classifiers, unapproved DCT-Image-Steganography, sigBits, or magiceye-solver (Unapproved rows 17, 75, 42).

Keep decoding local. Online image/barcode readers and public analysis uploads are not a substitute for missing tools under the [event rules](https://ajccbc.ncsa.or.th/cyber-sea-game-2026/).

## First five minutes

`carrier.png` is the supplied file; change the filename but preserve the original. **WSL:**

```bash
exiftool -a -u -g1 carrier.png
xxd -l 256 carrier.png
strings -a -n 6 carrier.png
binwalk carrier.png
zsteg -a carrier.png
```

Expected result: a metadata clue, embedded-format offset, or candidate bit layout. Binwalk signatures and zsteg readable fragments are leads, not proof. Validate extracted bytes using their file format. `binwalk -e` may invoke external helpers; prefer targeted carving with the Python extractor in the forensics chapter rather than relying on unlisted helper programs.

For a JPEG, inspect the first few hundred bytes even if ExifTool reports nothing. A passphrase may be raw text in an unusual segment. Extract the thumbnail in **WSL**:

```bash
exiftool -b -ThumbnailImage carrier.jpg > thumbnail.jpg
```

An empty output means the tag is absent. View original and thumbnail at full resolution. Small text, selection masks, and different crops can be the intended clue.

For a suspected steghide carrier, **Kali** rows 141–142:

```bash
steghide info carrier.jpg
steghide extract -sf carrier.jpg -xf recovered.bin
stegseek carrier.jpg challenge-words.txt recovered-from-wordlist.bin
```

Enter a clue-derived password at the steghide prompt; an empty password is a reasonable single test if the clue gives none. `challenge-words.txt` is a small local list built from evidence. A failed password does not prove absence of embedded data. Inspect the extracted format and contents before continuing to another layer.

## PNG chunks, trailers, and safe repairs

**Kali**: `pngcheck -v carrier.png` reports chunk order, CRC failures, and dimensions. The following **WSL Python** script walks actual chunk boundaries; it does not mistake an `IEND` byte string inside compressed data for the file's end. Save as `png_chunks.py` and run `python3 png_chunks.py carrier.png`.

```python
import sys, struct, zlib
from pathlib import Path

d = Path(sys.argv[1]).read_bytes()
assert d[:8] == b'\x89PNG\r\n\x1a\n', 'bad PNG signature'
out = Path('png-parts')
out.mkdir(exist_ok=True)
pos, index = 8, 0
while pos + 12 <= len(d):
    size = struct.unpack_from('>I', d, pos)[0]
    kind = d[pos+4:pos+8]
    end = pos + 12 + size
    assert end <= len(d), 'chunk extends beyond file'
    body = d[pos+8:pos+8+size]
    stored = struct.unpack_from('>I', d, pos+8+size)[0]
    valid = zlib.crc32(kind + body) == stored
    print(hex(pos), kind, size, 'CRC OK' if valid else 'BAD CRC')
    (out / f'{index:03d}-{kind.hex()}.bin').write_bytes(body)
    index += 1
    pos = end
    if kind == b'IEND':
        assert size == 0
        (out / 'trailer.bin').write_bytes(d[pos:])
        print('trailing bytes:', len(d)-pos)
        break
else:
    raise ValueError('no complete IEND')
```

Check `tEXt`, `iTXt`, `zTXt`, unknown chunks, unused palette data, and bytes after IEND. If an archive signature is overwritten, repair only a copy after verifying the rest of its header. For chunk-case corruption, change the **chunk type field**, then recompute its CRC over type+data. Global byte replacement can corrupt an IDAT stream.

IHDR must be first, IEND last, and IDAT chunks consecutive. PLTE/tRNS and other ancillary chunks have specific ordering requirements: do not move every ancillary chunk before IDAT indiscriminately. Preserve IDAT ordering unless a separate clue defines a permutation.

If only the IHDR height is damaged and the old CRC remains, search a bounded height range. **WSL:**

```python
from pathlib import Path
import struct, zlib
d = bytearray(Path('broken.png').read_bytes())
assert d[12:16] == b'IHDR' and int.from_bytes(d[8:12],'big') == 13
target = int.from_bytes(d[29:33], 'big')
for height in range(1, 8193):
    trial = d[12:20] + struct.pack('>I', height) + d[24:29]
    if zlib.crc32(trial) == target:
        d[20:24] = struct.pack('>I', height)
        Path('height-fixed.png').write_bytes(d)
        print('matching height:', height)
        break
else:
    print('no match: wrong hypothesis, range, or damaged CRC')
```

After repair, verify decoding and expected decompressed scanline length. A matching CRC is not permission to claim arbitrary new rows exist.

## Bitplanes and packed messages

Use when a lossless image looks normal but a hint points to low bits, colors, or parity. **WSL**, save as `planes.py`:

```python
from pathlib import Path
from PIL import Image
import numpy as np

im = np.array(Image.open('carrier.png').convert('RGB'))
out = Path('planes'); out.mkdir(exist_ok=True)
for channel, name in enumerate('RGB'):
    for bit in range(8):
        plane = ((im[:,:,channel] >> bit) & 1).astype('uint8')
        Image.fromarray(plane * 255).save(out / f'{name}{bit}.png')
        for order in ('big','little'):
            (out / f'{name}{bit}-{order}.bin').write_bytes(
                np.packbits(plane.ravel(), bitorder=order).tobytes())
parity = (im.astype('uint16').sum(axis=2) & 1).astype('uint8')
Image.fromarray(parity * 255).save(out / 'rgb-parity.png')
bits = np.stack([(im[:,:,0]>>0)&1, (im[:,:,1]>>1)&1,
                 (im[:,:,2]>>2)&1], axis=-1).ravel()
(out / 'R0-G1-B2.bin').write_bytes(np.packbits(bits).tobytes())
```

```bash
python3 planes.py
zbarimg -q planes/G1.png
zsteg -E 'b1,r,lsb,xy' carrier.png > extracted.bin
```

The zsteg selector is an example; copy the exact promising selector printed by its analysis. Expected output is structured text or a valid file, not merely a short printable run. If nothing works, try row/column order, reversed traversal, bit polarity, RGB/BGR order, or a clue-defined carrier subset. Avoid recompressing to JPEG before extracting low bits.

Conditional carriers: with NumPy, select `im[np.all(im <= 1, axis=2)]` for near-black pixels and pack the chosen channel bits in their original order. Do not remove all zero-valued pixels automatically; zeros may encode valid data.

For a clockwise binary border, avoid reading the corner pixels twice:

```python
from PIL import Image
im = Image.open('carrier.png').convert('RGB')
w,h = im.size
coords = ([(x,0) for x in range(w)] + [(w-1,y) for y in range(1,h)] +
          [(x,h-1) for x in range(w-2,-1,-1)] + [(0,y) for y in range(h-2,0,-1)])
bits = [int(sum(im.getpixel(p)) >= 384) for p in coords]
data = bytes(sum(b << (7-j) for j,b in enumerate(bits[i:i+8]))
             for i in range(0,len(bits)-7,8))
print(repr(data))
```

Use thresholding only for visibly black/white carriers. Lossy images may need a measured threshold; color LSB extraction from JPEG-decoded pixels is usually unstable.

## Palettes, quantization tables, and pixel paths

Unused PNG palette entries can hold bytes without affecting visible pixels. **WSL:**

```python
from PIL import Image
from pathlib import Path
im = Image.open('carrier.png')
assert im.mode == 'P', 'not a palette image'
palette = im.getpalette()
used = set(im.getdata())
unused = [i for i in range(len(palette)//3) if i not in used]
for c,name in enumerate('RGB'):
    data = bytes(palette[3*i+c] for i in unused)
    Path(f'unused-{name}.bin').write_bytes(data)
    print(name, repr(data))
```

For JPEG DQT, `Image.open('carrier.jpg').quantization` exposes tables. Examine which table IDs the frame components reference before calling any table “unused”; IDs ≥2 are not automatically unused. Pillow exposes table order differently from raw JPEG zigzag storage, so test the format-defined order if a packed bitstream is scrambled. Re-saving a JPEG can remove or rewrite these tables.

F5-like embedding changes quantized AC coefficient statistics. Compare a suspect to matched clean images at the same encoder/quality, exclude DC coefficients by their **block positions**, and examine counts near zero. There is no universal ±1/±2 threshold that proves F5. Use this as triage; the unapproved named DCT toolkit is not an extraction route.

For JPEG block slack, inspect frame dimensions and sampling factors: MCU dimensions depend on chroma subsampling and can exceed 8×8. Ordinary resizing does not reveal encoded padding. If justified, alter dimensions in a copy within the existing MCU grid, retain compressed coefficients, and validate decoder output; ImageMagick's decode-size hint is not a general uncrop operation.

For a clue-defined pixel chain, **WSL**:

```python
from PIL import Image
im = Image.open('carrier.png').convert('RGB')
x,y = 0,0  # starting coordinate from the clue
seen, out = set(), bytearray()
while (x,y) not in seen:
    if not (0 <= x < im.width and 0 <= y < im.height):
        raise ValueError('next coordinate outside image')
    seen.add((x,y))
    value,nx,ny = im.getpixel((x,y))
    if value == 0: break
    out.append(value)
    x,y = nx,ny
print(repr(out))
```

For seeded permutations, reproduce the exact generator, shuffle algorithm, seed, traversal order, and channel conversion. NumPy `RandomState` and `default_rng` produce different permutations. Extract multiple bitplanes in the order specified by the encoder, then test the result's framing/checksum.

## QR reconstruction and geometric transforms

Use **WSL ZBar** (Windows row 26) to decode locally. Start with finder patterns in three corners, alternating timing lines, and module count `21 + 4*(version-1)`. Add a four-module quiet zone. Do not smooth module boundaries.

For a manually transcribed grid, save equal-width lines of `0` and `1` in `qr.txt`, where `1` means dark:

```python
from pathlib import Path
from PIL import Image, ImageOps
rows = Path('qr.txt').read_text().splitlines()
n = len(rows)
assert n >= 21 and all(len(r) == n and set(r) <= {'0','1'} for r in rows)
im = Image.new('L',(n,n),255)
im.putdata([0 if c=='1' else 255 for r in rows for c in r])
im = ImageOps.expand(im,border=4,fill=255)
im.resize((im.width*12,im.height*12),Image.Resampling.NEAREST).save('qr.png')
```

```bash
zbarimg -q qr.png
```

If decoding fails, check mirror/rotation, grid size, quiet zone, and damaged format bits. Error-correction percentages refer to recoverable codewords under specific conditions, not a guarantee that an arbitrary percentage of the image can be erased. For curved reflections, pick the sharpest frame, correct mirroring, estimate grid intersections, and record uncertain modules instead of inventing a flag prefix.

For colored QR carriers with few exact colors, enumerate binary assignments to those colors and scan each candidate. Six colors means 64 assignments. Do not enumerate millions of JPEG-noise colors; first justify a palette from the image. Multiple valid results can carry different messages.

Jigsaw pieces: score adjacent borders with the sum of absolute pixel differences after converting to signed integers. Anchor known corners/finder patterns and require each piece once. Greedy placement can trap the search; retain several best placements and backtrack when seams disagree. A 4×4 brute-force permutation search is far too large to recommend blindly.

Nearest-neighbor carriers: sample each grid phase, `array[y_offset::step, x_offset::step]`, and inspect the resulting low-resolution image. A chained resize can select different source pixels from a single direct resize; reproduce the entire size sequence if given.

For Arnold's cat map on a square image, iterate this **WSL** transform until the state repeats or a defined limit is reached:

```python
from PIL import Image
import numpy as np
a = np.array(Image.open('scrambled.png').convert('RGB'))
n = len(a); assert a.shape[1] == n
y,x = np.indices((n,n))
start = a.copy()
for step in range(1, 1001):
    b = np.empty_like(a)
    b[(x+y)%n,(2*x+y)%n] = a
    Image.fromarray(b).save(f'cat-{step:04d}.png')
    a = b
    if np.array_equal(a,start): break
```

Map orientation is a hypothesis; use the challenge's matrix if provided. The period depends on the matrix and dimensions, not a universal multiple of the image size.

For an autostereogram, compute `abs(image[:,shift:] - image[:,:-shift])` in signed arithmetic over a small range of repeat widths. Structured contours suggest a useful shift. This is ordinary image processing; no unapproved magic-eye tool or learned classifier is needed.

For a frequency-domain image clue, render a **grayscale** 2-D FFT magnitude in WSL. Applying `fft2` to an RGB array without specifying axes can accidentally transform a color axis.

```python
from PIL import Image
import numpy as np
a=np.asarray(Image.open('carrier.png').convert('L'),dtype=float)
spectrum=np.log1p(np.abs(np.fft.fftshift(np.fft.fft2(a))))
span=np.ptp(spectrum)
assert span>0,'constant spectrum'
view=np.rint((spectrum-spectrum.min())/span*255).astype('uint8')
Image.fromarray(view).save('fft-magnitude.png')
```

Measure any rings/peak grids before sampling bits; choose radii, angular order, and threshold from the image, not the historical challenge's constants. Fourier symmetry may duplicate rather than add message bits.

If equal plaintext pixels were replaced with equal ciphertext tokens, preserve token equality and render each distinct token as a different color to reveal shapes. A 256-entry hash-to-pixel lookup works only for a known **unkeyed hash** of single-byte grayscale values; it does not decrypt arbitrary keyed AES. For Angecryption clues, use the supplied/recovered cipher/key/IV and test full format validity in both directions; two valid images alone do not prove a relationship.

## PDF, SVG, and office documents

**WSL** tools, Windows rows 21, 22, 33:

```bash
exiftool -a -u -g1 document.pdf
pdftotext -layout document.pdf document.txt
qpdf --check document.pdf
qpdf --show-xref document.pdf
qpdf --qdf --object-streams=disable document.pdf expanded.pdf
qpdf --show-object=12 --filtered-stream-data document.pdf > object12.bin
```

Replace object `12` with an observed stream object. Inspect text extraction, metadata, link URI annotations, attachments, page contents, and incremental revisions. Keep the original: rewriting a PDF can discard unreferenced objects or normalize a covert xref channel. A black rectangle may overlay readable content; real redaction may remove it entirely.

**Kali** Didier Stevens Suite (row 37):

```bash
python3 /opt/tools/DidierStevensSuite/pdfid.py document.pdf
python3 /opt/tools/DidierStevensSuite/pdf-parser.py --stats document.pdf
python3 /opt/tools/DidierStevensSuite/pdf-parser.py --object 12 --filter --dump object12.bin document.pdf
```

A hidden page must be a valid Page object with content/resources; arbitrarily adding a content-stream number to `/Kids` is not sufficient. Inspect page-tree reachability and inherited resources before repairing a copy. For rectangle-based QR drawings, parse `re` coordinates from a decompressed content stream, account for transformation matrices, and map centers onto a measured module grid.

For classic textual xref entries, inspect generation numbers before qpdf rewrites them. Nonzero generations are legitimate after object reuse; treat unusual patterned values as a hypothesis. Match an actual `xref` section, not the substring inside `startxref`. Xref streams need their `/W` field widths and filters decoded first.

For SVG, read it as XML/text before opening active content. Inspect `<animate>` values/keyTimes, extremely small coordinate clusters, hidden groups, and transforms. To reveal micro-coordinate art, change a **copy's** `viewBox` to the small observed coordinate range. Animation timing can encode Morse; use actual key-time differences and duration.

For XLSX numeric carriers, export cells to CSV using approved Kali LibreOffice (row 88), keeping row/column order. Reimplement any macro's arithmetic without enabling it. Frequency-ranked values are only a hypothesis: tied frequencies make ordering ambiguous. Check all candidate mappings against file signatures rather than assuming 256 distinct values imply a correct byte map.

## Text, terminal, and archive channels

View suspicious terminal captures as bytes before displaying their escape sequences. ANSI can move the cursor and overwrite text; stripping CSI codes recovers underlying text but does not simulate the final screen.

**WSL**, inspect invisible characters without normalizing them away:

```python
from pathlib import Path
import re, unicodedata
s = Path('art.txt').read_text(encoding='utf-8')
for i,c in enumerate(s):
    if ord(c) < 32 or ord(c) > 126:
        print(i, f'U+{ord(c):04X}', unicodedata.name(c,'CONTROL'))
clean = re.sub(r'\x1b\[[0-?]*[ -/]*[@-~]', '', s)
print(repr(clean))
bits = ''.join('0' if c==' ' else '1' for c in s if c in ' \t')
print(bytes(int(bits[i:i+8],2) for i in range(0,len(bits)-7,8)))
```

Only treat spaces/tabs as a bitstream if the challenge supports that interpretation. Preserve line endings and trailing spaces. **Kali** `stegsnow -C carrier.txt` handles SNOW's specific whitespace encoding (row 143); arbitrary whitespace is not automatically SNOW.

Kitty graphics begins with `ESC _ G` and ends with `ESC \`. Parse command headers, group chunks by image/transfer ID, and join base64 payloads until `m=0`. Respect `f=24` RGB versus `f=32` RGBA, dimensions `s`/`v`, and optional zlib compression `o=z`; PNG format `f=100` is already an encoded image. Validate decoded byte length before rendering. Joining every Kitty sequence can merge different images incorrectly.

For interleaved files, save `data[0::2]` and `data[1::2]`, identify both, then inspect alternating scanlines if the decoded images are striped. Try full byte reversal only when the other end has a meaningful reversed header. Nested PNG XOR carriers need per-layer keys and chunk CRC validation, not one global key. GZSteg/SpamMimic-specific external decoders from the source are not available defaults; inspect supplied encoder code and retain the unmodified gzip stream for any format-level investigation.

## Audio: hear, inspect, and preserve samples

**Kali** FFmpeg row 47, SoX row 136, multimon-ng row 98:

```bash
ffprobe -hide_banner recording.mkv
ffmpeg -i recording.mkv -map 0:a:0 -c:a pcm_s16le track0.wav
ffmpeg -i recording.mkv -map 0:a:1 -c:a pcm_s16le track1.wav
sox track0.wav reversed.wav reverse
sox track0.wav -n spectrogram -o spectrogram.png
sox track0.wav -t raw -r 22050 -e signed-integer -b 16 -c 1 - | multimon-ng -t raw -a DTMF -
```

`0:a:1` means the second audio stream; only use it if ffprobe lists one. Converted WAV is useful for listening but **not** an exact substitute for original PCM when testing LSB data. Spectrogram window size trades time resolution against frequency resolution; inspect both full-band and a suspected band in Sonic Visualiser (Kali row 135).

Standard DTMF uses row frequencies 697/770/852/941 Hz and columns 1209/1336/1477/1633 Hz. For custom tones, split into measured symbol windows, apply a Hann window, and select one peak from each observed frequency group. A note sequence must be decoded in time order; sorting all frequencies alphabetically destroys the message. Musical note number is `round(69 + 12*log2(f/440))`, but a harmonic peak may not be the fundamental.

For MIDI files, parse events rather than rendered audio. With WSL non-AI `mido`, iterate each track's events in order, retain channel and delta-time, and distinguish Note Off from Note On with velocity zero. If the challenge deliberately alternates pairs with different pitches, test sum, XOR, or high/low-nibble combination. Do not pair two independently collected pitch lists when overlaps, channels, or unmatched notes exist.

For two almost-identical aligned tracks, subtract sample values in a wider datatype. Sample-rate mismatch, gain differences, or a one-sample delay can swamp the hidden difference. **WSL**, on original 16-bit PCM WAVs:

```python
import wave
import numpy as np
with wave.open('track0.wav','rb') as f:
    params = f.getparams(); raw0 = f.readframes(f.getnframes())
with wave.open('track1.wav','rb') as f:
    assert f.getparams() == params
    raw1 = f.readframes(f.getnframes())
assert params.sampwidth == 2
a = np.frombuffer(raw0,dtype='<i2').astype('int32')
b = np.frombuffer(raw1,dtype='<i2').astype('int32')
delta = a-b
peak = max(1,int(np.max(np.abs(delta))))
pcm = np.rint(delta * (30000/peak)).astype('<i2')
with wave.open('difference.wav','wb') as f:
    f.setparams(params); f.writeframes(pcm.tobytes())
```

Generate a spectrogram of `difference.wav`. Normalization is for viewing/listening after subtraction; preserve the raw difference if it carries exact numeric data.

For sample LSB extraction, **WSL**, original 16-bit PCM only:

```python
import wave
from pathlib import Path
import numpy as np
with wave.open('original.wav','rb') as f:
    assert f.getsampwidth()==2 and f.getcomptype()=='NONE'
    channels = f.getnchannels()
    a = np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').reshape(-1,channels)
for ch in range(channels):
    for depth in (1,2):
        bits = np.stack([(a[:,ch] >> bit) & 1 for bit in range(depth)],axis=1).ravel()
        Path(f'audio-ch{ch}-lsb{depth}.bin').write_bytes(np.packbits(bits).tobytes())
```

The bit order within each sample is a hypothesis; try its reverse if warranted. For eight-bit PCM, use unsigned samples. Inspect channel-interleaved and separate-channel layouts deliberately.

## SSTV, analog image lines, and signal caveats

**Kali row 140** calls its tool `sstv` but records installation as `pip (PySSTV)`. PySSTV is commonly an encoder package; that row does **not** prove a working decoder exists. Inspect the installed command/help before promising a decode. MMSSTV and RX-SSTV are unapproved (rows 46/69); do not replace a missing decoder with a public upload service.

A high sample rate alone does not make standard SSTV invalid. Determine actual tone frequencies, VIS/mode, sync timing, scan order, and channel durations from the signal. If a custom signal is FM-modulated, a usable **WSL SciPy/NumPy** diagnostic is instantaneous frequency from analytic phase:

```python
import numpy as np
from scipy.io import wavfile
from scipy.signal import hilbert
rate,x = wavfile.read('signal.wav')
assert x.ndim == 1, 'select the intended channel first'
x = x.astype(float)
x -= x.mean()
phase = np.unwrap(np.angle(hilbert(x)))
frequency = np.diff(phase) * rate / (2*np.pi)
np.save('instantaneous-frequency.npy',frequency)
```

Band-limit around the known carrier before phase estimation if needed. Edge transients and low-amplitude intervals are unreliable. Map frequency to intensity only after recovering sync and mode-specific line/channel boundaries. A derivative of `arccos(samples)` loses phase direction and is not a general FM decoder.

For Voyager-style amplitude images, detect separated sync pulses, measure consecutive line intervals, resample each interval to equal width, normalize globally, then try orientation/transposition. Validate against any supplied calibration image. For RF `.sub` files, `RAW_Data` normally contains signed pulse durations; cluster pulse/gap widths according to the protocol rather than discarding bytes ≥128 as “noise.”

DeepSound-like WAVs: the approved John jumbo installation may include `deepsound2john.py`; inspect its help and use it to confirm a format-specific hash before cracking. A recovered password is not an extraction implementation. DeepSound GUI is not separately approved; use a supplied encoder/format description or a permitted local non-AI implementation, and validate output length/checksums.

## Video, animation, and temporal channels

**Kali FFmpeg:**

```bash
ffprobe -hide_banner clip.mp4
mkdir frames
ffmpeg -i clip.mp4 -map 0:v:0 -fps_mode passthrough frames/frame-%06d.png
ffmpeg -i clip.mp4 -map 0:v:1 -frames:v 1 second-stream.png
```

Select `0:v:1` only if a second video stream exists. Frame extraction is for pixel analysis; it can discard hidden container padding or metadata. Keep original bytes for MJPEG post-EOI analysis and JPEG XL TOC investigation.

**WSL**, frame average, bright-pixel accumulation, and first/last difference:

```python
from pathlib import Path
from PIL import Image, ImageOps
import numpy as np
files = sorted(Path('frames').glob('*.png'))
assert files
first = np.array(Image.open(files[0]).convert('L'),dtype=float)
total, maximum, last = first.copy(), first.copy(), first
for p in files[1:]:
    last = np.array(Image.open(p).convert('L'),dtype=float)
    assert last.shape == first.shape
    total += last
    maximum = np.maximum(maximum,last)
average = Image.fromarray(np.rint(total/len(files)).astype('uint8'))
ImageOps.autocontrast(average).save('average.png')
Image.fromarray(maximum.astype('uint8')).save('maximum.png')
Image.fromarray(np.abs(last-first).astype('uint8')).save('difference.png')
```

If dark marks on a white background carry data, use per-pixel minimum instead of maximum. For consecutive-frame bit channels, compare lossless decoded frames, distinguish exact `+1` from all other changes, and retain unchanged carrier positions. Lossy compression can destroy such a channel.

GIF/APNG frames need disposal/blending semantics. Pillow's `ImageSequence.Iterator` can export displayed frames; it may convert palette modes. If the channel is in **raw GIF local color tables**, parse the original GIF table blocks; re-encoding frames to PNG is not guaranteed to preserve palette bytes. A huge number of one-pixel frames may encode a square bitmap in colors, but verify the count and ordering before reshaping.

For blinking LEDs, crop a small stable region, compute brightness per frame, threshold into on/off states, then run-length encode using actual frame timestamps. Estimate dots/dashes/gaps from the duration clusters, and include the final run. Do not assume fixed frame rate from the container alone.

For MJPEG, inspect the container's frame boundaries and JPEG markers; preserve bytes after each true EOI before the next frame. Naively splitting at every `FFD8` can encounter thumbnails or unrelated bytes. For JPEG XL progressive ordering, a full decode hides the order channel. The source's `djxl` is not listed: if the approved ImageMagick build supports JXL, inspect its format support and whether partial decodes are usable; otherwise retain TOC analysis as a format-reading task, without installing a missing decoder. Do not reuse a stale output image after a failed partial decode.

## Printing, punched cards, and optical media

Binary G-code starts `GCDE`; read version and checksum type before walking blocks. Each block has type, compression, lengths, and type-specific fields. A checksum is not always an unconditional four bytes. Heatshrink parameters and G-code text encodings depend on the format version; a decompressed block can still need decoding. WSL non-AI `heatshrink2` is permitted by Windows row 14 when needed, but validate output against declared length. `qoif` thumbnails contain big-endian width/height and RGB/RGBA channel metadata.

For **plain G-code with absolute XYZ/extrusion**, save this **WSL** projection as `gcode.svg`. It tracks modal coordinates and draws only increasing-extrusion moves. It rejects relative-coordinate modes instead of silently rendering them incorrectly.

```python
from pathlib import Path
import re
state = dict(X=0.,Y=0.,Z=0.,E=0.)
segments = []
for line in Path('print.gcode').read_text().splitlines():
    line = line.split(';',1)[0].strip()
    if not line: continue
    command = line.split()[0]
    if command in ('G91','M83'):
        raise ValueError('relative mode: extend parser before proceeding')
    values = {k:float(v) for k,v in re.findall(r'([XYZE])\s*(-?\d+(?:\.\d+)?)',line)}
    previous = state.copy()
    if command in ('G0','G1','G92'): state.update(values)
    if command == 'G1' and state['E'] > previous['E']:
        segments.append((previous['X'],previous['Z'],state['X'],state['Z']))
assert segments
xs = [s[i] for s in segments for i in (0,2)]
zs = [s[i] for s in segments for i in (1,3)]
x0,z0 = min(xs)-1,min(zs)-1
w,h = max(xs)-x0+1,max(zs)-z0+1
body = ''.join(f'<line x1="{a}" y1="{-b}" x2="{c}" y2="{-d}"/>' for a,b,c,d in segments)
Path('gcode.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0} {-z0-h} {w} {h}"><g stroke="black" stroke-width="0.1">{body}</g></svg>')
```

Switch projection to XY/YZ or restrict Y ranges when side lettering overlaps. Arc moves G2/G3 need interpolation; the script intentionally handles only G0/G1/G92.

Punched cards: calibrate the 80-column ×12-row grid, label rows `12,11,0,1,…,9`, and record hole combinations per column. Map digit single-punches and zone+digit letters using the supplied code chart; row 12 alone is not “A.” Contrast, perspective, and punctuation variants need manual verification.

CDDA with only two dominant byte values can encode a disc image rather than normal audio. A specialized encoder may pre-interleave bytes to compensate for CIRC; this is not a general raw-audio decoder. Use the supplied calibration pair to establish the 24-byte channel permutation/delays, then render polar rings with increasing bytes-per-revolution. Tune initial circumference and radial increment against calibration before decoding the unknown file. Preserve sample order; assuming every `.cdda` uses one historical tool's constants produces plausible but wrong images.

## Statistical traces without AI

For power traces, determine axes from the challenge data description. Average repeated measurements, inspect per-sample variance, and compare hypotheses using an explicit leakage model. “Largest power is the correct digit” is only valid for a challenge whose implementation has that behavior. Report stability across separate trace subsets rather than one maximum.

For keyboard audio, manually segment keypress transients, compare waveform/spectral shapes to supplied labeled references, and corroborate uncertain positions with context. The source's KNN/scikit-learn route is excluded by the AI/ML restriction. Do not replace it with another learned classifier under a different name.

Source material adapted: `ctf-forensics/steganography.md`, `stego-image.md`, `stego-advanced.md`, `stego-advanced-2.md`, `3d-printing.md`, and media portions of `signals-and-hardware.md`/`SKILL.md`. Unsupported online decoders, blanket installers, genetic/ML solvers, and sample-specific assumptions were removed or replaced with bounded local workflows.


---

<a id="06-reverse-engineering"></a>

# Reverse engineering: turn a program into a checkable explanation

Your first deliverable is a sentence such as “the program XORs each input byte with a repeating key, rotates it, and compares the result with this table.” Once that sentence is accurate, writing a solver is usually straightforward. A decompiler's output is a hypothesis; the bytes and a repeatable run are the evidence.

This chapter is for human, local analysis of supplied challenge files. The event prohibits AI assistance and public online analysis, decompilation, and compilation services. Use the handbook as preparation or as an offline reference only where the event permits it. Do not upload binaries to a comparison site. Work only on the challenge targets assigned to your team.

## 1. Choose the correct machine before choosing a command

The workbook describes two separate environments. A tool listed under Windows with installation location WSL is not a Windows executable and is not automatically available in Kali.

| Route | Approved tools relevant here | Practical use |
| --- | --- | --- |
| **Windows native** | x64dbg (Windows row 40), HxD (42), Notepad++ (44), dnSpyEx (45) | PE debugging, byte inspection, managed .NET analysis |
| **Windows WSL** | Python 3 (14), GDB (16), objdump (17), strings (18), Ghidra (29), llvm-mc (34), xxd (35) | ELF analysis, local decompilation, small scripts |
| **Kali** | radare2 (123), Frida (53), angr (13), GCC/build tools (54), ltrace (90), strace (145), UPX (156), jadx (79), Apktool (15) | ELF triage, instrumentation, APK extraction, local practice builds |
| **Kali, specialized** | GoReSym (62), pycdc (117), pyinstxtractor-ng (118), uncompyle6 (152), unpyc3 (153), Cutter (31), BinDiff (19) | Language and packaging specific follow-up |

Kali tools were installed on a best-effort basis; operation is not guaranteed. Python 3.11's Kali row 121 records no installation information. Check the interpreter actually present before running a Python example. Windows WSL Python is the reliable workbook-backed route for the standard-library scripts below.

**Windows native, PowerShell: enter the supplied WSL distribution.**

```powershell
wsl --list --verbose
wsl
```

**Windows WSL, Bash: check the listed tools without installing anything.**

```bash
command -v python3 gdb objdump strings xxd
python3 --version
gdb --version
```

**Kali, Bash: check the separate tool set.**

```bash
command -v r2 rabin2 python3 frida strace ltrace gcc
r2 -v
python3 --version
```

If a command is missing, use a listed alternative or the other supplied environment. Do not run the source repository's blanket installation commands. Windows row 14 permits additional non-AI Python libraries; that is permission to add a library, not evidence it is already installed, and does not approve unrelated standalone software. This chapter's core route needs no additional Python package.

IDA Free and Binary Ninja Free are in the unapproved sheet. MCP servers and AI plugins are out of scope. WinDbg, Scylla/x64dbg plugins, de4dot, online decompilers, and online analysis services are also excluded by the workbook. The approved x64dbg application does not imply approval of every extension.

## 2. Preserve the file and identify its format

Use `chall` below for a local challenge file placed in your working directory. Keep the original untouched; make a separate copy before patching. Record its hash, format, architecture, input channel, and your first observed output.

**Windows native, PowerShell:**

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath .\chall
Copy-Item -LiteralPath .\chall -Destination .\chall.work
Format-Hex -Path .\chall
```

**Windows WSL, Python standard library:**

```bash
python3 - <<'PY'
from pathlib import Path
import hashlib
p = Path('chall')
data = p.read_bytes()
print('size:', len(data))
print('sha256:', hashlib.sha256(data).hexdigest())
print('first 32 bytes:', data[:32].hex(' '))
PY
```

Interpret the header before running it: `7f 45 4c 46` is ELF; `4d 5a` begins a DOS/PE family file; `00 61 73 6d` is WebAssembly; ZIP containers start with `50 4b` and may be APK, JAR, HAP, or an ordinary archive. A file extension alone proves none of these. An `MZ` stub may itself contain the challenge, so do not automatically discard it.

**Windows WSL:**

```bash
objdump -f chall
objdump -x chall > headers.txt
strings -a -t x chall > strings.txt
python3 - <<'PY'
from pathlib import Path
for line in Path('strings.txt').read_text(errors='replace').splitlines():
    if any(word in line.lower() for word in ('flag', 'correct', 'wrong', 'password', 'usage')):
        print(line)
PY
```

**Kali:**

```bash
file chall
rabin2 -I chall
rabin2 -S chall
rabin2 -zz chall > strings.txt
rg -in 'flag|correct|wrong|password|usage' strings.txt
```

Save full output; a filtered display is an index into it. No matching string means only that this search found none. Packed data, wide strings, runtime decoding, and a different flag format can all hide a useful string. `rabin2 -zz` reports physical and virtual addresses: a file offset is not a runtime address.

| Observation | Next action | Why |
| --- | --- | --- |
| Plaintext candidate flag | Find references and test the candidate against the original | A decoy string is cheap to plant |
| `strcmp`/`memcmp` imported | Find callers, then stop before the relevant call | Comparison arguments may reveal the actual check |
| Few imports and high-entropy sections | Inspect entry point, memory allocation and writes | A loader may create the real code at runtime |
| ELF sections rejected but program headers sensible | Inspect load segments; analyze a repaired copy only | The loader uses segments; corrupt sections can mislead tools |
| Native architecture does not match the host | Continue statically | A foreign ELF cannot run merely because it is executable |
| .NET metadata / CLR header | Open in native dnSpyEx | Managed methods are more informative than native startup stubs |

## 3. A complete small checker to practice on

This local toy accepts four bytes on standard input. It gives you a known reference for practicing strings, cross-references, decompilation, and comparison breakpoints. Save as `checker.c` using an approved editor.

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    unsigned char input[32] = {0};
    const unsigned char key[] = {0x31, 0x72};
    const unsigned char expected[] = {0x61, 0x3f, 0x72, 0x3f};
    unsigned char out[4];
    if (!fgets((char *)input, sizeof input, stdin)) return 2;
    size_t n = strcspn((char *)input, "\r\n");
    if (n != 4) { puts("wrong length"); return 1; }
    for (size_t i = 0; i < 4; i++)
        out[i] = (unsigned char)((input[i] ^ key[i % 2]) + i);
    if (memcmp(out, expected, 4) == 0) puts("correct");
    else puts("wrong");
    return 0;
}
```

**Kali, approved GCC; local practice only:**

```bash
gcc -O0 -g -fno-builtin -o checker checker.c
printf 'AAAA\n' | ./checker
printf 'PLAN\n' | ./checker
```

Expected output is `wrong`, then `correct`. This compiler command is not asserted available in Windows WSL. A compiled Linux file may be inspected statically there; execution also requires a compatible loader and libc.

**Windows WSL Python, or Kali with Python confirmed:**

```bash
python3 - <<'PY'
key = bytes([0x31, 0x72])
expected = bytes([0x61, 0x3f, 0x72, 0x3f])
answer = bytes(((b - i) & 0xff) ^ key[i % len(key)]
               for i, b in enumerate(expected))
reencoded = bytes(((b ^ key[i % len(key)]) + i) & 0xff
                  for i, b in enumerate(answer))
assert reencoded == expected
print(answer.decode('ascii'))
PY
```

The output is `PLAN`. Subtraction must happen before XOR because the checker applies XOR before addition. The round-trip assertion tests the inversion, while running the original checks the input length, newline handling, and surrounding logic.

## 4. Follow a check with radare2 on Kali

The following is an interactive **Kali radare2** session. `checker` is the toy above; for a real target, substitute its filename and use the names or addresses actually printed by the tool.

```text
r2 checker
aaa
iI
ii
izz~correct
afl
pdf @ main
```

`aaa` performs analysis; `afl` lists recognized functions; `pdf` disassembles a function. Find the call to `memcmp` and the conditional branch after it. `test eax,eax` followed by a zero/nonzero branch commonly checks a C comparison result. Follow both destinations and identify which prints `correct`. The presence of one apparent success branch does not establish that it is the final check.

**Kali radare2, continue in the same session:**

```text
axt @ sym.imp.memcmp
pdf @ main
agf @ main
q
```

`axt` lists incoming references; `agf` shows a function graph. If your imported name differs, copy its exact flag from `ii`. If `main` is absent, use `ie` for entry points, `afl` for candidates, and inspect the startup routine's call target. A stripped executable has fewer names, not less machine code.

For a string reference, copy the **virtual address** from `izz`, then use `axt @ ADDRESS`, replacing `ADDRESS` with that number. Use `pdf @ FUNCTION` for the containing function. The placeholder is deliberately not a universal address.

**Kali, save reusable static output:**

```bash
r2 -q -c 'aaa;aflj' checker > functions.json
r2 -q -c 'aaa;pdf @ main' checker > main.asm
r2 -q -c 'izzj' checker > strings.json
```

Do not add `-d` for static work: it starts a debug process. `-w` opens a writable file and is unnecessary for inspection. If analysis is wrong, inspect bytes with `px 32 @ ADDRESS`, disassemble a bounded region with `pd 12 @ ADDRESS`, and correct function boundaries only after checking where execution actually enters. Command meanings are documented in the [official radare2 reference card](https://book.rada.re/refcard/intro.html).

For JSON, check the decoded value's type and length. A failed command can produce an empty value rather than the list you expected. A `json.loads` error may mean diagnostic output polluted stdout, not that the binary has no functions. The optional `r2pipe` library is not individually listed; batch output above needs no plugin.

## 5. Read decompiled code without trusting invented types

**Windows WSL Ghidra:** launch the supplied Ghidra application, create a local non-shared project, import `chall`, and check the detected language, bitness, endianness, and image base before accepting analysis. Open **Search → For Strings**, select a relevant message, and follow its references into the function. Keep Listing and Decompiler panes visible together.

Rename `local_28` to a factual name such as `input_buffer` only after you have identified its use. Rename an unknown function to `candidate_transform` before claiming it is AES. Set array lengths from actual bounds, distinguish a byte count from an element count, and check signed comparisons in the assembly. Save your project separately from the original file.

| Decompiled appearance | Verify in instructions |
| --- | --- |
| `char` becomes negative | `movsx` sign-extends; `movzx` zero-extends |
| Arithmetic looks unbounded | Register width and truncation at each store |
| `memcmp` arguments appear missing | Calling convention, register assignments before the call, function prototype |
| Impossible branch | Flags, unsigned versus signed jump, or earlier mutation |
| Huge single function | Flattened dispatcher, bad boundaries, exception flow, or VM interpreter |
| No ordinary calls | Tail jumps, return chains, callbacks, destructors, signal handlers |

Ghidra in the Windows sheet is installed **in WSL**. Its presence there does not establish a Kali installation. Kali's approved radare2 provides the static fallback. `pdg` requires an r2ghidra plugin; radare2 approval alone is not proof that plugin exists. Use `pdf` if it is absent instead of installing it during the event.

## 6. Stop immediately before the comparison

**Windows WSL GDB, Linux x86-64 checker:**

```bash
gdb -q ./checker
```

```text
set disassembly-flavor intel
break main
run
disassemble /r main
break memcmp
continue
```

Enter `AAAA` when the program asks for input. At the relevant `memcmp` call, inspect arguments:

```text
info registers rdi rsi rdx rip
x/4bx $rdi
x/4bx $rsi
bt
```

On Linux x86-64 System V, these registers hold the first pointer, second pointer, and length. For this toy the second buffer should be `61 3f 72 3f` and the length 4. Those bytes are **transformed expected data**, not automatically the plaintext answer. Check the call site if other library calls also hit the breakpoint.

On Windows x64, the first arguments are RCX, RDX, R8, R9. On i386 cdecl they are on the stack; immediately before `call`, argument one is at `[esp]`, and at callee entry it is at `[esp+4]`. On ARM A32 use r0–r3; AArch64 uses x0–x7. Register assumptions must match the ABI, not just the CPU family.

For PIE, first `start` or `starti`, inspect `info proc mappings`, and derive the runtime address from the loaded image plus the correct relative offset. With symbols, `break *main+OFFSET` is convenient; replace `OFFSET` with an instruction offset from this binary. Never copy a raw address from an earlier run with ASLR enabled. The [GDB manual](https://sourceware.org/gdb/current/onlinedocs/gdb) documents breakpoints, memory inspection, and process mappings.

**Windows WSL GDB, useful follow-up commands:**

```text
nexti
stepi
finish
info registers
x/16i $pc
x/32bx $sp
```

`nexti` steps over a call; `stepi` enters it; `finish` runs until the current frame returns. If you need to discover who changes a known byte, set `watch *(unsigned char*)ADDRESS` after replacing `ADDRESS` with the live pointer. Watchpoints are limited resources; watch the meaningful field rather than an entire megabyte.

**Windows native x64dbg:** open a copy of the PE using the matching x32dbg or x64dbg executable, follow the entry point, and find the local comparison or imported comparison routine from the Symbols view. Set a breakpoint, run to it, and inspect the ABI argument registers in Dump. Use a hardware breakpoint on a changed byte when a software `INT3` breakpoint would modify self-checked code. Do not assume hardware breakpoints are invisible to the program.

## 7. When tracing reveals more than decompilation

**Kali, only for a local executable you intend to run:**

```bash
ltrace -s 256 -o library.log ./chall
strace -f -s 256 -o syscalls.log ./chall
rg -n 'strcmp|memcmp|open|read|write|ptrace|mprotect|execve' library.log syscalls.log
```

`ltrace` can expose imported function arguments; static linking, inlining, direct syscalls, or custom routines can hide them. `strace` shows kernel interactions, including child processes with `-f`. Neither tool proves that a missing call never occurred through another implementation. A file-open failure can reveal the expected working directory or companion filename.

**Kali Frida:** use this observation-only script when the binary imports `memcmp`. Save it as `compare.js`.

```javascript
const address = Module.findGlobalExportByName('memcmp');
if (address === null) {
  console.log('memcmp is not exported in this process');
} else {
  Interceptor.attach(address, {
    onEnter(args) {
      const length = args[2].toUInt32();
      if (length === 0 || length > 128) return;
      try {
        console.log('length=' + length);
        console.log(hexdump(args[0], { length: length, ansi: false }));
        console.log(hexdump(args[1], { length: length, ansi: false }));
      } catch (error) {
        console.log('unreadable comparison: ' + error);
      }
    }
  });
}
```

```bash
frida -f ./chall -l compare.js
```

Enter the challenge input through the terminal as appropriate for the supplied Frida CLI. Check `frida --help` if its process/input behavior differs. If the library loads later, attach after it is mapped or observe module loading; do not silently accept “no export” as “no comparison.” The script uses the current API spelling from [Frida's JavaScript documentation](https://frida.re/docs/javascript-api/).

## 8. Write down the transform before solving it

Use a table with one row per stage: source bytes, operation, width, key/state, destination. Keep the exact comparison direction: `transform(input) == stored` requires inversion, while `input == transform(stored)` requires forward evaluation.

**Windows WSL Python; Kali after interpreter check:**

```python
def rol8(value, amount):
    amount %= 8
    return ((value << amount) | (value >> ((8 - amount) % 8))) & 0xff

def ror8(value, amount):
    return rol8(value, -amount)

for value in range(256):
    for amount in range(8):
        assert ror8(rol8(value, amount), amount) == value
print('all byte rotations round-trip')
```

For XOR, applying the same key again reverses it. For addition modulo 256, subtract and mask. Reverse a permutation with the inverse index map. For a stateful cipher, restore the complete state before testing the next candidate; reusing mutated state creates plausible-looking wrong output. A non-bijective substitution can have several preimages: retain all candidates until later constraints eliminate them.

A repeated prefix hash can permit byte-by-byte search if each prefix digest is independently known. A single full cryptographic hash generally does not. A branch count or timing oracle must first show a consistent relationship to correct prefixes, with repeated baselines and randomized candidate order. Avoid treating the slowest single run as proof.

### Mixed Boolean-arithmetic expressions

Expressions such as `(x ^ y) + 2*(x & y)` implement `x+y` at a fixed width. Simplifying them can reveal an ordinary checksum hidden in a large expression. Record the width and signedness, simplify one expression, then compare original and replacement on boundary values and many random inputs. Random agreement is a useful check, not a mathematical proof of equivalence. For small widths, exhaustive checking is stronger.

**Windows WSL Python, complete 8-bit check:**

```python
for x in range(256):
    for y in range(256):
        original = ((x ^ y) + 2 * (x & y)) & 255
        replacement = (x + y) & 255
        assert original == replacement
print('equivalent for all 8-bit pairs')
```

The source's msynth/Miasm workflow is a specialized option, not a required installed tool. The manual identity and equivalence check survive without it. Solver-backed synthesis, deobfuscation plugins, and an oracle database each have separate availability requirements.

## 9. Anti-analysis: preserve the real semantics

Start by comparing one normal run with one instrumented run using the same input. Locate the first meaningful divergence. Patching every conditional jump can make a validator print success without recovering the answer.

| Evidence | Human investigation | Common wrong conclusion |
| --- | --- | --- |
| `ptrace`, `TracerPid`, PEB flags | Identify the exact return value or branch consumed | All anti-debugging is a single imported function |
| Time or instruction-counter state | Determine whether time changes the key or merely gates progress | Skipping a delay preserves cryptographic state |
| SIGILL/SIGFPE/SIGTRAP handlers | Trace handler and saved context changes | The first signal is an ordinary crash |
| Parent and child processes | Follow both and inspect writes between them | The child on disk contains its final instructions |
| Writes to executable pages | Dump after decoding, before erasure | A static disassembly describes every later instruction |
| TLS callbacks / constructors / destructors | Analyze startup and teardown too | All validation occurs under `main` |
| Stack-based call-less chaining | Follow saved frame and return pointers | No `call` instruction means no function dispatch |

**Windows WSL GDB, only after proving a handler is intended:**

```text
info signals SIGILL SIGFPE SIGTRAP
handle SIGILL nostop noprint pass
handle SIGFPE nostop noprint pass
set follow-fork-mode child
set detach-on-fork off
info inferiors
```

Do not broadly pass SIGTRAP without understanding debugger breakpoints. Signal-driven code may mutate instructions, adjust the saved PC, or switch decoding modes. For a parent that writes the child's text with `process_vm_writev`, Kali `strace -f` can expose the mechanism; exact dumped bytes may require a larger recorded string limit and careful parsing.

Dump a measured interval in GDB with `dump binary memory decoded.bin START END`, replacing both addresses with mapped runtime bounds. Record the base address alongside the dump. Reimporting at address zero loses pointer relationships. Integrity checks can detect patches and software breakpoints; emulation or observing after the check may preserve more behavior than editing code.

## 10. Custom VMs and emulation

A VM is an interpreter plus a bytecode program. Recover its state before naming every opcode: program counter, registers or operand stack, memory, flags, and input/output operations. Find the dispatch loop, log one instruction's before/after state, and build a table of operand lengths and effects. Compare two runs differing in one input byte to locate the first dependent bytecode region.

**Windows WSL Python; complete tiny VM with no extra libraries:**

```python
# Opcodes: 1=load immediate, 2=XOR immediate, 3=add immediate, 4=emit, 255=halt.
program = bytes([1, 0x61, 2, 0x31, 3, 0, 4,
                 1, 0x3d, 2, 0x71, 3, 0, 4, 255])
pc, accumulator = 0, 0
output = bytearray()
steps = 0
while pc < len(program):
    steps += 1
    if steps > 100: raise RuntimeError('instruction budget exhausted')
    at = pc
    opcode = program[pc]
    pc += 1
    if opcode == 255:
        break
    if opcode in (1, 2, 3):
        if pc >= len(program): raise ValueError('truncated operand')
        operand = program[pc]
        pc += 1
        if opcode == 1: accumulator = operand
        elif opcode == 2: accumulator ^= operand
        else: accumulator = (accumulator + operand) & 255
    elif opcode == 4:
        output.append(accumulator)
    else:
        raise ValueError(f'unknown opcode {opcode} at {at}')
    print(f'pc={at:02x} op={opcode:02x} a={accumulator:02x}')
assert bytes(output) == b'PL'
print(output.decode())
```

The final output is `PL`. A real VM may use variable-length instructions, encoded opcodes, channels between threads, or self-modifying bytecode. Keep program memory writable in the model when STORE can alter instructions. For concurrent interpreters, record message ordering and blocking conditions; arbitrary round-robin scheduling is not automatically equivalent.

| Model | Choose it when | State you must supply |
| --- | --- | --- |
| Small Python interpreter | Only a handful of VM instructions matter | Exact opcode semantics and integer widths |
| radare2 ESIL, Kali | A supported short native routine can be isolated | Registers, stack, memory, stop condition; verify instruction coverage |
| Unicorn, conditional non-AI library | Raw foreign CPU code is the obstacle | Mapped pages, architecture/mode, registers, memory and syscall/MMIO stubs |
| Qiling, conditional non-AI library | OS calls and filesystem behavior matter | Compatible root filesystem and accurate API behavior |
| angr, Kali approved row 13 | Input constraints lead to a small set of branches | Input model, success/failure conditions, bounds and realistic environment |

Unicorn/Qiling are not individually listed as preinstalled. Their library status does not supply missing firmware, OS images, or separate emulators. `qemu-img` approval covers disk-image tooling; it does not establish approval or installation of every `qemu-system-*` or `qemu-user-*` executable.

For Unicorn, map page-aligned code and stack, use a finite instruction budget, and stop at the function's return boundary. An invalid fetch usually means a bad PC or return address; an invalid read/write often means missing data, incorrect ABI arguments, or wrong pointer width. Do not “fix” every fault by mapping zero pages: that can conceal an incorrect model.

Snapshotting registers alone does not reset memory. Restore dirty pages and peripheral state between candidates. ARM Thumb needs the correct execution mode; MIPS needs endianness and delay-slot semantics; mixed x86 modes require compatible register and memory transfer. CPU emulation does not implement operating-system syscalls. MMIO reads need meaningful device behavior, such as a changing ready bit, rather than arbitrary constants.

## 11. Symbolic execution as a bounded experiment

Use symbolic execution after you know the checker's input shape. Avoid launching unconstrained exploration over an entire GUI or runtime. A solver model reaching a success address is a candidate input; replay it through the original file before accepting it.

**Kali, approved angr environment, with its Python import confirmed:**

```bash
python3 -c 'import angr, claripy; print(angr.__version__)'
```

A failed import can mean angr lives in an isolated pipx environment. Use the interpreter provided with that environment rather than assuming system Python shares its packages. If it cannot be located, continue with the byte-transform solver above.

Save as `solve_checker.py`; this is specific to the complete `checker.c` example, including its four-byte input and messages.

```python
import angr
import claripy

project = angr.Project('./checker', auto_load_libs=False)
characters = [claripy.BVS(f'c{i}', 8) for i in range(4)]
content = claripy.Concat(*characters, claripy.BVV(b'\n'))
stream = angr.SimFileStream(name='stdin', content=content, has_end=True)
state = project.factory.full_init_state(args=['./checker'], stdin=stream)
for character in characters:
    state.solver.add(character >= 0x20, character <= 0x7e)
manager = project.factory.simulation_manager(state)
manager.explore(find=lambda s: b'correct\n' in s.posix.dumps(1),
                avoid=lambda s: b'wrong' in s.posix.dumps(1), n=1000)
if not manager.found:
    raise SystemExit('No solution within this exploration budget; inspect states')
answer = manager.found[0].solver.eval(claripy.Concat(*characters), cast_to=bytes)
print(answer.decode('ascii'))
```

Expected candidate: `PLAN`. `n=1000` bounds exploration rounds, not wall-clock runtime; interrupt a stalled run rather than letting it consume the session. If a target reads argv, models a file, or requires more input, change the model accordingly. Hooks must preserve the behavior relevant to the check; replacing a hash with a success constant makes a false solver. File and stream modeling are covered in the [angr filesystem documentation](https://api.angr.io/en/v9.2.112/advanced-topics/file_system.html).

## 12. Language and platform routes

| Target | Approved starting route | What to recover before solving |
| --- | --- | --- |
| Python `.pyc` | Kali pycdc/uncompyle6/unpyc3; WSL matching Python `dis` when available | Interpreter version, constants, nested code objects, opcode mapping |
| PyInstaller | Kali pyinstxtractor-ng | Embedded archive, Python version, actual application module |
| .NET | Windows native dnSpyEx | Entry method, resources, initializer, decryptor, comparison |
| APK/DEX | Kali jadx and Apktool | Java/Kotlin entry flow, resources, native methods, ABI-specific `.so` |
| Electron | Kali approved `asar` utility | `app.asar`, main/preload scripts, native addon boundary |
| Go | Kali GoReSym; radare2 or WSL Ghidra | Runtime versus user functions, string pointer/length pairs, goroutines |
| Rust | WSL Ghidra or Kali radare2 | Slice lengths, enum tags, panic paths, JSON field names |
| Swift/Kotlin/C++ | WSL Ghidra; Kali jadx for JVM bytecode | Witness tables, coroutine state, vtables/RTTI, destructors |
| WASM / exotic bytecode | Local bytes, strings, small interpreter | Linear memory, imports, instruction encoding, host interaction |
| Godot/Roblox/Unity | Inspect supplied assets and scripts first | Resource container, script format, engine/native boundary |
| Firmware / drivers | Kali radare2; WSL Ghidra, binwalk where appropriate | Architecture, load address, entry point, device interfaces |

These are investigation routes, not claims that every specialized decompiler is installed. Flutter/IL2CPP, HarmonyOS ABC, Pyarmor, macOS/iOS, SGX, and proprietary game formats may require tooling absent from the approved list. Preserve the structural reasoning; use approved static tools and challenge-provided resources, or defer that route.

**Kali APK, static extraction:**

```bash
jadx -d jadx-out challenge.apk
apktool d challenge.apk -o apk-out
rg -n 'native |loadLibrary|RegisterNatives|flag|secret|check' jadx-out apk-out
```

When Java calls `native check(...)`, locate the corresponding `lib/<abi>/*.so`. Dynamic registration maps method names and signatures to native function pointers. Android `.so` files may depend on bionic, JNI objects, initialization, and ARM instructions; loading one into desktop Linux with `ctypes.CDLL` is not a general substitute for an Android runtime. Certificates, assets, or logged values can be key material; reproduce exact hashing and byte encodings.

**Kali UPX, work on a copy:**

```bash
cp chall chall.work
upx -t chall.work
upx -d chall.work
rabin2 -I chall.work
```

Failure can mean unsupported UPX, a modified header, or no UPX at all. It is not a reason to patch magic bytes blindly. For a custom packer, identify the decoding loop and inspect memory after it runs.

## 13. Recognize the less common patterns

| Pattern in the source collection | Useful observation and next step |
| --- | --- |
| Multi-layer decryptor / RC4 gate plus VM | Solve and dump one layer at a time; feed the original verified output into the next layer |
| S-box/SPN constants / GF(2^8) elimination | Extract tables exactly; XOR is addition in the field, and multiplication needs the observed reduction polynomial |
| Sliding-window popcount | Adjacent count differences constrain the leaving/entering bits; enumerate only the initial window |
| Decision-tree validator | Convert accepted leaves into constraints rather than reversing every repeated branch |
| CVP/LLL integer validator | Preserve coefficient widths and bounds; a nearby lattice vector still needs original-checker validation |
| Prefix key-chain VM | Each recovered block initializes the next; rollback all state when a candidate fails |
| GBA meet-in-the-middle hash | Separate forward/backward states at a real invertible boundary and retain collision candidates |
| Sprague-Grundy game | Recover legal moves and terminal states, then compute mex values; the winning input is game logic |
| Kernel-module maze | Extract transitions from the module and solve the graph without loading an unknown driver |
| ROPfuscation / return-chain obfuscation | Treat stack words as the instruction stream and track gadget side effects |
| Image XOR / Newton convergence / PE bitmap | The program may generate an image rather than compare a string; recover dimensions, bit order, and palette |
| Quadtree image parser | Recurse using the encoded subdivision rule; validate consumed length and leaf coordinates |
| GLSL texture VM | Separate program memory from rendered output; handle STORE and scheduling effects explicitly |
| Font ligatures / LED Morse / GPIO LCD | Decode the output protocol: glyph substitutions, timing units, enable edges, command/data bits |
| BWT without a terminator | Recover rotations and use the checker's external ordering constraints to select the valid one |
| CRT plus matrix lookup | Solve modular constraints first, then reproduce lookup/index conventions |
| Brainfuck / FRACTRAN / Make VM / OPAL / Glulx | Identify state transitions and input-dependent comparisons before adopting a full language runtime |
| Unusual ROM / custom opcode / KVM HLT chaining | Inspect the emulator or handler implementing the instruction, not only a generic ISA manual |
| Cortex peripheral AES / MIPS coprocessor crypto | Memory-mapped registers or coprocessor calls may perform the cryptography outside ordinary ALU code |
| Bootloader / real-mode x86 / ARM in pixels | Recover load base, segment/mode, and byte packing before disassembly |
| Backdoored library / binary diff | Compare equivalent builds, strings and changed functions; startup and exported wrappers deserve attention |
| Date-derived key / instruction counter | Preserve the exact clock or counter state used by the transform |
| Destructor-hidden or MFC event validation | Trace object teardown or event dispatch as part of the main control flow |
| EBCDIC SAVF / DOS stub / embedded ZIP | Identify the actual nested representation and decode it locally |

AI/ML inversion examples in the source are not competition workflows here: the event's AI/ML restriction takes priority. Likewise, historical C2 enumeration and cloud-function examples do not authorize contacting unrelated services. Study their local control/data-flow lesson only.

## 14. A useful stopping point and a reproducible handoff

Keep the original hash, exact tool/environment, relevant function addresses, transformation pseudocode, extracted constants, solver script, and original-program validation result. Describe unresolved assumptions explicitly. If a patch only displays “correct,” say so; it is not a recovered flag unless the task explicitly asks for a patch.

| Failure | First correction |
| --- | --- |
| “Exec format error” | Match architecture/format; continue static analysis instead of installing an emulator |
| Existing ELF reports “No such file” | Inspect its requested interpreter/loader and supplied runtime |
| Breakpoint never hits | Verify image base, process/thread, optimization, inline comparison, and delayed library load |
| Solver returns printable nonsense | Recheck direction, endian order, widths, and whether the expected table was a decoy |
| Emulator hangs | Find the polling condition, missing interrupt, wrong branch semantics, or incorrect stop address |
| A dump will not decompile | Record its runtime base and segment permissions; raw data has no loader metadata |
| Decompiler disagrees with a run | Inspect the exact instructions, mutated code, ABI and hidden handlers |

Source map: `ctf-reverse/SKILL.md`, `tools.md`, `radare2-r2pipe.md`, `tools-dynamic.md`, `tools-emulation.md`, `tools-advanced.md`, `tools-advanced-2.md`, `mba-simplification.md`, `anti-analysis.md`, `anti-analysis-ctf.md`, `patterns.md`, `patterns-runtime.md`, `patterns-ctf.md`, `patterns-ctf-2.md`, `patterns-ctf-3.md`, `languages.md`, `languages-platforms.md`, `languages-compiled.md`, `platforms.md`, `platforms-hardware.md`, `unicorn-emulation.md`, and `field-notes.md`. Paths after the first share the `ctf-reverse/` prefix. The source `ctf-reverse/tools-mcp.md` is retained as provenance only; its agent integration and unapproved-tool setup are excluded from the human workflow.


---

<a id="07-cryptography"></a>

# Cryptography: recover the structure before the secret

A crypto challenge usually supplies an algorithm, parameters, ciphertext, or a query service. Your first task is to translate those into an exact mathematical statement. A recognizable number size or file extension is a clue; it is not an attack.

This chapter gives runnable local examples for common cases. [Advanced cryptography](#14-advanced-crypto) preserves the repository's lattice, elliptic-curve, polynomial, proof-system, post-quantum, and unusual algebra topics with diagnostics and constraints.

## 1. Environment and notation

**Windows:** open WSL and use the listed Python 3, OpenSSL, and RsaCtfTool installations. Native Windows Python is not assumed. **Kali:** Python is used throughout; the sheet lists crypto-attacks at `/opt/tools/crypto-attacks`, hlextend, hashcat, John, and other tools. Check the actual interpreter and tool before relying on them.

SageMath is approved on Kali, but the workbook records no installation information. Treat it as optional: try `sage --version`, and keep the standard-library examples below as fallbacks for basic arithmetic. Do not use a blanket installer. The Windows sheet permits adding non-AI Python libraries; it does not authorize rejected standalone tools or online services, or establish the same installation permission on Kali. On Kali, check provisioned dependencies.

Factordb-python is listed on Kali. That is not authorization to send challenge moduli to the FactorDB website. Keep factoring local. Do not use online hash-cracking, online mathematical solvers, AI tools, or public challenge uploads.

```bash
python3 --version
python3 -c "import sys; print(sys.executable); print(pow(3, -1, 11))"
```

Expected inverse: `4`, because `3*4 % 11 == 1`. Modular inverses require coprime inputs; an exception is meaningful evidence, not a reason to switch to floating point.

| Symbol | Meaning | Common error |
|---|---|---|
| `n` | RSA modulus or a group order, depending on context | Confusing the field prime with the subgroup order |
| `p`, `q` | Usually primes | Assuming repeated or composite factors are impossible |
| `e`, `d` | Public and private exponents | Inverting modulo `n` instead of the appropriate group exponent |
| `m`, `c` | Integer message and ciphertext | Losing leading zero bytes |
| `k` | Nonce, key, or multiplier | Reusing a variable for unrelated quantities |
| `^` | XOR in Python; exponentiation in Sage preparsed files | Copying syntax between interpreters |

Every Python block with a filename below is a complete local demonstration. Save it and run `python3 filename.py`. Replace toy values only after the assertions pass.

## 2. Triage worksheet

Record these before choosing an attack:

```text
Artifact: source / text / binary / capture / query service
Encoding: hex / base64 / decimal integers / raw bytes
Known values: ______________________________
Unknown values: ____________________________
Equation or state update: __________________
Oracle input and exact response: ___________
Query limit / reset behavior: ______________
Verification equation: _____________________
```

Read source in execution order. Trace key generation, serialization, padding, nonce generation, encryption/signing, and verification. Check whether two apparently separate operations share a secret or RNG state. A cryptographically strong primitive can be surrounded by a weak protocol.

| Observation | First local check | Next branch |
|---|---|---|
| Small `e`, short unpadded message | Exact integer root | RSA low-exponent section |
| Several RSA moduli | Pairwise GCD | Shared factors |
| Several encryptions of the same message | Compare modulus/exponent relationships | Common modulus or broadcast |
| Repeated nonce or IV | Compare ciphertext XOR and tags | Stream or authenticated-encryption analysis |
| Equal 16-byte ciphertext blocks | Count block repetitions | ECB hypothesis |
| Distinct decryption errors | Repeat controlled malformed samples | Padding/error oracle |
| Repeated signature `r` | Compare messages and signatures | Nonce reuse |
| Numeric outputs from a PRNG | Check exact bit widths and output transformation | LCG, MT, LFSR, or constraint model |
| Approximate linear equations modulo `q` | Estimate error bound | Lattice chapter |

## 3. Bytes, integers, and encodings

Save as `bytes_basics.py`:

```python
import base64

original = b'\x00CTF{toy}'
value = int.from_bytes(original, 'big')
recovered = value.to_bytes(len(original), 'big')
assert recovered == original
assert bytes.fromhex(original.hex()) == original
assert base64.b64decode(base64.b64encode(original), validate=True) == original
print(original.hex())
print(value)
print(recovered)
```

Expected final line: `b'\x00CTF{toy}'`. If you choose output length solely from `bit_length`, the initial zero disappears. For RSA, use the modulus byte length when inspecting padded plaintext; trim only after recognizing the padding format.

Hex and base64 are encodings, not encryption. Decode one layer into a new file and inspect its header and length. Arbitrarily repeating decoders can turn random data into misleading printable fragments.

## 4. Classical ciphers and XOR

For substitution and transposition, preserve punctuation, spacing, alphabet, and repeated groups. Compare character frequencies and repeated distances. A long alphabetic text supports frequency analysis; a short random flag often does not.

For Vigenère, test plausible key lengths using repeated distances and coincidence statistics, then analyze each residue class separately. For book ciphers, establish the exact edition, tokenization, indexing base, and whether punctuation counts. For Polybius/Nihilist/pigpen/semaphore, identify the symbol alphabet before forcing ASCII.

Save as `xor_known_plaintext.py`:

```python
def xor(a, b):
    if len(a) != len(b):
        raise ValueError('equal lengths required')
    return bytes(x ^ y for x, y in zip(a, b))

key = b'ICE'
plain = b'CTF{repeat_xor_is_not_a_pad}'
cipher = bytes(c ^ key[i % len(key)] for i, c in enumerate(plain))
known = b'CTF'
recovered_key = xor(cipher[:len(known)], known)
recovered = bytes(c ^ recovered_key[i % len(recovered_key)]
                  for i, c in enumerate(cipher))
assert recovered_key == key
assert recovered == plain
print(recovered.decode())
```

This works because the known plaintext covers the entire repeating key at the correct alignment. If the key is longer, those bytes reveal only part of it. Validate a candidate key against file structure, checksum, or several independent known bytes, not just a guessed flag prefix.

For single-byte XOR, all 256 candidates are cheap locally. Score printable text and expected structure; do not select the first candidate containing a brace. For repeating XOR, compare several key lengths and penalize overly long keys that merely fit a guessed prefix.

### Reused one-time pad or stream nonce

For equal-length streams, `c1 XOR c2 = p1 XOR p2`. It removes the reused keystream, not both plaintexts at once.

Save as `reused_stream.py`:

```python
from hashlib import sha256

def xor(a, b):
    assert len(a) == len(b)
    return bytes(x ^ y for x, y in zip(a, b))

p1 = b'known message 01'
p2 = b'secret message!!'
assert len(p1) == len(p2)
stream = sha256(b'toy reused stream').digest()[:len(p1)]
c1, c2 = xor(p1, stream), xor(p2, stream)
recovered = xor(xor(c1, c2), p1)
assert recovered == p2
print(recovered)
```

If output is nonsense, check offsets, encoding, compression, and whether nonce reuse actually produced the same key stream. Load-balanced servers may use different keys or counters; group samples by backend evidence before comparing them.

## 5. Reusable exact arithmetic

Save this as `math_helpers.py`. Later examples import it from the same directory.

```python
from math import gcd, prod

def iroot(value, degree):
    """Return floor(value**(1/degree)) using integer arithmetic."""
    if value < 0 or degree < 1:
        raise ValueError('nonnegative value and positive degree required')
    lo, hi = 0, 1
    while hi ** degree <= value:
        hi *= 2
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid ** degree <= value:
            lo = mid
        else:
            hi = mid
    return lo

def egcd(a, b):
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r:
        q = old_r // r
        old_r, r = r, old_r - q*r
        old_s, s = s, old_s - q*s
        old_t, t = t, old_t - q*t
    return old_r, old_s, old_t

def crt(residues, moduli):
    if len(residues) != len(moduli) or not moduli:
        raise ValueError('one residue per modulus required')
    for i, a in enumerate(moduli):
        if a <= 1 or any(gcd(a, b) != 1 for b in moduli[:i]):
            raise ValueError('pairwise coprime moduli greater than one required')
    total = prod(moduli)
    result = 0
    for residue, modulus in zip(residues, moduli):
        partial = total // modulus
        result += residue * partial * pow(partial, -1, modulus)
    return result % total

if __name__ == '__main__':
    assert iroot(27, 3) == 3 and iroot(28, 3) == 3
    assert iroot(0, 3) == 0
    assert crt([2, 3, 2], [3, 5, 7]) == 23
    g, a, b = egcd(17, 13)
    assert g == 1 and 17*a + 13*b == 1
    print('exact arithmetic checks passed')
```

Run `python3 math_helpers.py`. Never use `int(c ** (1/3))` on large RSA integers: floating-point precision makes it unreliable.

## 6. RSA with known factors

Save as `rsa_known_factors.py`:

```python
from math import gcd, lcm

p, q, e = 61, 53, 17
n = p*q
lam = lcm(p-1, q-1)
assert gcd(e, lam) == 1
d = pow(e, -1, lam)
m = 65
c = pow(m, e, n)
recovered = pow(c, d, n)
assert p*q == n
assert recovered == m
assert pow(recovered, e, n) == c
print(n, c, recovered)
```

Expected output: `3233 2790 65`. Re-encryption is the essential verification. For multiple distinct primes, use the LCM of each `p_i-1`. For repeated prime powers, use the correct totient/group structure; `(p-1)*(q-1)` is wrong when `p == q`.

If `gcd(e, lambda(n)) != 1`, there is no unique private exponent of this form. Factor the modulus and recover all appropriate roots; select using format and re-encryption. See the advanced chapter rather than silently choosing an invalid inverse.

### Shared factors and close primes

Save as `rsa_factor_checks.py`:

```python
from math import gcd, isqrt

moduli = [101*113, 101*127, 131*137]
hits = []
for i, n in enumerate(moduli):
    for j in range(i):
        p = gcd(n, moduli[j])
        if 1 < p < n:
            hits.append((j, i, p))
assert hits == [(0, 1, 101)]
print('shared:', hits)

def fermat(n, budget=10000):
    if n % 2 == 0:
        return 2, n//2
    a = isqrt(n)
    if a*a < n:
        a += 1
    for _ in range(budget):
        delta = a*a - n
        b = isqrt(delta)
        if b*b == delta:
            return a-b, a+b
        a += 1
    return None

factors = fermat(1009*1013)
assert factors == (1009, 1013)
print('close primes:', factors)
```

For many keys, pairwise GCD is quadratic; use a local batch-GCD implementation from approved crypto-attacks after validating its inputs. Duplicate moduli produce `gcd == n`, which is not a new factor. Fermat is useful when primes are close; an exhausted budget is a reason to pivot.

### Small exponent, common modulus, broadcast

Save as `rsa_structural.py`, beside `math_helpers.py`:

```python
from math_helpers import iroot, egcd, crt

# Case 1: no modular wraparound.
m, e, n = 42, 3, 1000003*1000033
c = pow(m, e, n)
root = iroot(c, e)
assert root**e == c and root == m
print('small exponent:', root)

# Case 2: same message and modulus, coprime exponents.
n, e1, e2, m = 101*113, 3, 7, 42
c1, c2 = pow(m, e1, n), pow(m, e2, n)
g, a, b = egcd(e1, e2)
assert g == 1
recovered = pow(c1, a, n) * pow(c2, b, n) % n
assert recovered == m
assert pow(recovered, e1, n) == c1
print('common modulus:', recovered)

# Case 3: same unpadded message under three coprime moduli.
moduli = [101*113, 107*131, 137*149]
m, e = 42, 3
cs = [pow(m, e, modulus) for modulus in moduli]
combined = crt(cs, moduli)
recovered = iroot(combined, e)
assert recovered**e == combined and recovered == m
assert all(pow(recovered, e, modulus) == ci
           for modulus, ci in zip(moduli, cs))
print('broadcast:', recovered)
```

Small `e` alone is insufficient: padding or modular wraparound defeats the first check. The common-modulus script needs invertible ciphertexts for negative exponents; a failed inverse may expose a factor through GCD. Broadcast needs the same integer message and enough combined modulus size. Randomized padding breaks that assumption.

### Textbook RSA multiplicativity

Save as `rsa_blinding_toy.py`:

```python
from math import gcd

p, q, e = 61, 53, 17
n = p*q
d = pow(e, -1, (p-1)*(q-1))
message = 65
ciphertext = pow(message, e, n)
factor = 2
assert gcd(factor, n) == 1
modified = ciphertext * pow(factor, e, n) % n

def toy_decrypt_oracle(c):
    return pow(c, d, n)

answer = toy_decrypt_oracle(modified)
recovered = answer * pow(factor, -1, n) % n
assert recovered == message
print(recovered)
```

This models an oracle that refuses one ciphertext but decrypts related ciphertexts. Proper padding and protocol validation change the available oracle. Never assume a signing oracle accepts arbitrary integers; inspect hashing and encoding first.

### RsaCtfTool without accidental online analysis

On **Windows WSL**, locate the supplied RsaCtfTool entry point and read its local help. Inspect a PEM public key with the listed OpenSSL:

```bash
openssl pkey -pubin -in public.pem -text -noout
```

Expected fields include the modulus and exponent. Choose a local attack matching an observed property, such as close primes or shared factors. Do not launch an all-attacks mode without checking whether it includes network-backed factoring. If the entry point is absent, extract the numbers from supplied text and use the scripts above.

## 7. Block modes: distinguish confidentiality from integrity

For AES the block size is 16 bytes. ECB encrypts equal plaintext blocks to equal ciphertext blocks under the same key. CBC combines each plaintext block with the previous ciphertext block (or IV). CTR and OFB generate a stream that is XORed with plaintext.

Save as `block_repetitions.py` and pass a raw ciphertext filename:

```python
from collections import Counter
from pathlib import Path
import sys

data = Path(sys.argv[1]).read_bytes()
for offset in range(16):
    blocks = [data[i:i+16] for i in range(offset, len(data)-15, 16)]
    repeats = sum(count-1 for count in Counter(blocks).values() if count > 1)
    if repeats:
        print('offset', offset, 'repeated blocks', repeats)
```

Repeated blocks are evidence of deterministic block behavior, not a complete ECB proof. File headers, duplicated chunks, and framing can create repetitions too. With a chosen-plaintext oracle, compare ciphertext for repeated aligned input blocks.

### CBC bit flipping without an AES dependency

The relation is `P_i = D(C_i) XOR C_(i-1)`. Changing the previous block by `old XOR wanted` changes the targeted plaintext bytes. The previous plaintext block is usually corrupted; changing the IV targets the first block without that side effect.

Save as `cbc_relation.py`:

```python
def xor(a, b):
    assert len(a) == len(b)
    return bytes(x ^ y for x, y in zip(a, b))

# A fixed hypothetical decrypted block D(C1), not an AES implementation.
intermediate = bytes(range(16))
original = b'admin=0;uid=1000'
desired = b'admin=1;uid=1000'
iv = xor(intermediate, original)
modified_iv = xor(iv, xor(original, desired))
assert xor(intermediate, iv) == original
assert xor(intermediate, modified_iv) == desired
print(xor(intermediate, modified_iv))
```

Expected output contains `admin=1`. An authenticated ciphertext should be rejected after modification. If a challenge uses a CRC instead of a MAC, analyze that CRC separately; arbitrary CRC updates do not bypass a real authentication tag.

### ECB suffix recovery: runnable oracle rehearsal

The following uses a deterministic block transform to demonstrate byte alignment and dictionary matching. It is not AES and is not a cryptographically secure encryption implementation. The same equality logic applies to a deterministic ECB oracle with a fixed unknown suffix.

Save as `ecb_suffix_toy.py`:

```python
from hashlib import sha256

BLOCK = 16
secret = b'CTF{ecb_demo}'
key = b'local toy key'

def oracle(prefix):
    data = prefix + secret
    pad = BLOCK - len(data) % BLOCK
    data += bytes([pad]) * pad
    return b''.join(sha256(key + data[i:i+BLOCK]).digest()[:BLOCK]
                    for i in range(0, len(data), BLOCK))

base_length = len(oracle(b''))
growth = next(i for i in range(1, BLOCK+1)
              if len(oracle(b'A'*i)) > base_length)
secret_length = base_length - growth
known = b''
for index in range(secret_length):
    prefix = b'A' * (BLOCK-1-index % BLOCK)
    block_index = index // BLOCK
    start = block_index * BLOCK
    target = oracle(prefix)[start:start+BLOCK]
    matches = []
    for candidate in range(256):
        sample = oracle(prefix + known + bytes([candidate]))
        if sample[start:start+BLOCK] == target:
            matches.append(candidate)
    assert len(matches) == 1
    known += bytes([matches[0]])
assert known == secret
print(known)
```

Failure usually means a changing key, unknown prefix, randomized encryption, wrong block size, compression, or a query limit. Determine whether the prefix is fixed or changes per request before trying to align it. Do not send the toy loop to a remote service until its oracle model and allowed query budget are established.

## 8. Padding and error oracles

A CBC padding oracle reveals whether modified plaintext has valid padding. First distinguish padding rejection from authentication rejection, JSON parsing, UTF-8 decoding, or normal application errors. Repeat controls: one noisy error is insufficient.

This complete local simulator recovers a 16-byte intermediate value using only a padding-validity function. Save as `padding_oracle_toy.py`:

```python
BLOCK = 16
intermediate = bytes([91, 2, 77, 18, 200, 17, 9, 55, 66, 7, 33, 111, 8, 4, 3, 2])
plain = b'CTF{oracle_demo}'
assert len(plain) == BLOCK
original_previous = bytes(a ^ b for a, b in zip(intermediate, plain))
queries = 0

def valid_padding(chosen_previous):
    global queries
    queries += 1
    candidate = bytes(a ^ b for a, b in zip(intermediate, chosen_previous))
    length = candidate[-1]
    return 1 <= length <= BLOCK and candidate[-length:] == bytes([length])*length

recovered = bytearray(BLOCK)
for index in range(BLOCK-1, -1, -1):
    pad = BLOCK-index
    probe = bytearray(BLOCK)
    for j in range(index+1, BLOCK):
        probe[j] = recovered[j] ^ pad
    found = []
    for guess in range(256):
        probe[index] = guess
        if not valid_padding(probe):
            continue
        # Reject accidental padding longer than the intended suffix.
        if index > 0:
            probe[index-1] ^= 1
            still_valid = valid_padding(probe)
            probe[index-1] ^= 1
            if not still_valid:
                continue
        found.append(guess ^ pad)
    assert len(found) == 1, (index, found)
    recovered[index] = found[0]

result = bytes(a ^ b for a, b in zip(recovered, original_previous))
assert bytes(recovered) == intermediate
assert result == plain
print(result, 'queries:', queries)
```

This simulates one block, not a network exploit. To adapt it, preserve the full protocol framing, determine which block is actually decrypted, and confirm that a MAC is not checked first. False positives at padding length 1 need the second probe shown above. UTF-8 or application-format oracles require different logic.

RSA PKCS#1 v1.5 and OAEP-leading-byte oracles use multiplicative interval narrowing, not CBC byte flipping. Record the exact predicate before using a Bleichenbacher or Manger implementation from approved local crypto-attacks. See the advanced chapter for the distinction.

## 9. Hashes, MACs, CRCs, and compression

Hash length is not an algorithm identifier. Compare source, field names, encoding, salt placement, and known test values. A 32-character hex string might be MD5, a random token, or truncated output from another function.

Length extension applies to constructions such as certain Merkle–Damgård hashes of `secret || message`. It does not apply to HMAC simply because HMAC uses the same hash internally. You need the original digest, original message, a secret-length hypothesis, and an application parser that accepts the required glue padding.

**Kali:** hlextend is listed, but check its installed API locally before use:

```bash
python3 -c "import hlextend; help(hlextend)"
```

Start with a toy local verifier and verify the extended digest exactly before querying a challenge. Hash length extension does not decrypt a message and does not recover the secret.

For a custom XOR-aggregate hash or linear MAC, express each known message/signature pair as equations over the correct field. CRC32 is affine for fixed conventions and message lengths; bit order, initial state, and final XOR matter. Compare equal-length messages and verify any proposed correction with the same CRC implementation.

For compression side channels, measure compressed length before encryption noise if the interface permits. Keep secret context and chosen prefix adjacent, repeat samples, and compare candidates of equal input length. Padding, random prefixes, different compression dictionaries, and state resets can hide the signal.

Collision and preimage are different goals. A collision for two chosen files is not a preimage for a fixed digest. A published SHA-1 collision pair does not automatically produce a chosen-prefix collision for an arbitrary challenge document.

## 10. Diffie–Hellman and signature nonces

For finite-field DH, record `p`, generator `g`, both public keys, and whether private keys persist. Check trivial generator values, group order factors, and validation of peer public values.

Save as `dh_toy.py`:

```python
p, g, alice, bob = 1019, 2, 123, 456
A, B = pow(g, alice, p), pow(g, bob, p)
shared_a, shared_b = pow(B, alice, p), pow(A, bob, p)
assert shared_a == shared_b
print('shared:', shared_a)

for bad_g in [0, 1, p-1]:
    possibilities = {pow(bad_g, exponent, p) for exponent in range(1, 12)}
    print('generator', bad_g, 'public possibilities', sorted(possibilities))
assert {pow(p-1, exponent, p) for exponent in range(1, 12)} == {1, p-1}
```

Small-subgroup confinement needs an accepted low-order public value, a persistent secret, and an observable response that distinguishes candidate shared secrets. One oracle output with an ephemeral secret does not accumulate CRT information across sessions.

For DSA/ECDSA, repeated nonce `k` can expose the private key. The modular arithmetic below is common to both signature equations, using a toy subgroup order. It does not generate an elliptic-curve point.

Save as `nonce_reuse.py`:

```python
n = 1019
private, nonce, r = 123, 77, 456
h1, h2 = 100, 200
s1 = pow(nonce, -1, n) * (h1 + r*private) % n
s2 = pow(nonce, -1, n) * (h2 + r*private) % n
recovered_nonce = (h1-h2) * pow(s1-s2, -1, n) % n
recovered_private = (s1*recovered_nonce-h1) * pow(r, -1, n) % n
assert recovered_nonce == nonce
assert recovered_private == private
assert s1*nonce % n == (h1+r*private) % n
assert s2*nonce % n == (h2+r*private) % n
print(recovered_nonce, recovered_private)
```

Use the subgroup order, not the curve field prime. Match the real message hash truncation. ECDSA low-s normalization may require trying sign variants. Validate the recovered private key against the published public key. Ed25519 uses different encoding and scalar derivation; do not paste ECDSA code into it unchanged.

## 11. Predictable randomness

Identify the generator and its output transformation. Record how many hidden draws occur between observations. Timestamp seeds, truncated outputs, floating-point conversion, rejection sampling, and modulo reduction change the attack.

### LCG recovery and backward stepping

Save as `lcg_recovery.py`:

```python
from math import gcd

modulus, multiplier, increment = 1009, 65, 17
states = [123]
for _ in range(7):
    states.append((multiplier*states[-1]+increment) % modulus)

d1 = (states[1]-states[0]) % modulus
d2 = (states[2]-states[1]) % modulus
assert gcd(d1, modulus) == 1
a = d2 * pow(d1, -1, modulus) % modulus
c = (states[1]-a*states[0]) % modulus
assert (a, c) == (multiplier, increment)
assert all((a*x+c) % modulus == y for x, y in zip(states, states[1:]))
previous = (states[1]-c) * pow(a, -1, modulus) % modulus
assert previous == states[0]
print('a, c, previous:', a, c, previous)

# Unknown modulus: differences produce multiples of the modulus.
diffs = [y-x for x, y in zip(states, states[1:])]
candidate = 0
for x, y, z in zip(diffs, diffs[1:], diffs[2:]):
    candidate = gcd(candidate, abs(x*z-y*y))
assert candidate % modulus == 0
print('modulus multiple:', candidate)
```

The GCD may be a multiple of the modulus. Filter candidates using all observations and known bounds. If a difference is not invertible, solve the resulting congruence rather than discarding the case. Truncated outputs need a different model, often constraints or a lattice.

### Time seeds and generator matching

Bound the seed window using challenge timestamps; reproduce the exact language/runtime PRNG. Python `random`, libc `rand`, Java's LCG, and browser `Math.random` are not interchangeable. Use a known output sequence to verify the generator before testing a derived key.

For MT19937, enough full consecutive outputs permit state reconstruction after undoing tempering. Python floating outputs combine parts of multiple draws; they are not full 32-bit words. A tool that expects 624 raw words cannot accept decimal floats unchanged.

PCG, xorshift, xoroshiro, and xoshiro have distinguishable state transitions and output scramblers. Read constants and rotation amounts from source. Chaotic maps also depend on floating-point precision; mathematically similar real-valued recurrences can produce different byte streams.

LFSR output is linear only when the observed output is a linear state function. Filtered or combined LFSRs require correlation, algebraic, or constraint techniques. See the advanced chapter for a tested Berlekamp–Massey example.

## 12. A disciplined finish

Check the recovered object in the original equation: re-encrypt plaintext, verify a signature, regenerate observed RNG outputs, or reproduce the tag. Plausible English is not enough. Keep the original bytes, parameters, solver assumptions, and a minimal script with assertions.

If a solver stalls, reduce a toy instance first. Wrong endianness, the wrong modulus, row/column conventions, hidden random draws, noninvertible values, and incorrect oracle definitions are more common than missing brute-force capacity.

The chapter merges the source skill overview, classic/historical ciphers, RSA, DH, PRNG, stream, modern-mode and MAC notes. Specialized topics continue in [Advanced cryptography](#14-advanced-crypto); every crypto source file has a disposition in the coverage manifest.


---

<a id="08-binary-exploitation"></a>

# Binary exploitation: prove the primitive, then build the chain

Binary exploitation begins after you can explain the vulnerable operation. “The program crashes” is an observation. “A negative index reads an eight-byte pointer before the array” is a primitive you can build on. Record what you control, where it lands, how much you can read or write, and which operation triggers the next step.

Pwn is an advanced preparation topic: it is not one of the official categories identified for this event. Prioritize the listed categories first. These procedures concern local practice binaries and explicitly assigned challenge services only. The event's AI prohibition, approved-tool restrictions, and ban on public online analysis/compilation still apply.

## 1. Keep the two environments distinct

| Environment | Workbook-backed route | What is not implied |
| --- | --- | --- |
| **Windows native** | x64dbg, HxD, Notepad++ | Linux ELF execution, WinDbg, debugger extensions |
| **Windows WSL** | Python 3, GDB, objdump, strings, Ghidra, xxd | A native Windows Python install or Kali copies of these tools |
| **Kali** | radare2 row 123, checksec 28, ROPgadget 128, GCC/build tools 54, strace 145, ltrace 90 | Every tool normally associated with Kali |
| **Kali debugger extensions** | GEF 55, peda 111, pwndbg 116 | All extensions safely loaded into the same GDB session |

The Kali sheet is best-effort and records no installed-version information for Python 3.11. Check `python3 --version`; use Windows WSL for standard-library Python if Kali's interpreter is unavailable. GDB is explicitly listed in Windows WSL. Kali's extension rows describe supplied GDB setups; check that the provided debugger launches rather than assuming an unrelated WSL installation carries over.

**Windows WSL, Bash:**

```bash
command -v python3 gdb objdump strings
python3 --version
gdb --version
```

**Kali, Bash:**

```bash
command -v r2 checksec ROPgadget gcc gdb python3
r2 -v
checksec --version
```

Pwntools is not individually listed. Windows row 14 allows adding non-AI Python libraries, which can cover a non-AI library such as pwntools; this is not evidence that it is preinstalled, works with the supplied interpreter, or has its assembler/debugger dependencies. Do not infer a separate Kali installation permission from the Windows row. The main procedures below use standard-library Python, GDB, and approved static tools. No blanket installers are required.

## 2. Establish the exact target before discussing mitigations

Use `chall` for the local binary, `libc.so.6` and `ld-linux-x86-64.so.2` only when they were supplied for this exact target. Save an original copy and hash. Record the argument/stdin/network protocol, architecture, byte order, runtime files, and expected successful behavior.

**Windows WSL:**

```bash
objdump -f chall
objdump -x chall > headers.txt
objdump -T chall > dynamic-symbols.txt
strings -a chall > strings.txt
```

**Kali:**

```bash
file chall
checksec --file=chall
rabin2 -I chall
rabin2 -S chall
rabin2 -i chall
rabin2 -R chall
```

Read the vulnerable function, not just the protection summary. On Kali, `r2 chall`, then `aaa`, `afl`, and `pdf @ main` are the starting sequence; `axt @ sym.imp.read` locates callers when that import exists. On Windows WSL, use `objdump -d -M intel --disassemble=main chall` or Ghidra's local decompiler.

| Evidence | Implication | Required follow-up |
| --- | --- | --- |
| NX / non-executable stack | Injected stack bytes are unlikely to execute | Find a legitimate code target, ROP route, or actual executable mapping |
| Canary instrumentation | Some return paths detect overwritten stack data | Inspect this particular frame and whether the intended write crosses it |
| PIE | Main-image addresses depend on its load base | Obtain a matching image pointer or prove a valid partial overwrite |
| Full RELRO | Relocation data is intended read-only after binding | Verify mappings and target another writable object |
| Partial RELRO | Some relocation slots may be writable | Confirm the exact target slot and its future call site |
| Static linking | Functions may be embedded in the executable | Locate their actual presence; do not assume `system` was linked |
| Seccomp evidence | A syscall policy may constrain the end goal | Read the filter, architecture tests and argument checks |
| CET/CFI | Returns or indirect calls may be checked | Determine which features are enabled and enforced in this process |

No canary symbol does not prove every function is unprotected. No `GNU_STACK` entry does not prove an executable stack. A non-PIE executable does not fix the libc, heap, or stack addresses. A named mitigation is a constraint on a chain, not a complete exploitability verdict.

## 3. First build a reliable input harness

For a one-shot local program, avoid shell quoting and text conversions. Save as `run_local.py`.

**Windows WSL Python; Kali after Python check:**

```python
import subprocess
from pathlib import Path

payload = b'AAAA\n'
Path('input.bin').write_bytes(payload)
try:
    result = subprocess.run(['./chall'], input=payload,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            timeout=3, check=False)
except subprocess.TimeoutExpired as error:
    print('timeout; partial output:', repr(error.stdout))
else:
    print('exit:', result.returncode)
    print('stdout:', repr(result.stdout))
    print('stderr:', repr(result.stderr))
```

Change the input only after a baseline works. A negative return code on Unix commonly identifies a terminating signal. A timeout can mean the program expects another line, waits for EOF, or is stuck; it is not proof of a successful exploit.

For an authorized challenge endpoint, this standard-library helper handles a prompt split across packets. It connects only to the host and port you pass explicitly; it performs no discovery. Save as `one_prompt.py`.

```python
import argparse
import socket

parser = argparse.ArgumentParser()
parser.add_argument('host', help='exact assigned challenge host')
parser.add_argument('port', type=int)
args = parser.parse_args()

def recv_until(sock, marker, limit=65536):
    data = bytearray()
    while marker not in data:
        part = sock.recv(4096)
        if not part:
            raise EOFError(f'closed before prompt: {bytes(data)!r}')
        data.extend(part)
        if len(data) > limit:
            raise ValueError('prompt not found within limit')
    return bytes(data)

with socket.create_connection((args.host, args.port), timeout=3) as sock:
    sock.settimeout(3)
    print(repr(recv_until(sock, b'> ')))
    sock.sendall(b'AAAA\n')
    print(repr(sock.recv(4096)))
```

The literal `b'> '` is this example's prompt: replace it with an observed prompt. This minimal helper returns all received bytes, including any bytes after the marker; a multi-stage protocol needs a retained receive buffer. Never assume one `recv()` equals one server message, and do not use `.strip()` on leaked binary pointers because whitespace bytes may be data.

## 4. A complete data-only exercise

Before overwriting a return address, practice field layout and binary input. This intentionally vulnerable **wire-format** example accepts a client-controlled authorization field. It is fully defined C and does not rely on compiler-specific stack layout. Save as `record.c`.

```c
#include <stdint.h>
#include <stdio.h>

int main(void) {
    unsigned char record[20] = {0};
    size_t got = fread(record, 1, sizeof record, stdin);
    if (got != sizeof record) { puts("need 20 bytes"); return 1; }
    uint32_t approved = (uint32_t)record[16]
        | ((uint32_t)record[17] << 8)
        | ((uint32_t)record[18] << 16)
        | ((uint32_t)record[19] << 24);
    puts(approved == 0x12345678 ? "practice accepted" : "denied");
    return 0;
}
```

**Kali, approved GCC:**

```bash
gcc -Wall -Wextra -O0 -o record record.c
```

**Kali Python, after checking it; or generate the file in Windows WSL and transfer it to the Kali practice directory:**

```python
from pathlib import Path
import struct

payload = b'A' * 16 + struct.pack('<I', 0x12345678)
assert len(payload) == 20
assert payload[-4:] == b'\x78\x56\x34\x12'
Path('record.bin').write_bytes(payload)
```

**Kali:**

```bash
./record < record.bin
```

Expected output: `practice accepted`. The lesson is that a data-field change can meet the objective without code execution. For a real overflow, you must additionally prove how an input write reaches an adjacent field; this toy does not claim to demonstrate stack corruption.

## 5. Measure an overflow rather than guessing its offset

Use a recognizable nonrepeating pattern. The following standard-library generator provides unique four-byte windows within its generated sequence. Save as `pattern.py`.

**Windows WSL Python; Kali with Python available:**

```python
import argparse
from pathlib import Path

def de_bruijn(alphabet, width):
    k = len(alphabet)
    work = [0] * (k * width)
    result = []
    def visit(t, period):
        if t > width:
            if width % period == 0:
                result.extend(work[1:period + 1])
        else:
            work[t] = work[t - period]
            visit(t + 1, period)
            for value in range(work[t - period] + 1, k):
                work[t] = value
                visit(t + 1, t)
    visit(1, 1)
    return bytes(alphabet[i] for i in result)

parser = argparse.ArgumentParser()
parser.add_argument('--length', type=int, default=512)
parser.add_argument('--find', help='four bytes in memory order, as eight hex digits')
args = parser.parse_args()
pattern = de_bruijn(b'abcdefgh', 4)
assert len({pattern[i:i+4] for i in range(len(pattern)-3)}) == len(pattern)-3
if args.find:
    needle = bytes.fromhex(args.find)
    if len(needle) != 4: raise SystemExit('supply exactly four bytes')
    print(pattern.find(needle))
else:
    if not 1 <= args.length <= len(pattern):
        raise SystemExit(f'length must be 1..{len(pattern)}')
    Path('pattern.bin').write_bytes(pattern[:args.length])
    print('wrote', args.length, 'bytes')
```

```bash
python3 pattern.py --length 512
gdb -q ./chall
```

**Windows WSL GDB; Kali only with supplied GDB confirmed:**

```text
set disassembly-flavor intel
run < pattern.bin
info registers
x/32bx $sp
x/8gx $sp
bt
```

On x86-64, a noncanonical overwritten return pointer may fault at `ret` before RIP becomes the pattern. Inspect the pending return slot on the stack. Copy four bytes in increasing memory-address order and run `python3 pattern.py --find HEXBYTES`, substituting those eight hex digits. A `-1` means the sequence is absent: inspect truncation, byte order, newline handling, or which frame actually crashed.

The generator uses a maximum length of 4096 with this alphabet. Do not compare its result with a different pattern generator's offset. After measuring offset `N`, send exactly `N` filler bytes plus a recognizable pointer-sized marker and stop before the vulnerable return. Confirm that the marker occupies the saved return slot. In an optimized frame, `buffer size + pointer size` is not a trustworthy formula.

## 6. Ret2win, calling conventions, and a reproducible builder

A ret2win chain is possible when a useful function already exists and the input can reach its call path. Determine the measured return offset, the function's actual address, its arguments, the canary status, and stack alignment. A function called `win` may still require a valid state or argument.

**Kali:**

```bash
r2 -q -c 'aaa;afl~win;pdf @ sym.win' chall
ROPgadget --binary chall --only 'pop|ret' > gadgets.txt
rg 'pop rdi|pop rsi|pop rdx|ret$' gadgets.txt
```

If the symbol is absent, locate the success string and its references. Gadget output is a list of candidates: inspect the complete gadget instructions and whether the address is rebased for PIE. Additional `pop` instructions consume additional stack words.

This builder requires measured values as command-line arguments and performs no execution. Save as `build_return.py`.

**Windows WSL Python; Kali after interpreter check:**

```python
import argparse
import struct
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('offset', type=lambda s: int(s, 0))
p.add_argument('address', type=lambda s: int(s, 0))
p.add_argument('--bits', type=int, choices=[32, 64], default=64)
p.add_argument('--alignment-ret', type=lambda s: int(s, 0))
args = p.parse_args()
if not 0 <= args.offset <= 1048576: raise SystemExit('unreasonable offset')
fmt = '<Q' if args.bits == 64 else '<I'
words = []
if args.alignment_ret is not None: words.append(args.alignment_ret)
words.append(args.address)
payload = b'A' * args.offset + b''.join(struct.pack(fmt, x) for x in words)
Path('return.bin').write_bytes(payload)
print('wrote', len(payload), 'bytes; contains newline:', b'\n' in payload)
```

For an intentionally fictional measurement, `python3 build_return.py 72 0x401234` creates a 64-bit payload file. **Those numbers belong only to the builder demonstration; they are not an exploit for `chall`.** Replace them with the measurements above and inspect the resulting file before using it against your local target.

At a normal System V x86-64 function entry, the stack reflects the return address pushed by a call. A ROP return into the function may have different alignment. A fault on an aligned SIMD instruction suggests checking RSP and memory operands; add an alignment `ret` only when the diagnosis supports it. Also preserve callee-saved registers when the continuation depends on them.

| Architecture / ABI | Arguments and return path |
| --- | --- |
| Linux x86-64 System V | RDI, RSI, RDX, RCX, R8, R9; return in RAX |
| Linux x86-64 syscall | RDI, RSI, RDX, R10, R8, R9; number in RAX; RCX/R11 clobbered |
| i386 cdecl | Stack arguments; caller normally cleans the stack |
| Windows x64 | RCX, RDX, R8, R9; caller reserves shadow space |
| ARM A32 | r0–r3; link register and ARM/Thumb state matter |
| AArch64 | x0–x7; link register x30 and 16-byte stack alignment matter |

## 7. From an information leak to ROP

For a dynamic libc chain, the sequence is usually: obtain a pointer into the exact library, subtract that symbol's offset, verify another address, then build the next call. A function's exported entry and a return address inside that function have different offsets.

**Windows WSL, inspect a supplied libc; no online lookup service:**

```bash
objdump -T libc.so.6 > libc-symbols.txt
strings -a -t x libc.so.6 > libc-strings.txt
```

**Kali equivalent:**

```bash
rabin2 -s libc.so.6 > libc-symbols.txt
rabin2 -zz libc.so.6 > libc-strings.txt
rg 'puts|system|read|write' libc-symbols.txt
```

The arithmetic below is a complete toy calculation. Its addresses are invented and cannot identify a real runtime.

```python
leaked_puts = 0x7f1200080900
puts_offset = 0x80900
system_offset = 0x4f550
base = leaked_puts - puts_offset
assert base == 0x7f1200000000
assert base & 0xfff == 0
print('base:', hex(base), 'system:', hex(base + system_offset))
```

A page-aligned base is a consistency check, not proof. With an approved local debugger, check mappings and the loaded file. When supplied, invoke the challenge's loader and library path explicitly according to its run script. Do not quietly replace an old challenge libc with the host's libc: allocator behavior and offsets will differ.

For stage one, a common x86-64 shape is `pop rdi; ret → address to read → puts@plt → reentry`. It leaks until NUL, and stdout framing can add bytes; `write(1, address, size)` provides a fixed-length leak when you can control all its arguments. The reentry point must restore a usable stack/input state. Use a fresh process for each failed experiment unless you have proved the connection survived.

**A manual stack diagram, eight bytes per row on x86-64:**

```text
padding up to the measured return slot
address of argument-setup gadget
argument value(s), including values consumed by extra pops
address of function or syscall gadget
address of a valid continuation
```

Track every gadget's consumed stack bytes, register clobbers, memory reads/writes, and branch conditions. `ret2csu` needs the actual constructor gadgets and loop/cleanup conditions; newer binaries need not contain the familiar pair. A `pop rdx; pop rbx; ret` gadget needs both stack values. `puts()` is allowed to clobber caller-saved registers, so do not rely on a fixed RDX value afterward.

### Stack pivots, SROP, and dynamic resolution

For `leave; ret`, `leave` sets SP from BP and pops a new BP; `ret` consumes the next word as PC. A fake frame therefore needs both words. Check that the new stack is writable, large enough, aligned, and still mapped when subsequent calls execute. A pivot using a 32-bit stack register can truncate a 64-bit address.

SROP uses a kernel signal-return path to restore many registers from a frame. It requires a valid trigger, exact architecture/kernel frame layout, mapped stack, and a permitted next syscall. Merely serializing a frame or sending `/bin/sh` does not place that string at the pointer named in the frame. Modern shadow-stack enforcement must be investigated separately; the source's broad claim of a generic signal-frame bypass is not treated as an established recipe.

`ret2dlresolve` forges dynamic-linker metadata. It needs a reachable resolver, correctly related symbol/string/relocation records, usable writable storage, and compatible binding/version rules. It is not a general bypass of Full RELRO. With vDSO/vsyscall or partial GOT redirection, first inspect the actual kernel-provided mapping and instruction bytes; historical fixed addresses and executable modes vary.

## 8. Format strings: separate a leak from a write

A format-string bug occurs when user data becomes the **format argument**, such as `printf(input)`. `printf("%s", input)` is not that bug. Establish the sink in the disassembly or decompiler before sending probes.

For a local practice instance, a short marker followed by several `%p` directives tests whether stack/register values appear. Increase slowly and record which argument corresponds to your marker. Positional forms such as `%7$p` depend on the libc and call site; “offset six” is not a universal fact.

| Specifier | Relevant effect | Precondition |
| --- | --- | --- |
| `%p` | Print a pointer-shaped argument | An argument slot exists; output need not be a valid pointer |
| `%s` | Dereference an argument as a string | You can supply or identify a readable pointer |
| `%n` | Write character count through a pointer | Writable destination and a format path allowing `%n` |
| `%hn` / `%hhn` | Store a narrower count | Correct pointer position and accounting modulo 65536/256 |

**Windows WSL Python; harmless count-planning example:**

```python
targets = [(0x1000, 0x42), (0x1001, 0x13), (0x1002, 0xff)]
count = 7                         # seven characters already printed
for address, wanted in sorted(targets, key=lambda pair: pair[1]):
    padding = (wanted - count) % 256
    count += padding
    print(hex(address), 'padding=', padding, 'stored=', hex(count & 255))
```

This computes counts only. A real payload must also account for literal bytes printed by the vulnerable call, pointer alignment, string termination, width fields, write ordering, and any input transform such as ROT13. A zero padding does not require a `%0c`. FORTIFY behavior, positional arguments, and writable/read-only format checks depend on the exact runtime.

For GOT writes, prove the slot is writable and will be called with useful arguments. For saved frame or return-pointer writes, obtain the correct live stack address. A single-call leak-and-write cannot generally use a value learned from its own future output; special retargeting chains depend on argument evaluation order. Avoid copying `%n` generators without reconstructing that order.

## 9. Heap work starts with ownership and allocation history

Draw each object with fields and ownership. Then make a ledger for every menu action: requested size, actual chunk size when known, returned pointer, owner, free state, and whether any stale reference remains. A use-after-free is an access through a reference whose lifetime has ended. A double-free and an uninitialized pointer are different bugs even if they later lead to similar allocations.

**Windows WSL GDB; Kali supplied GDB setup if available:**

```text
break malloc
break free
run
bt
info registers rdi
finish
info registers rax
```

These registers apply to Linux x86-64. Stop at the relevant call site or add a condition after finding it; breakpoints on every allocation may be noisy. `finish` after `malloc` lets you inspect its returned pointer. Record the corresponding application object before continuing.

**Kali GEF:** the workbook specifically provides `/opt/tools/gef.py` and says it is not auto-sourced to avoid a peda clash. For an isolated GEF session:

```bash
gdb -nx -q -x /opt/tools/gef.py ./chall
```

Use the installed extension's `help` to inspect supported heap commands. `-nx` skips local initialization; do not source peda, pwndbg, and GEF together. Plain GDB memory inspection remains the fallback.

### Tcache, safe-linking, and version boundaries

In relevant glibc versions, tcache stores freed small allocations in per-thread lists. A stale write into a freed chunk can corrupt a link; subsequent allocations may follow that corrupted link if all checks pass. Size class, list count, alignment, duplicate-free checks, and safe-linking matter. `calloc`, `realloc`, and cross-bin behavior are version-dependent; observe the target's actual allocator instead of relying on a version slogan.

A common safe-linking relation is `stored = target XOR (address_of_link_field >> 12)`. The address is the position where the link is stored, not an arbitrary heap base. This self-contained example demonstrates the relation only:

```python
link_field = 0x5555555592a0
target = 0x55555555a040
stored = target ^ (link_field >> 12)
assert (stored ^ (link_field >> 12)) == target
print(hex(stored))
```

Pointer decoding does not bypass the remaining allocator checks. Examine the supplied allocator implementation when exact behavior matters; the [glibc allocator source](https://github.com/bminor/glibc/blob/master/malloc/malloc.c) shows how protection and bookkeeping interact, but its current version is not a substitute for the target's version.

The normal allocator stopped using the traditional malloc/free hooks in glibc 2.34. A visible compatibility symbol does not make an old `__free_hook` exploit work. This version boundary is documented in the [glibc 2.34 announcement](https://sourceware.org/pipermail/libc-announce/2021/000032.html).

| Family from the source notes | Primitive and prerequisites | What to verify first |
| --- | --- | --- |
| Fastbin/tcache poisoning | Repeated allocation through a modified free-list link | Exact list state, checks, alignment, and where the write occurs |
| Unsorted-bin disclosure | Read allocator pointers written into a freed chunk | Chunk was actually routed to unsorted, and you can read it afterward |
| Poison-null-byte / Einherjar | One byte changes adjacent size/consolidation interpretation | `prev_size`, in-use bits, valid neighbors, consolidation checks |
| Spirit | An attacker-shaped region is freed as a chunk | Alignment, headers, next-size checks, and accepted allocator path |
| Lore / stashing unlink | Controlled smallbin links affect later allocation writes | Reciprocal-link checks, tcache occupancy, exact write value |
| Classic unlink | A doubly linked list performs two linked writes | Both destinations remain valid; one write cannot be ignored |
| Force | Corrupted top size steers allocation on old runtimes | Target actually lacks the relevant top-size validation |
| Orange | Top-chunk behavior creates a free chunk without an explicit delete | Top end alignment, size constraints, allocator and FILE path |
| Largebin attack | Insertion manipulates an ordered-bin pointer write | Size ordering and all integrity checks for that libc |
| Tangerine and count corruption | Allocator state is steered across caching paths | Actual counter representation and allocation implementation |
| Custom talloc/nginx allocator | Pool/parent or free-list metadata directs allocation | Its own layout; glibc headers do not apply automatically |
| musl allocator | Different metadata and lifetime model | Exact musl generation and relevant integrity checks |

Old writeups often promise “deterministic” behavior based on a particular heap layout. Treat that as a claim about the original challenge environment. Reproduce allocation order, libc build, and output handling before relying on it.

## 10. FILE structures, callbacks, and modern targets

FILE corruption can change what stdio reads, writes, or dispatches. It is useful when a write primitive reaches `_IO_FILE` fields or a program's `FILE *`. Start with a **data effect**, such as a controlled leak, before trying a control-flow effect.

Map the exact fields used by the next call: flags, buffer bounds, write/read pointers, lock pointer, mode, vtable, and any wide-data pointer. `fclose`, flushing, allocation failure, and ordinary buffered input reach different paths. A fake object can fail before its intended callback because its lock or state is invalid.

The source's older fake-vtable attacks target old glibc. Later validation restricts acceptable vtable pointers; wide-data and legitimate-dispatch techniques have additional predicates and do not make all modern FILE objects interchangeable. “House of Apple” is a family label, not enough information to construct a working object.

A null byte in stdin's buffer pointer may move the next input operation into the FILE object itself; demonstrate the resulting write range in the debugger. A stdout leak needs correct buffer-pointer relationships and an output trigger. TLS destructors, `atexit` lists, pointer mangling, and application callbacks each have distinct layouts and invocation rules. A `setcontext` address is not a universal pivot: inspect the exact code and which base register it expects.

## 11. Seccomp and constrained shellcode

Begin with the allowed behavior. If the objective is reading a challenge file and `open/read/write` or suitable equivalents are permitted, an ORW chain may be enough. Never assume that a payload is “seccomp-safe” because it lacks the string `/bin/sh`.

**Kali, inspect locally:**

```bash
strace -f -o trace.log -e trace=prctl,seccomp,openat,read,write ./chall
rg -n 'seccomp|prctl|SIGSYS|EPERM|ENOSYS' trace.log
```

Trace output is evidence of tested calls, not a full policy listing. Recover the BPF filter from the supplied source, initializer data, or live setup arguments. `seccomp-tools` is not an individually approved executable in this workbook; do not rely on its source-repository installation command. Decode the policy with approved static tools and your own small parser when needed.

For each filter branch record architecture, syscall number, relevant argument, return action, and next branch. `KILL`, `TRAP`, `ERRNO`, and `ALLOW` produce different observations. Architecture checks matter because syscall numbers depend on ABI. x32 is an ABI and syscall-number convention; it is not synonymous with switching CPU execution to ordinary 32-bit x86. [Kernel seccomp documentation](https://docs.kernel.org/userspace-api/seccomp_filter.html) describes these policy semantics.

| ORW stage | Required invariant |
| --- | --- |
| Open | Exact NUL-terminated challenge path, permitted flags and syscall |
| Read | Use the returned descriptor; check for a negative error result |
| Write | Use the actual successful read count, not an assumed buffer size |
| Finish | Return or exit through an allowed path; retain a usable stack |

Direct `open` treats `*` literally; glob expansion belongs to a shell. Do not put `/flag*` in a raw file-open payload and expect wildcard expansion. A seccomp rule allowing `openat` may still restrict directory descriptors or flags. If a descriptor is already open, using it can avoid an unavailable open call, but verify its identity and offset.

For printable/alphanumeric/unique-byte shellcode, first list permitted bytes and execution permissions. Assemble locally with approved Kali NASM or an available approved assembly tool; inspect bytes and disassemble before execution. A small first-stage reader needs a valid destination, input descriptor, next control transfer, and enough remaining bytes for stage two. A `read` stub alone does not jump to the bytes it reads.

## 12. Integer, parser, VM, and race-condition primitives

| Symptom | Derive the actual bug | Useful bounded experiment |
| --- | --- | --- |
| Negative index accepted | Signed lower-bound check is missing | Evaluate `base + index * stride` and inspect target mapping |
| Length checked in one width, copied in another | Truncation/sign extension changes meaning | Test boundary values around 127/255/32767/65535 |
| `abs(INT_MIN)` used as index | The minimum signed value cannot be represented positively | Follow target compiler instructions and subsequent signedness |
| Floating input reaches raw memory | IEEE-754 conversion or bit reinterpretation | Compare packed bytes; distinguish NaNs, rounding and exact integers |
| Sorting changes an overflow payload | Input words are reordered before return | Model sort order and equal elements before building the stack |
| DNS compression / image/PCAP records | Nested length, count, offset or recursion is unchecked | Trace each length source through allocation and copy |
| JIT validates one program, runs another | Mutation or truncated branch offsets break validation | Compare bytecode at validation and execution time |
| GC releases a still-referenced object | Root/lifetime tracking is inconsistent | Record reference graph and exact collection trigger |
| File descriptor survives exec | Missing close-on-exec changes available capabilities | Check the inherited descriptor in the assigned sandbox |
| Two threads touch shared state | Check and use can observe different values | Establish an observable interleaving before repeated trials |

**Windows WSL Python, complete width example:**

```python
def signed16(value):
    value &= 0xffff
    return value - 0x10000 if value & 0x8000 else value

for original in [32767, 32768, 65535, 65536, -1]:
    print(original, 'as uint16=', original & 0xffff,
          'as int16=', signed16(original))
```

A large positive length can become negative or zero after narrowing. That is only exploitable if a later operation interprets it differently or trusts stale size state. C signed overflow is not generically defined wrapping arithmetic; reverse the emitted instructions before modeling it as modular arithmetic.

For custom VMs, separate guest memory from host state. A negative guest register index, unchecked dispatch index, truncated jump, or host-side `eval` can cross that boundary. Interpreter-level commands and language jail escapes have their own input rules; see the miscellaneous chapter when the main issue is a language sandbox rather than native memory.

Race experiments should have a measurable win condition and an attempt budget. A sleep merely changes timing; it does not prove the intended interleaving. Save the input and trace for a successful trial. Do not present a rare one-off crash as a reliable primitive.

## 13. Kernel and Windows extensions: advanced, environment-specific

Kernel exercises need the exact supplied kernel image, configuration, module, initramfs and launch script. Analyze these offline first. Do not load challenge modules into a competition host kernel or apply a kernel exploit to the workstation. `qemu-img` in the Kali workbook does not provide blanket approval for a system emulator; an organizer-provided kernel lab is a separate prerequisite.

**Kali radare2, static module review:**

```bash
rabin2 -I challenge.ko
rabin2 -s challenge.ko > module-symbols.txt
rabin2 -R challenge.ko > module-relocations.txt
rg 'ioctl|read|write|copy_|alloc|free|cred' module-symbols.txt module-relocations.txt
r2 challenge.ko
```

Inside radare2, run `aaa`, `afl`, and `pdf @ NAME`, replacing `NAME` with a discovered handler. Track `copy_from_user`/`copy_to_user` sizes, user-controlled offsets, object lifetime, locking, and error paths. A `.ko` is relocatable; its symbol offsets are not loaded kernel addresses.

| Kernel concept | What a usable chain must establish |
| --- | --- |
| KASLR / function-level randomization | The needed code/data addresses, with exact symbol-relative meaning |
| SMEP / SMAP | Whether supervisor code can execute/access user pages at the relevant point |
| KPTI | A valid, version-matched return to user mode with correct state |
| Kernel stack canary | Its observed value and which overwritten frame validates it |
| SLUB and per-CPU behavior | Correct cache, object size, lifetime and reuse on the tested CPU |
| Cross-cache / PTE overlap | Physical-page lifetime and reuse; similar virtual addresses prove nothing |
| `userfaultfd` or memory-fault races | Availability, permissions and a genuine blocking point |
| `tty_struct`, `seq_operations`, key payloads | Exact structure size/layout and the operation that dereferences a field |
| Credential/helper-path target | Applicable kernel version/configuration and the legitimate trigger |
| io_uring / eBPF verifier / hypercall | The precise interface and object lifetime or verifier/runtime disagreement |

Historical `addr_limit`/`set_fs` recipes apply to older kernels; current kernels may not have that mechanism. A `modprobe_path` or `core_pattern` overwrite depends on helper configuration and trigger behavior. Kernel-return trampoline offsets, structure sizes, and credential-call conventions must be measured against the supplied build. The source examples are study references, not portable exploits.

For **Windows native**, use approved x64dbg and HxD. Distinguish x86 SEH-chain techniques from x64 exception unwinding; they are not interchangeable. Verify DEP, ASLR, CFG, module imports, exception dispatch and stack layout for the actual executable. A valid CFG target alone does not guarantee useful arguments or a permitted call path. ROP chains must satisfy Windows calling conventions and shadow-space requirements.

The source's WinDbg/MCP and token-stealing workflows are excluded here because the tools are unapproved and the agent integration conflicts with event rules. Windows privilege exercises require an explicitly supplied challenge VM; they are not workstation troubleshooting steps.

## 14. Audit the repository scripts before adapting them

The five original Python files are **templates with unresolved assumptions**, not ready-to-run solvers. They all depend on pwntools and target-specific runtime files. The command-focused replacements above cover input, binary packing, offset measurement, and leak arithmetic without that dependency.

| Original source | Preserve this idea | Correct before reuse |
| --- | --- | --- |
| `ctf-pwn/scripts/ret2libc_two_stage.py` | Leak a library pointer, compute base, build a second stage | Replace offsets/gadgets/prompts; avoid `.strip()` on raw leaks; reconnect after a failed chain; verify pointer width and reentry |
| `ctf-pwn/scripts/fmtstr_payload_suite.py` | Compare byte and halfword write plans | Prove argument index, response framing, target permissions and intended destinations; the fallback win address and adjacent GOT entry are not generic |
| `ctf-pwn/scripts/seccomp_orw_generator.py` | Track file descriptor and scratch buffer across ORW | Its “x32” label does not create x32 syscalls; fixed-buffer writes may overrun valid data; no `/bin/sh` test proves seccomp compliance |
| `ctf-pwn/scripts/shellcraft_asm.py` | Generate then inspect architecture-specific code | A raw `open('/flag*')` does not glob; padding shellcode does not provide a return target; a read stage needs a transfer to stage two |
| `ctf-pwn/scripts/srop_execve.py` | Serialize a signal frame after a real trigger | `arb_read_gen` actually uses execve frames; `/bin/sh` is not placed by merely sending it; all frame/gadget/stack addresses require proof |

No original script was executed against a target in preparing this handbook. The source's broad success and reliability claims were not reproduced. Keep this distinction in your own notes as well.

## 15. Troubleshooting by the first failed invariant

| Failure | Inspect first |
| --- | --- |
| Crashes before your chosen return | Canary, corrupted saved registers, input parser or earlier pointer use |
| Return reaches wrong address | Endianness, pointer width, PIE base, partial overwrite and consumed newline |
| Correct function but no useful result | Calling convention, argument lifetime, stack alignment and program state |
| Local works, supplied service fails | libc/loader identity, ASLR, environment, buffering, limits and protocol framing |
| Heap aborts in `free` | Exact chunk header, allocator version, duplicate reference, neighboring chunk consistency |
| GOT write faults | Actual memory permissions and the correct relocation slot |
| SIGSYS or silent syscall failure | Architecture-aware seccomp branch and return action |
| EOF after a leak | Whether the first stage returns to a valid read loop |
| Intermittent partial overwrite | Which unknown address bits remain and your measured success rate |
| “Success” without challenge output | Verify the real objective; decoy files and messages exist |

Before calling a solve repeatable, start from a fresh local process, rebuild only from measured inputs, and confirm the intended challenge result. Save a compact trace: input bytes, crucial leak, base calculation, control-flow proof, and final output. The separate practice atlas preserves all 43 `pwnable-tw` cases as exercises with their own prerequisites rather than universal payloads.

Source map: `ctf-pwn/SKILL.md`, `ctf-pwn/attack-playbook.md`, `ctf-pwn/static-signals.md`, `ctf-pwn/overflow-basics.md`, `ctf-pwn/rop-and-shellcode.md`, `ctf-pwn/rop-advanced.md`, `ctf-pwn/format-string.md`, `ctf-pwn/heap-techniques.md`, `ctf-pwn/heap-techniques-2.md`, `ctf-pwn/heap-fsop.md`, `ctf-pwn/advanced.md`, `ctf-pwn/advanced-exploits.md`, `ctf-pwn/advanced-exploits-2.md`, `ctf-pwn/advanced-exploits-3.md`, `ctf-pwn/advanced-exploits-4.md`, `ctf-pwn/advanced-exploits-5.md`, `ctf-pwn/sandbox-escape.md`, `ctf-pwn/kernel.md`, `ctf-pwn/kernel-techniques.md`, `ctf-pwn/kernel-bypass.md`, and `ctf-pwn/field-notes.md`. Detailed case-specific payloads remain historical source material; advanced AI/ML, unapproved-tool, and external-target workflows are not competition instructions.


---

<a id="09-malware"></a>

# Malware analysis and configuration recovery

The first objective is usually a small, concrete answer: a configuration value, decoded payload, encryption key, persistence location, or reconstructed conversation. Find the data flow that produces it before considering execution.

## Approved analysis routes

**Windows native:** HxD, x64dbg, dnSpyEx (Windows workbook rows 42, 40, 45). **WSL:** Python 3, objdump, strings, Ghidra, Volatility 3 (Windows rows 14, 17, 18, 29, 38). **Kali:** capa, FLOSS, oletools, jadx, pyinstxtractor-ng, YARA, strace/ltrace (Kali rows 26, 50, 105, 79, 118, 164, 145/90).

Each approval applies to its listed environment. Use installed versions/help; optional rules, plugins, symbol files, and third-party unpackers are not automatically included. AI interfaces, public malware uploads, and online decompilers are prohibited by the [event rules](https://ajccbc.ncsa.or.th/cyber-sea-game-2026/) and Unapproved rows 51–52. Dissect is explicitly unapproved (row 21), so the source's `dissect.cobaltstrike` recipe is not used here.

## Static triage

`sample.bin` is a local challenge-supplied file. Hash it and keep an untouched copy. **Windows PowerShell:**

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath .\sample.bin
```

**WSL:**

```bash
xxd -l 256 sample.bin
strings -a -n 6 sample.bin > strings-ascii.txt
strings -a -e l -n 6 sample.bin > strings-utf16.txt
objdump -f sample.bin
objdump -x sample.bin > headers.txt
```

**Kali**, if those corresponding tools are present:

```bash
file sample.bin
capa sample.bin
floss sample.bin
```

Expected result: architecture/file type, imports, section layout, interesting strings, and candidate capabilities. High entropy can mean compression, encryption, or ordinary media. A capability match is a lead, not proof that a function executed.

Open a native binary in approved Ghidra. Run auto-analysis, search for the interesting string, inspect cross-references, and decompile its callers. Rename the decryptor and annotate key/IV/blob sources. Read assembly when decompiler types or control flow are misleading. Record whether integer operations wrap at 8, 16, or 32 bits.

## Decode scripts without executing them

Replacing `eval` with `print` does not neutralize code that runs before the eval. Extract literals and reproduce their transformations in a separate script. Do not dot-source a PowerShell file, import a suspicious Python module, or run `npm install` on a malicious package to inspect it.

**Windows PowerShell**, decode only a copied `-EncodedCommand` value saved to `encoded.txt`:

```powershell
$encoded = (Get-Content -Raw -LiteralPath .\encoded.txt).Trim()
$decoded = [Text.Encoding]::Unicode.GetString([Convert]::FromBase64String($encoded))
Set-Content -LiteralPath .\decoded.ps1.txt -Value $decoded -Encoding UTF8
```

Expected result: readable UTF-16LE PowerShell text. If it is gibberish, check that you extracted only the literal, then inspect whether it was UTF-8 or compressed. Keep the `.txt` suffix to discourage accidental execution.

For a Base64 layer containing gzip or zlib, **WSL**, save as `decode_layer.py`:

```python
from pathlib import Path
import base64, zlib

encoded = ''.join(Path('encoded.txt').read_text().split())
raw = base64.b64decode(encoded, validate=True)
Path('layer1.bin').write_bytes(raw)
if raw.startswith(b'\x1f\x8b'):
    mode = 31  # gzip wrapper
elif len(raw) >= 2 and (raw[0]*256 + raw[1]) % 31 == 0 and raw[0] & 15 == 8:
    mode = 15  # plausible zlib wrapper; still requires validation
else:
    print('no supported compression wrapper; inspect layer1.bin')
    raise SystemExit
dec = zlib.decompressobj(mode)
out = dec.decompress(raw, 16_000_001)
if len(out) > 16_000_000 or dec.unconsumed_tail:
    raise ValueError('output limit reached')
assert dec.eof, 'incomplete compressed stream'
Path('layer2.bin').write_bytes(out)
print('decoded bytes:', len(out), 'unused trailing bytes:', len(dec.unused_data))
```

For JS `String.fromCharCode`, parse only literal numeric arrays; `fromCharCode` emits UTF-16 code units rather than unrestricted Unicode codepoints. For `%xx`, use `urllib.parse.unquote_to_bytes`; JS `unescape` additionally handles `%uXXXX`. For Python literals use `ast.literal_eval`, not `eval`; marshal/code objects require version-aware disassembly and must not be executed.

**Kali** beautification is available (row 82): `js-beautify suspicious.js -o readable.js`. Beautification preserves behavior; it is not a safety sandbox. Search for string tables, index rotations, function constructors, and decode chains, then lift just the pure transformations.

## Packages, office macros, and trojanized plugins

**Kali**, `7z` row 9 and oletools row 105:

```bash
7z l package.deb
7z x package.deb -opackage-parts
oleid document.docm
olevba document.docm > macro-report.txt
```

Inspect `control.tar.*` for `preinst/postinst/prerm/postrm`; inspect data archive paths without running package installation. A plugin can hide activation code in an exception handler, setup hook, or import side effect. Compare with a supplied known-good release using **Kali Git**, row 56:

```bash
git diff --no-index -- known-good/plugin.py suspect/plugin.py
```

Exit code 1 means differences were found. Follow added network calls and decode wrappers. An offline custom-alphabet decoder, **WSL**:

```python
from pathlib import Path
alphabet = '0123456789abcdefghijklmnopqrstuvwxyz-.'
shift = 13  # derive from the sample
encoded = Path('domain-encoded.txt').read_text().strip()
assert all(c in alphabet for c in encoded)
decoded = ''.join(alphabet[(alphabet.index(c)-shift)%len(alphabet)] for c in encoded)
print(decoded)
```

For macro-encoded cells, preserve traversal order and reverse the exact arithmetic. If the macro stores `3*byte+78`, require `(value-78)%3 == 0` and result in `0..255` before writing bytes. This avoids silently accepting an incorrect formula. Do not enable the document's macros to obtain the output.

## PE resources, .NET, and Python bundles

Use `objdump -s -j .rdata sample.exe` in **WSL** for a selected PE section. In Ghidra, trace resource-loading APIs and the code that consumes the resource. If extracting with WSL non-AI `pefile`, distinguish RVA from file offset; `pe.get_data(rva,size)` performs that translation. Virtual-size padding and overlays are separate from raw section bytes.

On **Windows**, open managed assemblies in dnSpyEx. Search for `FromBase64String`, cipher constructors, `Dns`, `TcpClient`, registry writes, and static initialization. Follow configuration fields to their decryptor; a plausible C2 string in resources can be a decoy. Export the encrypted bytes and key source as data, then decode locally.

For an observed MD5-password + IV-prefixed AES-CBC construction, **WSL** with non-AI PyCryptodome permitted by Windows row 14:

```python
from pathlib import Path
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib

password = Path('key-source.bin').read_bytes()  # exact bytes, no implicit stripping
data = Path('encrypted-config.bin').read_bytes()
assert len(data) >= 32 and (len(data)-16)%16 == 0
key = hashlib.md5(password).digest()  # only if the sample uses MD5 digest bytes
plain = unpad(AES.new(key,AES.MODE_CBC,iv=data[:16]).decrypt(data[16:]),16)
Path('config.txt').write_bytes(plain)
print(repr(plain))
```

Padding success alone has false positives. Verify structure, key names, lengths, and any authentication tag. A sample may use hexadecimal digest text instead of digest bytes. The historical LimeRAT recipe `MD5[:15] + MD5 + NUL` is one 32-byte derivation, not a universal LimeRAT rule; reproduce the exact decompiled byte-copy operations.

**Kali** Python bundle tools (rows 118, 117, 152):

```bash
pyinstxtractor-ng --help
pyinstxtractor-ng sample.exe
pycdc recovered.pyc > recovered.py
uncompyle6 recovered.pyc > recovered-legacy.py
```

Use the extractor's actual output directory and interpreter version. A decompiler error often means unsupported bytecode, not missing content. Extracted `.pyc` files may need correct version headers. Do not assume pycdc supports every recent Python version, or install an unlisted PyArmor unpacker. When protected code cannot be recovered statically, identify resources/configs and use supplied memory evidence.

For Android samples, **Kali jadx** (row 79): `jadx -d decoded sample.apk`. Inspect the manifest for exported receivers/services and startup triggers, then code references to network methods. Searching only `strings.xml` misses Java/Kotlin string literals. JNI/native libraries continue through the native reversing route.

## C2 decoding: reconstruct first, decrypt second

Use the network chapter's direction-aware reassembly. Record each message's length, direction, sequence number, nonce/IV, and cipher reset behavior. TLS decryption, WebSocket unmasking, application framing, and application encryption are separate layers. Wireshark **Decode As** can recognize a nonstandard TLS port without rewriting packet ports.

For RC4, determine whether state resets per message or continues across the stream. A compact **WSL** implementation for a verified single stream:

```python
from pathlib import Path
def rc4(key, data):
    if not key: raise ValueError('empty key')
    s,j = list(range(256)),0
    for i in range(256):
        j = (j+s[i]+key[i%len(key)]) & 255
        s[i],s[j] = s[j],s[i]
    i=j=0; out=bytearray()
    for byte in data:
        i=(i+1)&255; j=(j+s[i])&255
        s[i],s[j]=s[j],s[i]
        out.append(byte ^ s[(s[i]+s[j])&255])
    return bytes(out)
key = Path('rc4-key.bin').read_bytes()
plain = rc4(key,Path('ciphertext.bin').read_bytes())
Path('decrypted.bin').write_bytes(plain)
print(repr(plain[:200]))
```

A first 32-byte packet is a key only if sample logic confirms that design. “Concatenate both directions chronologically” is valid only for an unusual protocol explicitly sharing state; most protocols have independent direction state. For rotating passwords, reconstruct time bucket/sequence units and timezone from implementation and capture timestamps.

Crypto clues: RC4 initializes a 256-byte permutation; ChaCha uses `expand 32-byte k`; AES often contains S-box constants; TEA/XTEA often uses `0x9E3779B9`. Constants alone do not identify mode, key derivation, or padding. For Camellia-based samples, inspect **WSL OpenSSL** `openssl list -cipher-algorithms`; PyCryptodome does not supply the source's invented `Crypto.Cipher.Camellia` module. Verify mode/block framing before using a locally supported primitive.

RAT-specific leads: DarkComet-like logs may exist in `%APPDATA%\dclogs\*.dc`; inspect memory file objects and Run keys. Beacon-like samples often store structured configuration values; decode XOR wrappers and trace configuration parsing in Ghidra. Timing, URI names, and a familiar port do not prove a malware family. Recovered Telegram tokens stay evidence: do not call live bot APIs or retrieve third-party messages.

## Memory and controlled runtime work

Use supplied memory dumps first. **WSL Volatility 3**, with existing matching symbols only:

```bash
vol --offline -f memory.dmp windows.pstree
vol --offline -f memory.dmp windows.psscan
vol --offline -f memory.dmp windows.cmdline
vol --offline -f memory.dmp windows.netscan
vol --offline -f memory.dmp windows.malfind
```

Check `vol --help` for current plugin names. Symbol ZIPs are unavailable (Unapproved row 82). Suspicious executable private memory can suggest injection; JIT runtimes also legitimately create executable regions. Correlate contents, mapped files, threads, and process ancestry. `malfind` is a heuristic, not a complete detector.

On approved **Windows x64dbg**, a justified runtime inspection belongs in an organizer-provided disposable analysis environment with network isolation. WSL, Wine, a timeout, or `strace` alone does not isolate malware from your files or network. Set breakpoints at allocation/decryption handoff, inspect the resulting buffer in the Dump view, and save only the relevant region for static analysis. Follow injection API chains as evidence; you do not need to reproduce injection against another process.

For a permitted isolated Linux runtime, **Kali**:

```bash
strace -f -s 256 -e trace=network,file -o trace.log ./sample
ltrace -f -o library-trace.log ./sample
```

These commands execute the sample. If that environment is absent, continue static/dump analysis. No dynamic execution is required merely because a sample contains an environment check.

For raw shellcode, **WSL**:

```bash
objdump -D -b binary -m i386:x86-64 -M intel shellcode.bin
```

Set the correct architecture before interpreting output. A decoder loop's XOR/subtract operations wrap modulo 256: `((byte-0x32)&255) ^ key[i%len(key)]`. Preserve exact key bytes, including newlines. Junk push/pop sequences may alter flags or fault; confirm data/control dependencies before deleting them from an analysis model.

## Local indicators and API hashes

**Kali YARA**, row 164. Save as `case.yar`:

```yara
rule Case_Config_Lead {
    strings:
        $a = "challenge-marker" ascii wide
        $b = "cmd.exe /c" ascii wide nocase
    condition:
        $a and $b
}
```

```bash
yara -s case.yar sample.bin
yara -s case.yar memory.dmp
```

Replace `challenge-marker` with a distinctive recovered string. Broad “not MZ” rules match almost every non-PE file and are not useful evidence. Retain matching offsets for follow-up extraction.

For API hashing, export names from relevant challenge DLLs and compute the **sample's** hash locally. A common ROR13-add hypothesis:

```python
from pathlib import Path
def api_hash(name):
    h=0
    for c in name.encode('ascii'):
        h=((h>>13)|(h<<19))&0xffffffff
        h=(h+c)&0xffffffff
    return h
target=0x12345678  # comparison constant from the sample
for name in Path('exports.txt').read_text().splitlines():
    if api_hash(name)==target: print(name)
```

Check name casing, terminating NUL, DLL-name inclusion, and seed. Hash collisions require validating the resolved API's arguments/call sites. No online hash database is needed.

Source material adapted: all five files in `ctf-malware/`. The useful manual decompiler/debugger reasoning from `tools-mcp.md` was retained; agent calls and unsupported debuggers were removed. Live bot access, ARP interception/RST injection, unapproved parser packages, and public sandbox uploads were excluded.


---

<a id="10-osint"></a>

# OSINT from supplied evidence

Build an evidence trail from a clue to an answer. Preserve exact identifiers, original text, dates, and uncertainty. A matching username, reused photograph, or hosting IP is a lead; it does not independently establish identity or location.

This chapter emphasizes local files and organizer-provided material. Use the handbook's competition rules before consulting external sites. Do not upload challenge images to reverse-image services, use face recognition, contact people or bots, or treat a recovered token as permission to access an account.

## Environment and local inventory

**Windows native:** Chrome and a PDF viewer, Windows workbook rows 12 and 10. **WSL:** Python 3, ExifTool, pdftotext, strings (Windows rows 14, 21, 22, 18). **Kali:** Git, ripgrep, ImageMagick, SQLite, MediaInfo (Kali rows 56, 126, 74, 138, 94). Keep those environments distinct; a Kali tool is not automatically installed in WSL.

Use a notebook or CSV with these columns:

```text
clue_id,source_file,source_offset_or_page,observation,hypothesis,confidence,next_check
```

Example observation: “profile-export.json contains account ID 123 and display name Harbor.” Hypothesis: “Harbor is the account's current alias.” The number is more stable than a display name, but exported metadata can still be fabricated.

**Kali**, search a supplied evidence directory without contacting its links:

```bash
rg -n -i 'username|handle|author|identifier|location|latitude|longitude' evidence
rg -n -i 'https?://|mailto:|t\.me/|github\.com/' evidence
```

**WSL**, inspect media metadata and PDF text:

```bash
exiftool -a -u -g1 evidence/photo.jpg
exiftool -GPSLatitude -GPSLongitude -GPSLatitudeRef -GPSLongitudeRef -n evidence/photo.jpg
pdftotext -layout evidence/document.pdf document.txt
strings -a -n 6 evidence/blob.bin > blob-strings.txt
```

Expected result: concrete coordinates, timestamps, embedded names, document titles, or linked identifiers. Metadata can be edited or stripped; absence is not proof of deception. Do not assume every social platform always removes every metadata field.

## Parse saved pages and JSON

Saved HTML may include richer JSON-LD or application state than the visible page. In Chrome, open a **copy** only if its active-content behavior is understood; otherwise read as text. Search for `application/ld+json`, `author`, `identifier`, `content`, and media URLs. Keep archived fetch date separate from the page's claimed publication date.

This **WSL standard-library** script extracts link targets and script blocks from a local saved page. It does not fetch them. Save as `page_extract.py`:

```python
from html.parser import HTMLParser
from pathlib import Path

class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.blocks=[]; self.current=None
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        for key in ('href','src'):
            if key in attrs: self.links.append((tag,key,attrs[key]))
        if tag=='script': self.current=[attrs.get('type',''),[]]
    def handle_data(self,data):
        if self.current is not None: self.current[1].append(data)
    def handle_endtag(self,tag):
        if tag=='script' and self.current is not None:
            self.blocks.append(self.current); self.current=None

p=Page(); p.feed(Path('page.html').read_text(encoding='utf-8',errors='replace'))
for item in p.links: print(item)
out=Path('page-scripts'); out.mkdir(exist_ok=True)
for i,(kind,chunks) in enumerate(p.blocks):
    (out/f'{i:03d}.txt').write_text(''.join(chunks),encoding='utf-8')
    print(i,kind)
```

Read extracted JSON with `python3 -m json.tool page-scripts/000.txt` when that block is actual JSON. JavaScript assignments are not JSON; extract the value deliberately rather than executing the block. An HTTP 200 status can be a login wall or generic “not found” page; compare body content and stable identifiers.

## Aliases, social exports, and timestamps

In supplied profile exports, correlate numeric IDs, explicit cross-links, avatar history, post IDs, and dates. Same handles on different platforms are not identity proof. Numeric suffixes could be postal codes, years, random numbers, or deliberate misdirection; test alternatives against independent evidence.

For a Twitter-style Snowflake **known to use that scheme**, decode its creation timestamp locally:

```python
from datetime import datetime,timezone
snowflake=1234567890123456789  # replace with the observed numeric ID
milliseconds=(snowflake>>22)+1288834974657
print(datetime.fromtimestamp(milliseconds/1000,timezone.utc).isoformat())
```

Discord uses a different epoch; other services use entirely different ID schemes. A calculated timestamp does not prove an account belongs to a person. Retain the original identifier alongside the derived time.

For saved social-media datasets, inspect all supplied posts/replies, bios, playlist descriptions, role names, emoji frames, and image variants. Short-duration GIF frames can hide text; use the steganography chapter's animation workflow. Preserve playlist/album order when testing acrostics. For gaming data, include realm/server and character IDs; a character name without server context is ambiguous.

A supplied fitness route can identify a **challenge location** from its path and landmarks. Do not infer or expose a real person's home from privacy-zone boundaries. Use the exact endpoint/waypoint requested by the challenge, and distinguish a route from the camera position.

## Unicode and encoded clues

Before normalizing text, list its codepoints. Homoglyph encodings often mix Latin and Cyrillic lookalikes, but emoji, accents, and smart punctuation are not automatically secret bits. **WSL:**

```python
from pathlib import Path
import unicodedata
text=Path('post.txt').read_text(encoding='utf-8')
for i,c in enumerate(text):
    print(i,repr(c),f'U+{ord(c):04X}',unicodedata.name(c,'CONTROL'))
pairs={'a':'\u0430','e':'\u0435','o':'\u043e','p':'\u0440','c':'\u0441','x':'\u0445'}
zeros=set(pairs); ones=set(pairs.values())
bits=''.join('0' if c in zeros else '1' for c in text if c in zeros|ones)
for shift in range(8):
    b=bits[shift:]
    data=bytes(int(b[i:i+8],2) for i in range(0,len(b)-7,8))
    print(shift,repr(data))
```

The explicit alphabet is a hypothesis; change it only with evidence. Whole-text ASCII/non-ASCII encoding is a different scheme and includes spaces/punctuation differently. Record the choice so someone else can reproduce it.

For a Base58 clue, preserve leading `1` characters as leading zero bytes:

```python
from pathlib import Path
alphabet='123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
s=Path('base58.txt').read_text().strip()
number=0
for ch in s: number=number*58+alphabet.index(ch)
zeroes=len(s)-len(s.lstrip('1'))
decoded=b'\0'*zeroes+number.to_bytes((number.bit_length()+7)//8,'big')
print(repr(decoded))
```

Validate a Base58Check checksum when the format requires one. Strings of 32/40/64 hexadecimal characters can be MD5/SHA-1/SHA-256, but may also be random IDs, Tor fingerprints, keys, or data. Length is a classification clue, not a definitive algorithm detector.

## Geolocation without image uploads

Make an observation sheet before choosing a country: readable sign fragments, writing systems, road numbers, driving side, rail crossings, building layout, terrain, coastline, shadows, and unique small objects. Generic architecture and vegetation should carry low confidence. A Cyrillic sign does not uniquely identify Russia, and motorway sign colors vary by road class; the source's one-feature country table was too strong.

**Kali ImageMagick**, row 74, makes local inspection copies:

```bash
magick photo.jpg -crop 600x300+120+80 +repage -resize 200% sign.png
magick sign.png -flop mirrored-sign.png
magick sign.png -colorspace Gray -auto-level contrast-sign.png
```

The crop is `width×height+x+y`; measure it on the image. `-flop` mirrors horizontally. Use nearest-neighbor scaling for pixel grids; ordinary photo inspection can use other interpolation. Preserve the original and record transformations. Do not invent illegible letters; keep alternate readings in the notes.

Compare candidate photographs/maps already supplied by the organizer. Verify at least two independent scene constraints: building alignment plus road geometry, or sign plus coastline. For exact viewpoint tasks, match camera position using foreground poles, paths, bollards, and the relative alignment of distant buildings. The subject's coordinate can differ substantially from the camera's.

For newspaper or product clues, use supplied catalogs/archives: record publication date, page number, headline, model number, voltage/capacity, and dimensions. A matching brand without the exact model is insufficient. For a series of music landmarks, solve locations first, then assemble the per-image key numbers in the specified order; do not adjust uncertain locations merely to force readable ASCII.

## Coordinates and local spatial checks

Latitude/longitude order and hemisphere signs are frequent errors. Decimal degrees are not degrees-minutes-seconds. An MGRS string includes zone, latitude band, grid square, and equally precise easting/northing digits; do not treat it as a decimal coordinate. A short Plus Code needs a reference locality; a full Open Location Code does not. What3Words is a distinct system and cannot be converted using a guessed word grid.

When non-AI Python libraries are needed in **WSL**, Windows row 14 permits them except explicit exclusions; use a documented coordinate conversion library only after checking its input/output convention. Do not assume public conversion websites are an approved analysis route. If the required proprietary lookup is unavailable, preserve the verified coordinates and state the conversion dependency.

For a supplied `places.csv` with `name,lat,lon`, this **WSL** script ranks locations near a clue coordinate using a spherical distance:

```python
import csv,math
latitude,longitude=13.7563,100.5018  # replace with clue coordinates
def distance(lat,lon):
    a,b=map(math.radians,(latitude,lat))
    dlat=b-a; dlon=math.radians(lon-longitude)
    h=math.sin(dlat/2)**2+math.cos(a)*math.cos(b)*math.sin(dlon/2)**2
    return 6371000*2*math.asin(min(1,math.sqrt(h)))
rows=[]
with open('places.csv',newline='',encoding='utf-8') as f:
    for row in csv.DictReader(f):
        rows.append((distance(float(row['lat']),float(row['lon'])),row['name']))
for metres,name in sorted(rows)[:20]: print(round(metres,1),name)
```

Expected result: a candidate list, not a final match. Ten metres may be smaller than the map's coordinate error. For a supplied OSM JSON export, filter `elements[].tags` for `shop`, `amenity`, `railway`, and `tourism`, then compare proximity locally. Ways may need geometry/centroids; a node-only export can omit the desired business entirely.

## DNS, registration, archives, and infrastructure

Start with supplied DNS captures, zone files, WHOIS/RDAP exports, certificate records, or archive indexes. Extract TXT/CNAME/MX records and preserve answer timestamps/TTL. TXT records can consist of multiple strings within one record: join those in order, but do not merge independent answers arbitrarily.

A stored archive index can reveal old URLs and date ranges; an archived snapshot's timestamp is the crawl time, not the original publication time. Compare saved old/new pages for changed aliases and links. For saved Google Docs/Sheets exports, preserve document IDs and sheet IDs; a private-access response is not a puzzle to bypass.

Registrars, shared name servers, shared IPs, and ASNs are infrastructure correlations, not ownership proof. IP geolocation may point to a provider, VPN, or coarse regional estimate. A reused SSH host key or certificate can indicate a reused image/configuration rather than one physical server. Tor relay fingerprint/family data in a supplied export can support chronology, but does not identify a user.

Active DNS queries, zone transfers, service fingerprinting, and scanning belong only to a challenge-designated target and the permitted tools for that machine. This offline chapter does not turn a public hostname found in evidence into an attack target. Do not copy the historical cross-challenge infrastructure-pivot advice into event practice.

## Repository and file-metadata pivots

**Kali Git**, row 56, on a supplied local repository:

```bash
git -C repo log --all --format='%H %aI %an <%ae> %cn <%ce>'
git -C repo log --all --diff-filter=D --name-status
git -C repo log --all -p -- '*.private' '*.key' '*.txt'
git -C repo show COMMIT:path/to/file
```

Replace `COMMIT` with an observed ID. Examine `.mailmap`, README links, contributors, commit messages, and supplied issue/review exports. Author/committer fields are user-controlled; most Git history is not cryptographically signed. Even a valid signature needs a trusted key-to-identity link.

For a supplied `.DS_Store`, inspect filenames with a permitted local non-AI parser in WSL; Finder metadata indicates names seen in a directory, not contents or necessarily current files. Do not recursively fetch discovered paths from unrelated sites. For TTF remapping clues, a non-AI `fontTools` script can inspect cmap and glyph contours locally; contour matching works best against the exact reference font and normalization, not any arbitrary standard font.

## Finish the chain

For each answer component, record the source, exact observation, transformation, and independent confirmation. Keep rejected hypotheses too when they explain ambiguity. A final location should state whether it is a building, camera point, route waypoint, or coordinate grid cell, with the requested precision.

Source material adapted: all five files in `ctf-osint/`. Agent automation, paid/API-key services, public image uploads, face recognition, credentialed Discord enumeration, live bot interaction, invasive location inference, and cross-challenge pivots were excluded. Their underlying local evidence-reading methods are retained where useful.


---

<a id="11-miscellaneous"></a>

# Miscellaneous: turn unfamiliar artifacts into a small model

“Misc” is a repository label, not one of the event's six official categories. Its material often belongs to cryptography, forensics, network analysis, steganography, reverse engineering, or a web challenge. Use the artifact and intended operation to choose the next step.

This chapter covers layered encodings, symbolic puzzles, jails, games, audio/RF data, and challenge navigation. Work only on supplied files and assigned challenge services. A challenge container escape is not authorization to modify the organizer's Kali host, workstation, or scoring platform.

## 1. Platform map

| Task | Windows/WSL route | Organizer Kali route |
|---|---|---|
| Decode bytes or solve small puzzles | WSL Python 3 standard library | Python 3; check actual interpreter |
| QR scanning | Listed WSL ZBar | Use a provisioned approved scanner if available; do not assume Windows tools are duplicated |
| Inspect bytes | Windows HxD or WSL xxd | Listed file, local editor, Python |
| Audio/spectrogram | Standard-library WAV inspection below | Listed Audacity, Sonic Visualiser, FFmpeg, SoX |
| Source search | Editor or Python file reads | Listed ripgrep |
| Constraints | Small Python enumeration; permitted non-AI library if added under Windows-sheet policy | Use a provisioned library; installation permission is not inferred |
| Interactive protocol | Python socket to the assigned host | Python socket or listed Ncat |

There is no all-tools installation command. Check the exact dependency for the next step. The Windows sheet permits non-AI Python libraries; it does not make rejected tools or AI/ML libraries acceptable. Do not use online decoders, compilers, or analysis services for challenge material.

## 2. Preserve the original and inspect the representation

Save as `inspect_bytes.py`, then run `python3 inspect_bytes.py artifact.bin`:

```python
from pathlib import Path
from collections import Counter
import hashlib
import math
import sys

data = Path(sys.argv[1]).read_bytes()
counts = Counter(data)
entropy = -sum((n/len(data))*math.log2(n/len(data)) for n in counts.values()) if data else 0
print('bytes:', len(data))
print('sha256:', hashlib.sha256(data).hexdigest())
print('first64 hex:', data[:64].hex())
print('first64 repr:', repr(data[:64]))
print('byte entropy:', round(entropy, 3))
```

High entropy suggests compressed, encrypted, or naturally varied data; it does not identify which. A known magic header plus a mismatched extension is more useful than entropy alone. Keep transformed outputs under new names so you can reverse a mistaken branch.

**Kali only:** `file artifact.bin` provides another format hypothesis. Check the actual bytes before trusting an extension or a single tool label.

## 3. Decode one layer with a reason

| Appearance | Candidate | Confirm before decoding again |
|---|---|---|
| Even number of hex digits | Hex bytes | Decoded length halves; inspect header |
| Alphabet/base64 padding | Base64 | Strict decoder accepts it; inspect bytes |
| A–Z and 2–7 | Base32 | Padding/case rules match |
| `%xx` sequences | URL encoding | Distinguish bytes from Unicode text |
| `\xNN`, `\uNNNN` | Language/string escapes | Decode according to the source language |
| Two decimal digits per byte | BCD | Each nibble must be 0–9 |
| Mostly invisible Unicode | Tags/variation selectors/zero-width marks | Print code points, not rendered text |
| Numeric columns | ASCII, coordinates, or samples | Check ranges and column meaning |

Save as `encoding_toys.py`:

```python
import base64
import codecs
from urllib.parse import unquote_to_bytes

original = b'CTF{layers}'
encoded = base64.b64encode(original.hex().encode()).decode()
stage1 = base64.b64decode(encoded, validate=True)
stage2 = bytes.fromhex(stage1.decode('ascii'))
assert stage2 == original
assert unquote_to_bytes('CTF%7Blayers%7D') == original
assert codecs.decode(codecs.encode('hello', 'rot_13'), 'rot_13') == 'hello'
print(encoded)
print(stage1)
print(stage2)
```

The order matters: base64 decoding reveals hex text, then hex decoding reveals the flag-shaped toy. Do not feed arbitrary strings to `eval` to “decode” them.

### Unicode tags and variation selectors

Save as `unicode_inspect.py`, then run it on a UTF-8 text file:

```python
from pathlib import Path
import sys
import unicodedata

text = Path(sys.argv[1]).read_text(encoding='utf-8')
tags = []
selectors = []
for position, char in enumerate(text):
    point = ord(char)
    if point > 127 or not char.isprintable():
        print(position, f'U+{point:04X}', unicodedata.name(char, 'UNNAMED'))
    if 0xE0020 <= point <= 0xE007E:
        tags.append(point-0xE0000)
    # A common byte mapping, not a universal Unicode steganography standard.
    if 0xFE00 <= point <= 0xFE0F:
        selectors.append(point-0xFE00)
    elif 0xE0100 <= point <= 0xE01EF:
        selectors.append(point-0xE0100+16)
print('tag ASCII:', bytes(tags))
print('selector bytes:', bytes(selectors))
```

The tags block and variation-selector mapping are different encodings. Confirm the producer's convention. Zero-width characters can encode bits with a custom alphabet; enumerate symbols first. UTF-16 endianness reversal instead acts on byte pairs, so retain original bytes rather than copying rendered text.

### Floats, Gray code, and BCD

Save as `numeric_encodings.py`:

```python
import struct

raw = b'ABCD'
value = struct.unpack('<f', raw)[0]
assert struct.pack('<f', value) == raw
print('float carrying four bytes:', value)

def gray_to_binary(gray):
    result = gray
    while gray:
        gray >>= 1
        result ^= gray
    return result

for n in range(256):
    assert gray_to_binary(n ^ (n >> 1)) == n
print('Gray-code checks passed')

packed = bytes([0x12, 0x34, 0x56])
digits = ''
for byte in packed:
    hi, lo = byte >> 4, byte & 15
    assert hi < 10 and lo < 10
    digits += str(hi) + str(lo)
assert digits == '123456'
print(digits)
```

A decimal float text dump may have rounded away the original bits. IEEE-754 endian choice and width matter. Gray code requires cumulative XOR, not simply reading the Gray-coded integer as binary. Packed BCD is not hexadecimal ASCII.

## 4. Archive and polyglot puzzles

List contents before extraction. Nested archives may hide a password or next filename in metadata, comments, or a previous layer. Do not blindly recurse without depth, size, and path limits.

**Kali only**, for the listed archive tools:

```bash
7z l challenge.zip
unzip -l challenge.zip
```

For a ZIP on either Python environment, use `zipfile.ZipFile(...).infolist()` to inspect names, compressed/uncompressed lengths, and comments. The web chapter includes a path/symlink inspector. Extract into a fresh challenge directory only after reviewing traversal and total size.

PNG/JAR/ZIP, JPEG/HTML, and WAV/polyglot formats exploit parsers that read different regions. Identify where each parser starts and stops. Appended ZIP data may be visible to an archive reader even when an image viewer ignores it. Do not execute an embedded JAR or program merely because an image opened successfully.

RTF custom tags and SMS PDU payloads need format-aware extraction. Preserve escape sequences, record PDU user-data length and encoding, and reassemble concatenated SMS parts by their reference/sequence fields. Ordinary UTF-8 decoding is not a substitute for GSM 7-bit unpacking.

## 5. QR reconstruction and other visual alphabets

Determine the module grid, orientation, polarity, and quiet zone. A normal QR has three finder patterns and timing patterns; decorative image pixels are not necessarily modules. Rotate/flip only with a record of each transformation.

For a text file of `0`/`1` module rows, save `grid_to_pgm.py`:

```python
from pathlib import Path
import sys

rows = [line.strip() for line in Path(sys.argv[1]).read_text().splitlines() if line.strip()]
assert rows and all(len(row) == len(rows[0]) for row in rows)
assert all(set(row) <= {'0', '1'} for row in rows)
scale, quiet = 8, 4
height, width = len(rows), len(rows[0])
out_w, out_h = (width+2*quiet)*scale, (height+2*quiet)*scale
pixels = bytearray()
for y in range(out_h):
    for x in range(out_w):
        gx, gy = x//scale-quiet, y//scale-quiet
        dark = 0 <= gx < width and 0 <= gy < height and rows[gy][gx] == '1'
        pixels.append(0 if dark else 255)
Path('grid.pgm').write_bytes(f'P5\n{out_w} {out_h}\n255\n'.encode()+pixels)
print(out_w, out_h, 'grid.pgm')
```

**Windows WSL**, with listed ZBar:

```bash
python3 grid_to_pgm.py modules.txt
zbarimg --raw grid.pgm
```

Expected output is decoded text, which may itself be another layer. If scanning fails, inspect the grid visually and check whether `1` should be light instead. Do not “repair” random modules until finder/timing patterns and dimensions are consistent.

For tile reassembly, use filenames, directory indexes, edge continuity, and QR structural constraints to reduce permutations. A nonogram may produce the QR grid: solve row/column run constraints, then render with the script above. Hexadecimal Sudoku may similarly map symbols to image modules.

Pigpen, flag semaphore, musical intervals, DTMF, keyboard shifts, and MaxiCode have different symbol systems. Identify the alphabet first. ZBar support is not universal across barcode types; a scanner failure may mean unsupported symbology rather than a damaged image.

## 6. Audio: inspect channels before interpreting tones

**Kali only**, with listed FFmpeg:

```bash
ffprobe -v error -show_entries stream=codec_name,sample_rate,channels,bits_per_sample -of default=noprint_wrappers=1 audio.wav
ffmpeg -i audio.wav -lavfi showspectrumpic=s=1600x900:legend=1 spectrum.png
```

Open the spectrogram and look for text, repeated bursts, paired tones, or frequency shifts. Try Audacity's Spectrogram view if you need to zoom and compare channels. Preserve the original sample rate; resampling can destroy symbol timing.

On Windows WSL, a standard-library WAV inspection works without assuming FFmpeg:

```python
# Save as wav_info.py; run: python3 wav_info.py audio.wav
import wave
import sys

with wave.open(sys.argv[1], 'rb') as wav:
    print('channels:', wav.getnchannels())
    print('sample width:', wav.getsampwidth())
    print('sample rate:', wav.getframerate())
    print('frames:', wav.getnframes())
    print('seconds:', wav.getnframes()/wav.getframerate())
```

The `wave` module handles supported uncompressed WAV variants, not every audio codec. An unsupported-format error means use an available approved decoder, not rename an MP3 to `.wav`.

### Morse bursts from one PCM channel

Save as `morse_runs.py`. It prints high/low envelope run lengths; it does not guess a threshold or a Morse alphabet for you.

```python
import sys
import wave
import struct
import math

filename = sys.argv[1]
threshold = float(sys.argv[2])  # RMS amplitude, e.g. 1000 for 16-bit PCM
channel = int(sys.argv[3]) if len(sys.argv) > 3 else 0
with wave.open(filename, 'rb') as wav:
    assert wav.getsampwidth() == 2, 'requires 16-bit PCM'
    count, rate = wav.getnchannels(), wav.getframerate()
    assert 0 <= channel < count
    raw = wav.readframes(wav.getnframes())
samples = struct.unpack('<'+'h'*(len(raw)//2), raw)[channel::count]
window = max(1, rate//100)  # approximately 10 ms
states = []
for start in range(0, len(samples), window):
    chunk = samples[start:start+window]
    rms = math.sqrt(sum(x*x for x in chunk)/len(chunk))
    states.append(rms > threshold)
runs = []
for state in states:
    if runs and runs[-1][0] == state:
        runs[-1][1] += 1
    else:
        runs.append([state, 1])
for state, length in runs:
    print('tone' if state else 'gap', round(length*window/rate, 3))
```

```bash
python3 morse_runs.py audio.wav 1000 0
```

Expect short/long tone clusters and several gap clusters. For conventional Morse, dot and dash lengths are roughly 1:3; within-letter, letter, and word gaps are roughly 1:3:7. Choose the basic unit from the run histogram, not a single noisy burst. If both channels differ, run each separately. Continuous music requires band filtering before envelope thresholding.

### DTMF, SSTV, and hidden sample bits

DTMF uses one low and one high frequency per key. After decoding digits, repeated presses may represent multi-tap text rather than a telephone number. Compare tone duration and pauses.

SSTV sounds like a long modulated image transmission. The Kali sheet has an `sstv`/PySSTV entry, but package name and decoding CLI capability must be verified with local help; do not assume an encoder package provides the source repository's decoder command. MMSSTV and RX-SSTV are explicitly unapproved. If the provided CLI cannot decode, retain the mode/timing observations and report the limitation.

Sample LSB extraction needs the correct sample width, signedness, endian order, channel, and bit order. Read PCM values rather than the WAV header bytes. Test whether an extracted stream begins with a plausible header; a handful of printable bytes is weak evidence.

## 7. RF/IQ files: get units and layout right

An IQ file may contain interleaved signed 8-bit, signed 16-bit, or float32 I/Q pairs. Determine the format from the challenge description or generator. A wrong dtype can produce a plausible-looking but meaningless constellation.

Save as `iq_peek.py` for a **little-endian float32 IQ** hypothesis:

```python
from pathlib import Path
import struct
import math
import sys

raw = Path(sys.argv[1]).read_bytes()
assert len(raw) % 8 == 0, 'not whole float32 I/Q pairs'
pairs = list(struct.iter_unpack('<ff', raw[:8*10000]))
assert pairs and all(math.isfinite(i) and math.isfinite(q) for i, q in pairs)
power = sum(i*i+q*q for i, q in pairs)/len(pairs)
print('pairs total:', len(raw)//8)
print('first five:', pairs[:5])
print('sampled mean power:', power)
```

Next establish sample rate, occupied bandwidth, carrier offset, symbol rate, and modulation. With a provisioned non-AI numerical library, plot a short spectrum and constellation locally. For QAM, carrier rotation and timing recovery must precede symbol slicing. Try a known preamble to resolve quadrant ambiguity and bit order.

FFT bins are in cycles per sample until multiplied by the sample rate. A frequency peak in a squared signal is not always the symbol rate; modulation and filtering can produce harmonics. Validate the proposed rate by a stable eye/constellation and repeated frame synchronization.

Manchester coding, whitening, convolutional coding, checksums, and framing may follow demodulation. A valid packet CRC is a much stronger success check than a few recognizable letters.

## 8. Interactive protocols without losing synchronization

Read the prompt and response framing before automating. A service may use newline-delimited JSON, length prefixes, menus, or multiple phases. TCP reads do not correspond one-to-one with server messages.

Save as `read_prompt.py` and replace the host/port only with the assigned challenge endpoint:

```python
import socket
import sys

host, port = sys.argv[1], int(sys.argv[2])
with socket.create_connection((host, port), timeout=5) as sock:
    sock.settimeout(5)
    stream = sock.makefile('rb')
    line = stream.readline(65537)
    if len(line) > 65536:
        raise SystemExit('line exceeds local limit')
    print(repr(line))
```

This reads one line and sends nothing. If the prompt has no newline, use a bounded `recv` loop until the observed delimiter instead. Preserve state in one connection when the challenge requires it; reconnecting may reset the secret or invalidate prior observations.

For a timed multi-phase puzzle, implement and test each local solver first, then connect the phases through explicit parsers. Never use a remote response as Python source. Treat a timeout as an unknown state, not automatically a wrong answer.

## 9. Python jails: inspect the evaluator, then build the primitive

Read the supplied jail source. Record the Python version, `eval` versus `exec`, available globals/builtins, input normalization, blacklist/allowlist, AST checks, length limit, output handling, and whether state persists between inputs.

Use small diagnostic expressions, one at a time:

```python
1+1
"A"*3
().__class__
(1).__class__.__name__
```

Expected results tell you whether arithmetic, strings, attribute access, and normal Python objects exist. A syntax error, filter rejection, NameError, and runtime exception reveal different stages. Do not assume `eval` accepts statements such as `x=1`; it does not. A walrus expression has separate syntax and scope restrictions.

### A complete object-reference escape toy

Removing `__builtins__` does not make references to powerful Python objects safe. Save as `jail_reference_toy.py`:

```python
FLAG = 'CTF{function_globals_are_reachable}'

def helper():
    return 'ordinary helper'

def toy_jail(expression):
    return eval(expression, {'__builtins__': {}, 'helper': helper}, {})

assert toy_jail('1+1') == 2
result = toy_jail("helper.__globals__['FLAG']")
assert result == FLAG
print(result)
```

For a real challenge, inspect which function/object is exposed and which globals it retains. If an exposed function's globals contain real builtins and the supplied flag path is `/app/flag.txt`, a corresponding builtins `open` call can read that file. The exact dictionary/module shape and filter rules decide the syntax.

Subclass enumeration is another route, but hard-coded indexes are unreliable across versions and imported modules. Search by class name and verify its attributes in a local reproduction. Decorators, format-field traversal, `__getitem__`, and object lifecycle hooks can create implicit calls only if the jail permits the required syntax and objects.

Unicode identifier normalization occurs during Python parsing; string literals are not normalized in the same way. Encoding comments matter only when source bytes are decoded as a file, not necessarily when an already-decoded input string is passed to `eval`.

### Advanced jail constraints

| Restriction | Useful starting point | Failure to avoid |
|---|---|---|
| No quotes | Existing docstrings, names, or indexed strings | Assuming the same docstring offsets across Python versions |
| No direct calls | Allowed decorators, indexing, or formatting hooks | Mutating immutable built-in classes |
| One dot | An already available attribute-access primitive | Presenting a chain containing many dots as a solution |
| Prime length | Count actual transmitted characters; pad with a permitted comment | Confusing escaped source spelling with received bytes |
| Length checked before a second read | Trace the second input's validation path | Treating assignment statements as valid `eval` expressions |
| Audit hooks | Determine Python hook, native hook, and events actually monitored | Assuming private CPython memory offsets are portable |
| Mastermind/distance oracle | Define exact score and input bounds | Interpreting a different score metric as character equality |

Private-runtime memory corruption and hard-coded `_PyRuntime` offsets are not portable recipes. Keep those source examples as version-specific reverse-engineering leads, and validate in the supplied local binary before attempting anything against a service.

## 10. Bash and restricted-shell puzzles

Find the real shell and input path. A filter before `eval`, a restricted shell mode, a menu wrapper, and a seccomp sandbox impose different constraints. Test quoting and expansion locally with a harmless marker.

```bash
printf '%s\n' $'\103\124\106'
printf '%s\n' "$0"
```

Expected first output: `CTF`. ANSI-C octal quoting creates bytes after the raw-input filter has already seen a different spelling. It helps only if the shell supports that syntax and the necessary characters survive the filter.

For an assigned jail that permits the shell built-in `read` and redirection, a supplied flag path can be read without an external `cat`:

```bash
while IFS= read -r line; do printf '%s\n' "$line"; done < /app/flag.txt
```

This assumes that exact challenge file path and permissions. If redirection is filtered or execution happens in another shell, it fails. Closed stdout requires tracing the actual output channel; carriage returns can alter display but do not create file access by themselves.

`HISTFILE`, startup files, environment variables, editor command hooks, and dynamic-loader variables are meaningful only if the wrapper invokes the corresponding feature. Do not set persistent startup variables on the competition workstation to test a challenge theory.

## 11. Games, virtual machines, and finite-state puzzles

Locate the authoritative state. Browser-rendered scores, local cookies, a WebSocket server, WASM memory, and server databases are different sources of truth. Change a harmless client value and check whether the server accepts the resulting state.

For an unsigned or disclosed-secret Flask session, separate decoding from forging; a readable cookie is not necessarily modifiable. For WebSocket games, compare a normal frame with a controlled changed field. Server-time-only validation and floating-point edge cases require actual server acceptance, not just a changed display.

WASM memory is linear bytes, but compiler layouts and exported functions determine meaningful offsets. Use supplied source and browser DevTools to correlate one known value before patching. Roblox files, PyInstaller bundles, remapped Python opcodes, and memfd-packed binaries belong primarily to reverse engineering; preserve their container/bytecode version and use the approved local tools from that chapter.

### A shortest-path toy you can adapt

Save as `maze_bfs.py`:

```python
from collections import deque

grid = ['S..#', '.#..', '...E']
start, goal = (0, 0), (2, 3)
queue = deque([start])
previous = {start: None}
while queue:
    r, c = queue.popleft()
    if (r, c) == goal:
        break
    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nr, nc = r+dr, c+dc
        if not (0 <= nr < len(grid) and 0 <= nc < len(grid[0])):
            continue
        if grid[nr][nc] == '#' or (nr, nc) in previous:
            continue
        previous[(nr, nc)] = (r, c)
        queue.append((nr, nc))
assert goal in previous
path = []
current = goal
while current is not None:
    path.append(current)
    current = previous[current]
path.reverse()
assert len(path)-1 == 5
assert all(abs(a[0]-b[0])+abs(a[1]-b[1]) == 1 for a, b in zip(path, path[1:]))
print(path)
```

For image mazes, first derive a stable grid from cell centers. Anti-aliased edges, moving sprites, and coordinate scaling can corrupt wall detection. If a move depends on inventory or switches, include them in the BFS state; position alone is insufficient.

### Recurrences and number representation

For a recurrence puzzle, compute a dozen terms locally, compare all supplied examples, then use dynamic programming or matrix exponentiation. Do not upload the challenge sequence to an online lookup service. OEIS-style automated online searching from the original source is excluded here.

JavaScript integers lose exactness above `2^53-1`. **Kali only**, with listed Node.js:

```javascript
// Save as precision-demo.js; run: node precision-demo.js
const x = 2 ** 53;
console.log(x === x + 1); // true
console.log(BigInt(x) === BigInt(x) + 1n); // false
```

A challenge must actually use floating-point number semantics for this to matter. JSON-to-integer conversion in another language may reject or preserve the value differently.

De Bruijn sequences cover all fixed-length substrings efficiently, but cyclic versus linear output changes the required suffix. The 100-prisoners strategy follows permutation cycles; it does not guarantee success for an arbitrary instance. Fifteen-puzzle solvability depends on inversion parity and blank-row convention, so verify with a solved board before decoding bits.

## 12. Constraint solving and esoteric languages

Write constraints in the original domain. For bytes, constrain `0..255`; for fixed-width arithmetic, preserve wrapping and signedness. Add a second-solution check to learn whether the model is unique.

Without an SMT dependency, small domains can be enumerated exactly. Save as `constraints_toy.py`:

```python
solutions = [(x, y) for x in range(10) for y in range(10)
             if x+y == 11 and 3*x-y == 9]
assert solutions == [(5, 6)]
print(solutions[0])
```

For a provisioned `z3` library, model the same constraints first and verify its solution with ordinary Python. A SAT result is not a flag until it passes the challenge checker. YARA-derived conditions, Boolean circuits, nonograms, and type constraints may each need different domain choices.

Brainfuck requires a tape size policy, cell width, EOF behavior, and matched bracket map. Instrument each opcode and bound the step count before running unknown code. Whitespace languages treat spaces, tabs, and newlines as syntax; do not strip them. Piet requires image color transitions and direction state; an image viewer alone does not execute it.

Verilog/HDL puzzles require combinational versus sequential semantics, bit widths, signedness, and clock/reset behavior. If an unlisted simulator is required, manually translate a small circuit into a local Boolean model or use the provided approved environment; do not use an online HDL compiler.

## 13. DNS and protocol puzzles

Use the organizer-provided resolver or packet capture, not public infrastructure. DNS round-robin responses may reveal a set over repeated queries, but caching, TTL, and load balancing affect observations. A DNS maze needs a visited set and an explicit next-label rule.

For DNSSEC NSEC walking, inspect predecessor/successor names and whether the zone uses NSEC or NSEC3. An IXFR request differs from AXFR and requires the proper serial framing. EDNS Client Subnet affects resolver behavior only when the server honors it; it is not a universal source-address spoof.

When DNS carries encoded data, use transaction IDs, sequence fields, timestamps, and domain labels to reconstruct order. Remove the fixed suffix before decoding. Do not send challenge secrets through public DNS as a recovery method.

DNS rebinding is a timing and resolution disagreement; capture both validation and fetch phases. A hostname resolving twice to the same address is a failed experiment, not proof that the application is safe.

## 14. Challenge-scoped privilege puzzles

These source topics apply only when the challenge explicitly gives you a shell or local service and makes privilege escalation part of the objective. Run checks inside that challenge, never on the competition workstation:

```bash
id
pwd
sudo -l
```

Read the exact allowed program and argument constraints. Wildcards can match path separators depending on the matching function; a symlink can change what a later privileged open sees. Confirm ownership and permissions of the specific file involved. Do not modify `/etc/sudoers` or host service configuration merely to prove a theory.

SUID file readers, backup jobs, writable script paths, database program execution, print deployment services, and monitoring-agent arguments are separate primitives. Start with the supplied service's normal behavior and a harmless marker. The end goal is the designated challenge file, not persistence or workstation control.

Docker socket, privileged containers, BuildKit secrets, Kubernetes tokens, NFS, and internal proxies require explicit inclusion in the challenge topology. A token found in a challenge does not authorize unrelated infrastructure. For a permitted local puzzle, determine the token's actual namespace/role or socket permissions before choosing an action.

Historical polkit overflows, seccomp high-bit descriptor mistakes, editor escapes, and WinSSHTerm credential formats are version-specific. Use the supplied binary/configuration and approved reverse-engineering tools to verify the failing check. Source writeup commands are not portable proof.

## 15. Portal workflow and a useful handoff

Use the organizer's normal browser interface to read descriptions, download attachments, start instances, request hints, and submit flags. A CTFd-looking theme does not prove its API or authentication behavior. Hints can cost points; read the displayed consequence before purchasing.

If the organizer explicitly documents an API for competitors, use its token and endpoint format as supplied. Keep the token out of notes and logs. Do not scrape hidden challenges, attack the scoring platform, or automate repeated submissions because an old repository script can do so.

Record each solve as input artifact/hash, interpretation, exact transformation or script, expected output, final flag, and remaining assumptions. If a QR, audio, game, or jail solution depends on manual transcription, save that intermediate representation so a teammate can reproduce it.

The 14 source files in `ctf-misc/` are merged here: overview; encodings and advanced formats; audio and RF; Python/Bash jails; games/VMs parts 1–4; DNS; CTFd navigation; and Linux privilege puzzles. Overlapping network, media, crypto, and reverse-engineering details are cross-category material rather than new official event categories.


---

<a id="12-excluded-and-advanced"></a>

# Excluded workflows and advanced material

The repository contains agent instructions and techniques that are unsuitable for this event handbook. The approved workbook and [official event rules](https://ajccbc.ncsa.or.th/cyber-sea-game-2026/) control tool use. A source file remaining in the repository is not approval to run it.

## AI/ML and agent workflows are excluded

All four files in `ctf-ai-ml/` are excluded from runnable event instructions:

| Source | Material reviewed | Reason and useful manual alternative |
|---|---|---|
| `SKILL.md` | Model inspection, weight comparison, adversarial tests, remote LLM calls | AI/ML tools and libraries are not permitted. Identify ordinary file/container metadata with approved local tools; route conventional data/crypto logic to the relevant chapter |
| `adversarial-ml.md` | FGSM, PGD, C&W, adversarial patches, poisoning, backdoor analysis, historical Keras/foolbox examples | These depend on prohibited ML frameworks/workflows. Do not install or run them; inspect an ordinary supplied parser or validation function manually if that is the actual challenge surface |
| `model-attacks.md` | Weight negation, inversion, encoder collisions, LoRA merging, model extraction, membership inference | Model training/inference and related tools are excluded. For a non-AI artifact embedded in an archive, inspect the archive structure and recover that artifact without loading a model |
| `llm-attacks.md` | Prompt injection, jailbreaks, token smuggling, context manipulation, agent tool misuse | AI interaction workflows are excluded. Treat embedded text as data; analyze any conventional HTTP/authentication/serialization issue manually |

The web sources also contain chatbot and AI tool-call sections. Those sections are excluded even though the rest of their source files is adapted. There are no runnable prompts, framework installers, model downloads, or AI service calls in this handbook.

## Tavily, MCP, and automated online assistance are excluded

`ctf-similar-search/SKILL.md`, `search.py`, and `search.sh` implement Tavily-based search/extraction. The Python client requests an answer from the service and transmits search queries/URLs. These are not the manual local research workflow used here.

`ctf-web/tools-mcp.md` describes Playwright/Burp MCP integrations, agent approval settings, scanners, and callback services. Use the approved browser DevTools and Burp Community interface manually as shown in [Web exploitation](#02-web-exploitation). Burp Community does not imply approval of every extension or Professional-only feature.

For **Kali**, use supplied offline references without exposing challenge material:

```bash
rg -n -i 'padding oracle|nonce reuse' /opt/tools/hacktricks
rg -n -i 'sudo|wildcard' /opt/tools/GTFOBins.github.io
```

Search for the general technique locally, read the matching explanation, and compare prerequisites to the supplied challenge. If the path is absent, use the handbook and supplied source; do not assume an unlisted reference checkout can be installed.

## Tools and services that are not substitutes

| Source suggestion | Event-compliant replacement |
|---|---|
| Public webhook, callback tunnel, cloud function, external JWKS host | Organizer-provided callback service or a same-challenge observable response; otherwise keep a blind hypothesis unconfirmed |
| Online hash cracking, public FactorDB lookup, online mathematical solver | Local Python arithmetic, listed local factoring/cracking tools, or an honest environment limitation |
| Online compiler/decompiler | Approved local compiler/decompiler, supplied build artifact, or manual static analysis |
| Dirsearch | A few evidence-backed paths in Repeater; targeted low-rate ffuf on Kali when appropriate |
| JWT Editor, GraphQL Raider, Hackvertor, Copy As Python-Requests | Raw HTTP editing and local standard-library decoding; these extensions are explicitly unapproved |
| YAFU | Local mathematical checks or an appropriate approved crypto-attacks implementation on Kali |
| MMSSTV/RX-SSTV | Inspect the available approved audio workflow; verify what the listed SSTV package actually supports |
| Large asynchronous fuzzing script | Manual baseline/control experiment and a small bounded candidate set |
| Online sequence lookup/OEIS automation | Derive a recurrence from supplied terms and validate it locally |

The workbook's permission to add non-AI Python libraries appears in the Windows sheet. It is not a loophole for explicitly unapproved tools, and it is not a claim that every library is already installed or that the same installation policy was stated for Kali.

## Advanced does not mean excluded

Useful advanced topics remain in the handbook with their prerequisites:

- [Web exploitation](#02-web-exploitation): parser disagreement, browser origins, cache/race/protocol behavior, serialization, source-based framework analysis, and static Web3 review.
- [Cryptography](#07-cryptography): exact integer arithmetic, practical RSA and oracle demonstrations, nonces, modes, and PRNG modelling.
- [Advanced cryptography](#14-advanced-crypto): lattices, ECC, small roots, unusual algebra, proof systems, post-quantum recognition, and reduced-round constructions.
- [Miscellaneous](#11-miscellaneous): constrained interpreters, finite-state games, encoding reconstruction, RF/audio prerequisites, and explicitly challenge-scoped privilege puzzles.

Version-specific exploits need the supplied version and configuration. The handbook does not present every historical payload as current. In particular, Python `eval` cannot accept assignment statements; private runtime memory offsets are not portable; prototype pollution needs a merge and a gadget; FROST is not inherently a lattice scheme; and a listed package name does not guarantee a particular decoder executable.

The original high-concurrency fuzzer has further correctness limits: regex markers are not stripped consistently, processing-chain arguments do not uniformly match the callable signatures, redirects can hide the first response, and TLS verification is disabled in paths where it should remain enabled. It is retained as source provenance, not endorsed as a runnable event tool.

## What to do when a challenge seems to require an excluded tool

Continue the parts that use approved local tools: inspect bytes, source, equations, normal requests, and supplied metadata. Identify the specific missing capability. Ask the organizer for clarification through the event's normal support channel before using a prohibited or unlisted tool. Do not upload the challenge, install an AI framework, or invoke an online service to bypass the restriction.

File-by-file dispositions are recorded in `human-guide/review/web-coverage.json`. An “adapted” or “merged” file may contain excluded subsections; its notes identify those exceptions. “Reference-only” means historical/provenance material whose original commands are not part of the runnable handbook.


---

<a id="13-pwn-practice-atlas"></a>

# Pwn practice atlas: 43 cases, each with a specific lesson

Use this atlas after the binary-exploitation chapter. It preserves the individual exercises from `ctf-pwn/pwnable-tw/` without presenting historical offsets as universal exploits. The cases are preparation material, not an instruction to connect to public practice servers during the competition. Use locally supplied practice artifacts or an explicitly assigned challenge service.

The case descriptions below come from the repository's individual writeups. Their original binaries, exact runtimes, and exploit success claims were not reproduced for this handbook. Several directory-index summaries disagree with their detailed writeups; the disputed claims are identified below. Treat the individual mechanisms as hypotheses to verify against your copy of the binary.

## How to work through a case

For every case, record the binary and libc hashes, architecture, input protocol, protections, and the exact state transition that creates the primitive. Stop after each checkpoint. A working local leak is more useful than an unexplained full exploit copied from an old environment.

**Kali, approved tools, with the exercise binary named `chall`:**

```bash
file chall
checksec --file=chall
rabin2 -I chall
rabin2 -i chall
r2 chall
```

In radare2, use `aaa`, `afl`, `pdf @ main`, and `axt @ IMPORT`, replacing `IMPORT` with the exact flag shown by `ii`. Follow the vulnerable caller, identify the input operation and the state it changes, then inspect the next consumer of that state. The GDB commands in the pwn chapter are the **Windows WSL** debugging route; Kali debugging requires the supplied GDB environment to work. **Windows native** x64dbg is for Windows PE targets, not these Linux ELF cases.

For stdlib packing use Windows WSL Python, or Kali Python after checking its availability. Pwntools is not individually listed as preinstalled. The Windows non-AI-library permission does not establish its availability in either environment. Keep original template scripts as study references; the pwn chapter describes their defects and standard-library alternatives.

## First control-flow and parsing exercises

### 1. `start`: obtain the stack address before using it

**Prerequisites:** i386 syscall conventions, little-endian packing, executable-stack behavior, two-stage input framing.

The detailed writeup describes a 60-byte read into a 20-byte message region, followed by a return. An existing write sequence can disclose the stack value before another input stage. Identify the read count and the exact saved return slot in the disassembly; then reuse the output path and parse its raw bytes before considering a stack target.

**Checkpoint:** the recovered pointer falls inside the current stack mapping and the next read lands where you predict. A successful first write does not mean the second payload has enough space. Source: `ctf-pwn/pwnable-tw/start.md`.

### 2. `orw`: the permitted end goal is smaller than a shell

**Prerequisites:** i386 Linux syscalls, shellcode placement, seccomp policy interpretation.

Input is executed in a writable/executable region, but a syscall filter limits what it can do. Decode the actual policy and implement the permitted file-read sequence: open the exact challenge path, preserve the returned descriptor, read into a valid buffer, and write the returned count. The historical alternative involving a missing architecture check requires a very specific kernel and filter; do not confuse x32 ABI calls with a 32-to-64-bit mode switch.

**Checkpoint:** every syscall and argument is permitted, and errors are distinguished from successful reads. Source: `ctf-pwn/pwnable-tw/orw.md`.

### 3. `calc`: an arithmetic parser can become a stack-index primitive

**Prerequisites:** expression parsing, stack layout, signed arithmetic, ROP in a static i386 binary.

The source describes a mismatch between pushing an operand and evaluating an operator when a token converts to zero. That mismatch changes the operand-pool index. Trace a minimal expression in the debugger and record the pool counter before and after each operation; derive which expression reads or adjusts one chosen stack word before assembling a longer chain.

**Checkpoint:** one selected word changes by the predicted delta while surrounding state remains usable. Preserve any canary and account for arithmetic width. Source: `ctf-pwn/pwnable-tw/calc.md`.

### 4. `silver_bullet`: the terminator changes the next operation's length

**Prerequisites:** struct layout, `strncat` semantics, staged ret2libc on i386.

When the description reaches its nominal capacity, the appended NUL reaches the adjacent power field. The next append trusts that altered field and can write farther. Measure the field boundary and demonstrate the reset with a complete-length input before using the enlarged append to reach saved control data.

**Checkpoint:** the first operation changes length state, and the second demonstrably uses that new state. Leak and reentry stages must each preserve the game's expected flow. Source: `ctf-pwn/pwnable-tw/silver_bullet.md`.

### 5. `dubblesort`: the program rearranges the payload

**Prerequisites:** i386 stack layout, unterminated-string disclosures, failed numeric conversions, sorting constraints.

An unterminated name can disclose neighboring stack data; an excessive element count reaches past the number array. A failed `scanf` conversion may leave an existing canary word unchanged, but the subsequent sort still permutes the entire array. Reconstruct the actual comparison type and positions before choosing numeric values.

**Checkpoint:** model the sorted array locally and confirm the canary and final control words end up at the intended slots. A “skip input” trick is insufficient if sorting later moves the preserved word. Source: `ctf-pwn/pwnable-tw/dubblesort.md`.

### 6. `3x17`: a small write becomes a staged sequence

**Prerequisites:** ELF destructors, static x86-64 layout, `leave; ret` stack pivots.

The source describes a fixed-size arbitrary write and writable destructor-related state. Reentering the input routine through the finalization path can provide repeated writes, after which a prepared fake frame pivots to a chain. Confirm the actual finalizer order and guard counter: “infinite writes” in the source is shorthand and may be bounded by program state.

**Checkpoint:** two consecutive writes succeed through the planned reentry, and the fake frame has both a replacement BP word and a return word. Source: `ctf-pwn/pwnable-tw/3x17.md`.

### 7. `starbound`: a menu choice becomes an indirect call

**Prerequisites:** indexed addressing, function-pointer dispatch, stack pivots and disclosure calls.

The main menu uses the parsed choice as an unchecked index into a function table. A negative index can reach the player-name buffer. Derive `(controlled_buffer - table_base) / pointer_size` from the actual image rather than copying the historical index, and confirm the resulting indirect call target.

**Checkpoint:** the dispatcher reads the intended pointer from your name data. Then prove the chosen gadget's stack and register effects before using it for a leak or pivot. Source: `ctf-pwn/pwnable-tw/starbound.md`.

### 8. `babystack`: an authentication oracle and stale stack bytes compose

**Prerequisites:** prefix comparisons, NUL termination, repeated stateful requests, stack-copy behavior.

The comparison length comes from the supplied string, so empty input or a correct prefix can change authentication behavior. A later copy uses a stack buffer previously filled by another operation; bytes outside the shorter read can survive and extend a `strcpy`. Separate oracle recovery from the overflow and preserve the original password/check value where the exit path validates it.

**Checkpoint:** a known correct and known wrong prefix produce distinct results under the same process state. Then demonstrate the stale tail used by the copy. Source: `ctf-pwn/pwnable-tw/babystack.md`.

## Constrained code and missing-output exercises

### 9. `death_note`: a negative index reaches a relocation slot

**Prerequisites:** i386 GOT layout, signed bounds checks, printable shellcode encoding.

The note index is checked only against an upper bound. Derive which negative slot reaches a writable function pointer and inspect whether the allocated note memory is executable at runtime. The input filter constrains bytes, so ordinary machine code must be encoded or constructed in stages.

**Checkpoint:** the target slot changes to the allocated buffer and the next call actually dereferences it. Check every input byte against the filter before attempting execution. Source: `ctf-pwn/pwnable-tw/death_note.md`.

### 10. `alive_note`: tiny fragments need a reliable bridge

**Prerequisites:** the negative-index primitive, alphanumeric encoding, heap placement, short jumps.

This variant combines a small per-note limit with a restricted character set. The source chains tiny code fragments across allocations, but allocator padding and terminators are part of the instruction stream. First draw fragment addresses, usable bytes, and gaps; then derive each jump and verify the initial register state used by the decoder.

**Checkpoint:** a local disassembly follows the intended fragment sequence without executing chunk headers or NUL terminators. Source: `ctf-pwn/pwnable-tw/alive_note.md`.

### 11. `mno2`: bytes must satisfy two grammars

**Prerequisites:** x86 instruction encoding, alphanumeric self-modification, parser tokenization.

The executed input must also parse as a chemical formula. A sequence that is valid x86 and alphanumeric can still fail the element-symbol grammar. Reproduce the validator and test each encoded fragment through both the parser and disassembler; preserve the known entry registers that make arithmetic/XOR construction possible.

**Checkpoint:** the full first stage passes the original validator and reconstructs the intended unrestricted bytes in writable memory. Element-looking bytes are not harmless padding if they change a needed register. Source: `ctf-pwn/pwnable-tw/mno2.md`.

### 12. `kidding`: account for descriptors closed before control transfer

**Prerequisites:** static i386 ROP, descriptor lifetime, tight payload budgets.

The binary reads once, then closes standard input/output/error before returning. The obvious second read or stdout write is therefore unavailable. Trace the descriptor closures and count the first payload's usable bytes; any restored communication must stay within an explicitly authorized local practice topology.

**Checkpoint:** the complete first-stage path works with descriptors 0, 1 and 2 already closed. The historical helper/flag path is specific to that challenge image. No public callback endpoint or listener is provided by this handbook. Source: `ctf-pwn/pwnable-tw/kidding.md`.

### 13. `unexploitable`: manufacture a missing primitive from existing code

**Prerequisites:** x86-64 ROP, ret2csu, partial pointer writes, syscall return values.

The overflow is simple, but the binary lacks an ordinary output routine and convenient syscall gadget. The detailed source describes a writable relocation at a page boundary and a low-byte redirection into a nearby syscall instruction in the matching libc. Verify actual runtime page permissions rather than assuming the RELRO summary identifies every boundary correctly.

**Checkpoint:** the redirected call reaches the intended instruction and its registers have the expected values. A read returning 15 is usable for SROP only if the trigger and frame are also correct. Source: `ctf-pwn/pwnable-tw/unexploitable.md`.

### 14. `de_aslr`: use a pointer already present without printing it

**Prerequisites:** constrained x86-64 ROP, stack pivots, arithmetic gadgets, dynamic linker internals.

The detailed writeup describes an unbounded `gets`, no normal output function, and Full RELRO. Study how a known libc pointer can be loaded or transformed through existing register/memory operations without first leaking it. The directory index's generic writable-GOT/dynamic-resolver story is not sufficient evidence for this target.

**Checkpoint:** track one existing pointer through every gadget and prove the resulting indirect target. Test newline restrictions and carry/overflow side effects. Source: `ctf-pwn/pwnable-tw/de_aslr.md`.

### 15. `printable`: a format string can still act when output is closed

**Prerequisites:** `%n` count writes, stdio buffering, finalization, partial overwrite probabilities.

The format sink executes after stdout is closed, and the program then calls `exit`. A useful path must create repetition or redirect a usable output stream before ordinary leaks become available. Measure how much formatting occurs before a failed flush aborts the operation; do not assume arbitrary large counts are possible.

**Checkpoint:** distinguish a successful loop, a restored output channel, and final control flow as three separate milestones. Historical argument positions and retry probabilities depend on the original runtime. Source: `ctf-pwn/pwnable-tw/printable.md`.

## Heap ownership and allocator exercises

### 16. `hacknote`: metadata can be reclaimed as content

**Prerequisites:** UAF, allocation size classes, i386 function pointers.

Deleting a note frees its metadata and content but leaves the table pointer. A later allocation can occupy that metadata region and replace the print callback/data interpretation. Track the metadata allocation separately from its content allocation; otherwise a superficially similar size may reclaim the wrong object.

**Checkpoint:** a new buffer overlaps the stale note object, and the print action reads the expected callback and argument. Start with a controlled disclosure before a final call. Source: `ctf-pwn/pwnable-tw/hacknote.md`.

### 17. `secret_garden`: free state and table membership disagree

**Prerequisites:** glibc fastbins/unsorted bins, stale references, partial writes.

Removing a flower releases its name but leaves enough object state to revisit the allocation. The source combines disclosure of freed metadata with repeated frees/reallocation. Distinguish a slot's active flag from whether its pointer has been cleared; cleanup operations can change the heap history.

**Checkpoint:** after removal, identify exactly which later action still accesses the freed name and what bytes an allocation preserves. Source: `ctf-pwn/pwnable-tw/secret_garden.md`.

### 18. `secret_of_my_heart`: one NUL changes consolidation

**Prerequisites:** off-by-one terminators, chunk headers, backward consolidation, heap disclosures.

A full content read is followed by a terminator one byte beyond the requested buffer. A separate unterminated name can expose the adjacent pointer. Recover the heap layout, then verify which size flag the zero byte changes and which neighboring fields must remain consistent for the allocator.

**Checkpoint:** freeing the affected neighbor produces the intended overlap without an integrity abort. A time-derived metadata address or hidden menu route is an alternative to investigate, not a required assumption. Source: `ctf-pwn/pwnable-tw/secret_of_my_heart.md`.

### 19. `tcache_tear`: repeated free plus a fixed scratch region

**Prerequisites:** the supplied early-tcache libc, free-list state, fake-chunk prerequisites, unsorted disclosures.

The detailed source's reliable core is a global pointer left live after free, plus a known BSS region useful for shaping metadata. Prove the actual tcache behavior of the supplied build and the allocation sequence leading to the target region. Do not transplant this chain to modern safe-linking allocators.

**Checkpoint:** repeated allocation returns the intended overlap, and a forged larger chunk satisfies the target allocator's checks. The source's additional claim that a small `malloc(size)` plus `read(..., size)` is itself an overflow is not established by that code and is not used here. Source: `ctf-pwn/pwnable-tw/tcache_tear.md`.

### 20. `heap_paradise`: build a leak before relying on absolute addresses

**Prerequisites:** fastbin duplication, unsorted-bin residue, partial stdout corruption.

The menu has allocation/free operations and stale pointers but no convenient normal disclosure. The source uses allocator metadata and a partial overwrite to reach a stdout-related disclosure. Draw the relative chunk layout before making an absolute-address hypothesis.

**Checkpoint:** a recognizable libc pointer is emitted and confirmed against the supplied library. Record the unknown low bits and measured retry rate instead of calling the initial partial overwrite deterministic. Source: `ctf-pwn/pwnable-tw/heap_paradise.md`.

### 21. `bookwriter`: no delete operation does not mean no freed chunk

**Prerequisites:** unterminated strings, top-chunk behavior, historical House of Orange/FILE exploitation.

The editor updates capacity from `strlen`, which can exceed the original allocation when no NUL is present. The source combines this with top-chunk manipulation to enter allocator paths that free old top memory without a menu delete. Also inspect the off-by-one page slot and author-string disclosure.

**Checkpoint:** the edited length really increases, the next write reaches the intended metadata, and the old top follows the predicted allocator path. The final FILE technique requires the old challenge libc. Source: `ctf-pwn/pwnable-tw/bookwriter.md`.

### 22. `applestore`: a list keeps a pointer to an expired stack object

**Prerequisites:** stack lifetimes, linked-list layout, constrained reciprocal writes.

A specific cart total creates a promotional node as a local variable and links it into a longer-lived list. After checkout returns, later input can overlap its fields. Solve the cart-total arithmetic from the supplied prices, then show the same stack bytes being reused as the node's name/link fields.

**Checkpoint:** listing the cart dereferences your chosen name pointer. Before using unlink, calculate both writes and ensure the secondary write does not crash or destroy a needed field. Source: `ctf-pwn/pwnable-tw/applestore.md`.

### 23. `spirited_away`: decimal formatting changes a length field at a threshold

**Prerequisites:** precise stack layout, decimal string lengths, fake-chunk allocation.

The feedback counter is formatted into a buffer near a length field. As the digit count grows, the formatted suffix corrupts that field and enables a larger later read. An unterminated reason supplies useful disclosures; the historical chain then places a fake chunk on the stack.

**Checkpoint:** observe the exact counter threshold and changed length byte. Verify the fake chunk and next allocation before targeting a saved return slot. Source: `ctf-pwn/pwnable-tw/spirited_away.md`.

### 24. `re_alloc`: audit the zero-size return path carefully

**Prerequisites:** glibc `realloc` semantics, two-slot ownership, tcache poisoning, GOT redirection.

The intended lesson is a stale-pointer/lifetime error around zero-size reallocation and a later conversion-function redirection. However, this source contradicts itself: its overview says the old pointer remains, while one subsection says the NULL return is stored. Ordinary `realloc(NULL, n)` followed by a write is not by itself a UAF.

**Checkpoint:** establish from the binary whether the zero-size path leaves a dangling pointer, duplicate alias, or another invalid lifetime. Only then consider the proposed tcache/GOT/format-string chain. Source: `ctf-pwn/pwnable-tw/re_alloc.md`.

### 25. `re_alloc_revenge`: an error branch preserves an invalid owner

**Prerequisites:** realloc failure/zero-size behavior, two-slot heap choreography, disclosure alternatives.

The detailed source describes `realloc(ptr, 0)` freeing storage and returning NULL, followed by an error path that does not clear the stored pointer. Model both slots after every operation and inspect how allocator duplicate-free checks are handled in the exact provided runtime.

**Checkpoint:** show an actual subsequent access through the dangling slot and prove a controlled overlap. The harder version's protection changes require a new target choice; do not carry over writable-GOT assumptions. Source: `ctf-pwn/pwnable-tw/re_alloc_revenge.md`.

### 26. `caov`: C++ temporaries and stale stack fields both affect ownership

**Prerequisites:** copy assignment, destructors, stack-frame reuse, arbitrary-free consequences.

Returning a data object by value can create a temporary whose destructor releases shared storage. A separate routine leaves stack bytes where a later object expects its pointer field, allowing destruction to act on stale data. Draw the copy/destruction sequence rather than treating every menu operation as one allocation.

**Checkpoint:** identify which destructor frees which address, and whether the same pointer still has a live owner. Source: `ctf-pwn/pwnable-tw/caov.md`.

### 27. `ghost_party`: shallow copies violate unique ownership

**Prerequisites:** C++ copy constructors, raw owning pointers, virtual dispatch.

The Vampire class's default copy preserves a pointer that its destructor frees, while another object's temporary string can leave a dangling `c_str` pointer. Compare the vulnerable classes with those that implement correct copying; that contrast helps identify the actual lifetime error.

**Checkpoint:** after the source object or temporary is destroyed, demonstrate the remaining reference and the allocation that reuses its storage. Source: `ctf-pwn/pwnable-tw/ghost_party.md`.

### 28. `break_out`: a freed note remains reachable through a linked object

**Prerequisites:** UAF, overlapping objects, linked-list traversal, read/write through pointer fields.

Punishment frees a prisoner's note without clearing its pointer and size. Reallocation can turn that stale access into an overlapping object; modifying a next pointer can make listing traverse a forged prisoner. Preserve enough list structure to keep the menu usable during each stage.

**Checkpoint:** a list operation reads a controlled note pointer and an edit writes the predicted region. Validate both before selecting a libc-specific endpoint. Source: `ctf-pwn/pwnable-tw/break_out.md`.

### 29. `food_store`: an uninitialized link inherits old allocation contents

**Prerequisites:** heap reuse, uninitialized fields, linked structures, old-libc FILE constraints.

The individual writeup identifies a recipe `next` pointer never initialized after allocation. A reclaimed chunk can therefore supply a controlled or allocator-derived link. This is more specific than the directory index's generic heap-overflow summary and should guide the first experiment.

**Checkpoint:** record the chunk's previous contents, allocate the recipe, and show which bytes become its next pointer without being written. Follow the resulting list before considering advanced FILE or allocator chains. Source: `ctf-pwn/pwnable-tw/food_store.md`.

### 30. `babyallocator`: stack-segment metadata is an allocation target

**Prerequisites:** GCC split stacks, `alloca`, recursive frames, libc stack usage.

The source describes split-stack segment metadata being corrupted by a non-split-stack libc call at a carefully chosen depth and allocation size. This is not an ordinary one-buffer overflow: the runtime's segment header and dynamic allocation list must be reconstructed.

**Checkpoint:** identify the segment boundary and the exact libc write that reaches a metadata field, then prove the resulting returned allocation or frame overlap. Depth/size constants depend on the complete runtime. Source: `ctf-pwn/pwnable-tw/babyallocator.md`.

## FILE, stateful library and complex application exercises

### 31. `seethefile`: a pointer overflow reaches `fclose`

**Prerequisites:** BSS layout, file disclosures, glibc 2.23 FILE structures.

An unbounded exit-name input reaches the neighboring `FILE *`, and the program subsequently closes it. The file-viewing feature can disclose memory mappings in the original lab. Separate that address disclosure from the fake-object construction; identify every field consumed before virtual dispatch.

**Checkpoint:** the overwritten pointer reaches your object at `fclose`, with valid supporting state. The old fake-vtable route is not applicable unchanged to modern glibc. Source: `ctf-pwn/pwnable-tw/seethefile.md`.

### 32. `wannaheap`: validation updates one size but not another

**Prerequisites:** mmap-relative layouts, single-byte writes, stdin FILE behavior, treap-dependent residue.

The first requested size is remembered even after a replacement size is validated and used for allocation. The terminator is then written using the original value. The source turns this into a null-byte change to stdin buffering, while a separate uninitialized string can disclose a libc pointer.

**Checkpoint:** trace both size variables and observe the terminator address. Verify any mmap-to-libc distance for the supplied runtime and distinguish a probabilistic tree-layout leak from a guaranteed one. Source: `ctf-pwn/pwnable-tw/wannaheap.md`.

### 33. `criticalheap`: data types and library side effects matter

**Prerequisites:** format-string reads, stale slot state, environment variables, libc allocation behavior.

The detailed source describes several independent observations: a user-controlled format sink, unterminated output, reused slot contents, timezone file loading through `localtime`, and a `realpath` output buffer issue. Treat them as alternative routes with separate prerequisites rather than assuming one combined exploit.

**Checkpoint:** distinguish the challenge's stated objective from any decoy file, and identify which local operation yields the required information or write. File paths and helper behavior are specific to the original image. Source: `ctf-pwn/pwnable-tw/criticalheap.md`.

### 34. `criticalheap_pp`: the expanded path exceeds the input allocation

**Prerequisites:** `realpath` output semantics, heap grooming, environment-triggered allocations.

The detailed route uses the same small buffer for a relative input path and its longer resolved output, reaching adjacent allocation metadata. Environment and timezone operations provide additional allocation/free behavior. The directory index's broad C++ type-confusion explanation is not a substitute for measuring this path.

**Checkpoint:** demonstrate the exact resolved path length and write boundary, then record the neighboring chunk affected. Verify the real challenge objective independently of any decoy. Source: `ctf-pwn/pwnable-tw/criticalheap_pp.md`.

### 35. `bounty_program_a`: a NULL argument has stateful library meaning

**Prerequisites:** `strtok` continuation state, allocation failure, object pointer overwrites, digest oracles.

Failed allocation returns NULL, but passing NULL to `strtok` continues a previous tokenization rather than starting an empty one. The detailed source also describes a password overflow into a contact pointer and a contact-hash oracle. Prove each capability independently; a digest reveals a byte only when the remaining hashed bytes and candidate space are controlled.

**Checkpoint:** inspect the tokenizer's retained pointer and show the next read or delimiter NUL-write reaches the intended stale buffer. Source: `ctf-pwn/pwnable-tw/bounty_program_a.md`.

### 36. `bounty_program_b`: a delimiter write can alter a pointer

**Prerequisites:** the alpha variant's tokenizer state, heap overlap, protection-aware object reuse.

The hardened variant retains stateful tokenization on freed data. Because `strtok` replaces a matching delimiter with NUL, it can modify a byte inside a pointer if that byte equals the delimiter. Recover a real pointer containing that byte and calculate the resulting address before using the overlap.

**Checkpoint:** the intended pointer byte changes while the surrounding object survives its consistency checks. Keep alpha and beta runtime/protection assumptions separate. Source: `ctf-pwn/pwnable-tw/bounty_program_b.md`.

### 37. `hitcon_ftp`: protocol state supplies both a leak and a copy size

**Prerequisites:** MessagePack parsing, multi-packet protocol state, stack canaries, seccomp-aware ROP.

The detailed writeup identifies an option-type check performed only for one array length, enabling type confusion with a longer array. It separately describes a large negotiated block length used for formatting into a fixed **stack** buffer. The index's generic heap-corruption wording loses this distinction.

**Checkpoint:** decode a minimal valid request first, then show the unchecked object interpretation and the measured stack-write length independently. Preserve the canary and use the actual permitted output descriptor for a later ORW chain. Source: `ctf-pwn/pwnable-tw/hitcon_ftp.md`.

### 38. `seccomptools`: emulator/kernel disagreement is the first bug

**Prerequisites:** classic BPF, `seccomp_data`, return actions, FILE dispatch.

The detailed source says the user-space emulator fails to implement a length-load instruction that the kernel evaluates differently. A filter accepted under one model can therefore produce a different syscall result in the other. The proposed chain then exploits a synthetic zero return and a stream-pointer overwrite; it is not simply a generic heap-hook attack as the index suggests.

**Checkpoint:** compare both evaluators on the exact small filter before constructing a larger chain. Distinguish `ERRNO(0)` suppressing a syscall from a real successful file open. Source: `ctf-pwn/pwnable-tw/seccomptools.md`.

### 39. `stupid_boss`: compatible names do not imply compatible layouts

**Prerequisites:** C++ class layouts, type confusion, floating-point bit encoding, failed numeric conversions.

The detailed source describes compatibility checks that allow one language object's setter to operate on another layout. A double-valued setter can overwrite a pointer field, while another setter later dereferences it for reading or writing. The directory index's employee-UAF story is inconsistent with these details and is not used as the primary explanation.

**Checkpoint:** compare the two concrete field layouts and show exactly which eight bytes the setter changes. A failed `scanf` conversion may expose stale stack data, but confirm the leaked value's origin before using it. Source: `ctf-pwn/pwnable-tw/stupid_boss.md`.

### 40. `digimon`: start with parser state, not an assumed race

**Prerequisites:** unterminated input, `strtok` mutation, stack indices, asynchronous program state.

The individual writeup prioritizes a full command buffer lacking a NUL terminator, allowing tokenization to reach an adjacent partner index. It also identifies failed numeric conversions as a disclosure path and marks several apparent races/overflows as non-exploitable. The index's generic race-UAF description is therefore insufficient.

**Checkpoint:** use a full-length command to observe the exact index mutation and the subsequent task lookup. Preserve negative findings; do not spend time racing a path the detailed analysis says lacks the needed primitive. Source: `ctf-pwn/pwnable-tw/digimon.md`.

### 41. `omegago`: gameplay controls memory representation

**Prerequisites:** game-state transitions, history bounds, packed two-bit cells, fake-object construction.

The detailed route overfills a board-history array through repeated legal capture cycles, reaching adjacent state. A regret operation then dereferences altered history pointers. Controlled board bits can encode metadata, but each desired bit pattern must also be reachable through the game's rules.

**Checkpoint:** reproduce a short cycle and count history growth, then verify the first out-of-bounds history slot. This differs from the directory index's simpler coordinate-to-GOT narrative. Source: `ctf-pwn/pwnable-tw/omegago.md`.

## Restricted-shell and historical runtime exercises

### 42. `bash`: distinguish policy gaps from memory corruption

**Prerequisites:** executable permissions, dynamic loader behavior, shell builtins, exact lab confinement.

One historical route relies on the sandbox removing execute permissions from programs while leaving a readable program usable through an executable loader. Another investigates an old `popd` memory-corruption bug. These are different mechanisms; enumerate only the capabilities of the supplied challenge image before selecting one.

**Checkpoint:** establish which permission or builtin behavior is actually available in the local lab. The original loopback flag service is internal to that image; do not treat loopback services on a competition workstation as challenge targets. Source: `ctf-pwn/pwnable-tw/bash.md`.

### 43. `bash_revenge`: a shell variable can become the reclaimed object

**Prerequisites:** the exact old Bash build, out-of-bounds free, Bash's allocator, `SHELL_VAR` layout.

The detailed writeup turns a malformed `popd` index into a free operation and reclaims the region through shell-variable activity. A variable's value pointer can disclose data, and its dynamic callback is a distinct later control target. Model Bash's allocator and variable lifetime rather than applying glibc chunk offsets blindly.

**Checkpoint:** show which address is freed, what allocation reuses it, and when variable expansion dereferences the changed field. All helper/service access stays inside the explicitly supplied practice environment. Source: `ctf-pwn/pwnable-tw/bash_revenge.md`.

## What to retain after finishing a case

Write five short items: the initial bug, the first reliable primitive, the missing information it supplies, the final trigger, and the assumptions specific to this artifact. Include a failing attempt that taught you something about layout or protocol. This produces a reusable solver notebook without turning old offsets into folklore.

The source directory index, `ctf-pwn/pwnable-tw/README.md`, is preserved as a historical catalog. Its entries for `re_alloc`, `de_aslr`, `food_store`, `hitcon_ftp`, `seccomptools`, `stupid_boss`, `digimon`, `omegago`, and related advanced cases require comparison with the individual files and actual binary. The atlas favors concrete per-case observations and explicitly leaves unverified exploit claims unverified.


---

<a id="14-advanced-crypto"></a>

# Advanced cryptography: choose a model you can verify

Use this chapter after [Cryptography](#07-cryptography). These techniques are retained because the original repository covers considerably more than introductory RSA and XOR. They are not a suggestion to run every attack against every number.

All Python demonstrations run locally with Python 3 in Windows WSL or Kali. Save the named files and run them with `python3`. Where a script imports `math_helpers`, use the helper file from chapter 07 in the same directory. Sage is optional on Kali: the approved sheet records it but gives no installation information. The approved crypto-attacks checkout is also Kali-specific. No online mathematical service is needed here.

## 1. RSA decision points beyond the elementary checks

| Evidence | Candidate technique | Required verification |
|---|---|---|
| Tiny private exponent with balanced primes | Wiener continued fractions | Recovered factors multiply to `n`; private exponent decrypts |
| Larger but unusually small private exponent | Boneh–Durfee lattice | The lattice bounds and model fit the challenge; candidate factors verify |
| Known contiguous bits of a prime or private exponent | Coppersmith/partial-key recovery | Construct the exact polynomial and unknown bound |
| Known small `dp` or `dq` | CRT exponent attack | Respect exponent bounds and recovered congruences |
| Smooth `p-1` or `p+1` | Pollard p−1 or Williams p+1 | GCD returns a proper factor, not 1 or `n` |
| Related messages under the same key | Franklin–Reiter/polynomial GCD | The relation is exact modulo `n` |
| Faulty CRT signature | Bellcore-style GCD | At least one residue remains correct |
| Encryption samples but hidden modulus | GCD of `m^e-c` values | Candidate modulus explains all samples |
| Repeated primes or noncoprime exponent | Root enumeration in prime powers | Enumerate all roots and verify each |

ROCA, restricted-digit primes, base-representation primes, dependent primes, and shared high/low bits are key-generation structures. Start by reproducing that generator on a tiny instance. A patterned decimal modulus does not establish patterned factors.

## 2. Wiener: a complete toy with candidate validation

Save as `wiener_toy.py`:

```python
from math import isqrt, gcd

def convergents(numerator, denominator):
    p0, p1, q0, q1 = 0, 1, 1, 0
    while denominator:
        a, remainder = divmod(numerator, denominator)
        p0, p1 = p1, a*p1+p0
        q0, q1 = q1, a*q1+q0
        yield p1, q1
        numerator, denominator = denominator, remainder

def wiener(e, n):
    for k, d in convergents(e, n):
        if k == 0 or (e*d-1) % k:
            continue
        phi = (e*d-1)//k
        total = n-phi+1
        discriminant = total*total-4*n
        if discriminant < 0:
            continue
        root = isqrt(discriminant)
        if root*root != discriminant or (total+root) % 2:
            continue
        p, q = (total+root)//2, (total-root)//2
        if p*q == n:
            return d, p, q
    return None

p, q, d = 1009, 1013, 5
phi, n = (p-1)*(q-1), p*q
assert gcd(d, phi) == 1
e = pow(d, -1, phi)
answer = wiener(e, n)
assert answer is not None and answer[0] == d
assert answer[1]*answer[2] == n
print(answer)
```

Wiener's sufficient bound assumes suitable prime sizes and a genuinely small private exponent. Failure does not prove secure key generation. Do not increase brute-force ranges blindly; inspect whether the source actually biases `d`.

## 3. Local smoothness factoring and fault checks

Save as `rsa_advanced_toys.py`:

```python
from math import gcd

def pollard_p_minus_one(n, bound):
    a = 2
    for j in range(2, bound+1):
        a = pow(a, j, n)
        candidate = gcd(a-1, n)
        if 1 < candidate < n:
            return candidate
        if candidate == n:
            return None
    return None

n = 257*1019
factor = pollard_p_minus_one(n, 30)
assert factor is not None and n % factor == 0
print('p-1 factor:', factor)

# A correct signature and one faulty CRT residue.
p, q, e, message = 61, 53, 17, 65
n = p*q
d = pow(e, -1, (p-1)*(q-1))
signature = pow(message, d, n)
# Adding p preserves the residue modulo p but changes it modulo q.
faulty = (signature+p) % n
factor = gcd(pow(faulty, e, n)-message, n)
assert factor == p
print('fault factor:', factor)
```

Pollard p−1 depends on smoothness of the factor's predecessor, not the size of the whole modulus. If the GCD becomes `n`, both factors may have entered the exponent; change the bound/base in a controlled local experiment.

Williams p+1 and ECM require different machinery. In the approved Kali crypto-attacks checkout, inspect the relevant implementation's signature and required parameters before importing it. Do not install YAFU: it is explicitly unapproved. A missing local factoring dependency is a limitation to record, not permission to upload the modulus.

## 4. Nonunique roots, Rabin, and unusual totients

Rabin encryption squares a message modulo `pq`. With distinct primes congruent to 3 modulo 4, square roots can be recovered separately and recombined into four candidates.

Save as `rabin_roots.py`:

```python
from math_helpers import crt

p, q, message = 11, 19, 42
n = p*q
ciphertext = message*message % n
rp = pow(ciphertext, (p+1)//4, p)
rq = pow(ciphertext, (q+1)//4, q)
roots = {crt([a, b], [p, q])
         for a in {rp, (-rp) % p}
         for b in {rq, (-rq) % q}}
assert message in roots
assert len(roots) == 4
assert all(x*x % n == ciphertext for x in roots)
print(sorted(roots))
```

Encoding or redundancy selects a candidate; the mathematics alone does not know the flag format. Repeated factors, roots modulo prime powers, Schmidt–Samoa `p²q`, quaternion exponents, and custom expressions such as `(p^4-1)(q^4-1)` need the group actually used by the program. Do not rename such an expression `phi` and assume textbook RSA proof applies.

If a modulus is hidden, collect several known plaintext/ciphertext pairs and compute local GCDs of exact encryption residuals. The result may be a multiple of `n`; require it to fit ciphertext ranges and every sample. Large exponents can make unreduced powers expensive, so assess input size first.

## 5. Small roots and polynomial relations

Coppersmith methods look for bounded integer roots of modular polynomials. Before opening a lattice tool, write:

```text
Ring and modulus: __________________________
Polynomial f(x): ___________________________
Unknown x represents: ______________________
Bound |x| < X: _____________________________
Known factor-size fraction beta: ___________
How candidate x recovers p/message: ________
```

A known-prefix message gives a polynomial such as `(prefix*2^t+x)^e-c`. A known prime prefix instead gives `known+x`, vanishing modulo an unknown factor of `n`. These are different `beta` cases. Linearly related messages suggest a polynomial GCD before a lattice.

**Optional Kali Sage**, first confirm `sage --version`. Save this illustrative, deliberately easy instance as `small_root.sage`:

```sage
N = 1000003 * 1000033
R.<x> = PolynomialRing(Zmod(N))
secret = 123
f = x - secret
roots = f.small_roots(X=2^10, beta=1)
assert secret in [ZZ(r) for r in roots]
assert all(f(r) == 0 for r in roots)
print(roots)
```

Run `sage small_root.sage`. This checks environment and syntax, not the feasibility of a hard RSA attack. For the actual challenge, derive the polynomial and bounds from source. A monic-polynomial requirement, noninvertible leading coefficient, wrong root size, or wrong modulus commonly causes failure.

Hensel lifting solves roots modulo `p^k` from roots modulo `p` when its derivative conditions hold. If the derivative vanishes modulo `p`, branches can disappear or multiply; do not apply the simple-root formula blindly. Polynomial CRT over `GF(2)[x]` uses coprime polynomials, not integer moduli.

## 6. Discrete logarithms with explicit bounds

Baby-step giant-step uses about `sqrt(order)` storage and operations. Use it when that bound is realistically small, not for an arbitrary 256-bit prime-order group.

Save as `bsgs_toy.py`:

```python
from math import isqrt

def bsgs(g, h, p, order):
    width = isqrt(order)+1
    table = {}
    value = 1
    for j in range(width):
        table.setdefault(value, j)
        value = value*g % p
    step = pow(pow(g, width, p), -1, p)
    value = h
    for i in range(width+1):
        if value in table:
            candidate = i*width+table[value]
            if candidate < order and pow(g, candidate, p) == h:
                return candidate
        value = value*step % p
    return None

p, g, secret = 1019, 2, 123
h = pow(g, secret, p)
recovered = bsgs(g, h, p, p-1)
assert recovered == secret
print(recovered)
```

For Pohlig–Hellman, factor the **group order**, solve prime-power subgroup logarithms, then use CRT. A smooth `p-1` helps finite-field DH only if the actual generator order inherits the small factors. For ECC, use the curve/subgroup order, not `p-1`.

Sparse exponents can permit a meet-in-the-middle search over positions instead of all integer values. Count combinations first and verify the sparsity promise from source. A low Hamming weight guess without evidence can be more expensive than ordinary BSGS.

## 7. Elliptic-curve triage

Write down the curve model, field, coefficients, base point, subgroup order, cofactor, point encoding, and validation routine. The following are distinct failure families:

| Family | Observable prerequisite | Starting calculation |
|---|---|---|
| Singular curve | Discriminant vanishes | For short Weierstrass, check `4*a^3+27*b^2 == 0 mod p` |
| Anomalous curve | Curve order equals field prime | Compute/confirm `#E(Fp) == p` before considering Smart's attack |
| Small subgroup | Accepted low-order point and reused scalar | Determine point order; compare oracle outputs for each residue |
| Invalid curve | Coordinates accepted without curve membership check | Check whether scalar multiplication formulas ignore a supplied coefficient |
| Weak twist | X-coordinate-only multiplication plus weak twist order | Analyze the twist order and low-order acceptance |
| MOV reduction | Small embedding degree | Find small `k` for which subgroup order divides `p^k-1` |
| Nonce reuse/bias | Repeated `r`, partial nonce bits, or biased generation | Verify message hashing; then reuse formulas or HNP |
| Faults | Corrupted scalar multiplication or signature | Determine which intermediate relation remains valid |

Point negation, infinity encoding, and malformed points differ across libraries. X25519 low-order input can produce an all-zero shared secret; check whether the protocol rejects it. Ed25519 torsion issues depend on point validation and the verification equation. A cofactor greater than one is not by itself an exploit.

Clock groups satisfying `x²+y²=1`, singular curves with additive/multiplicative parameterizations, and endomorphism-based constructions can reduce to more familiar groups. Derive and test the map on toy points: it must preserve the operation and handle exceptional points. CM/GLV structure alone does not break correctly implemented standard curves.

Isogeny challenges need the exact curve and isogeny construction. Determine what the public key reveals and whether parameters are deliberately weakened; do not treat an isogeny keyword as permission to apply an unrelated historical attack.

## 8. Linear algebra over GF(2)

CRC adjustments, linear PRNGs, XOR aggregate hashes, and some stream-cipher leaks become binary linear systems. Each equation is a bitmask of coefficients plus one result bit. Bit order must match the source.

Save as `gf2_solve.py`:

```python
def solve_gf2(equations, variables):
    rows = [[mask, rhs] for mask, rhs in equations]
    pivots = []
    next_row = 0
    for column in range(variables):
        selected = next((i for i in range(next_row, len(rows))
                         if (rows[i][0] >> column) & 1), None)
        if selected is None:
            continue
        rows[next_row], rows[selected] = rows[selected], rows[next_row]
        for i in range(len(rows)):
            if i != next_row and ((rows[i][0] >> column) & 1):
                rows[i][0] ^= rows[next_row][0]
                rows[i][1] ^= rows[next_row][1]
        pivots.append(column)
        next_row += 1
    if any(mask == 0 and rhs for mask, rhs in rows):
        raise ValueError('inconsistent system')
    if len(pivots) != variables:
        raise ValueError('underdetermined: collect independent equations')
    result = 0
    for row, column in enumerate(pivots):
        result |= rows[row][1] << column
    return result

secret = 0b1011
masks = [0b0011, 0b0110, 0b1100, 0b1000]
equations = [(mask, (mask & secret).bit_count() & 1) for mask in masks]
recovered = solve_gf2(equations, 4)
assert recovered == secret
assert all(((mask & recovered).bit_count() & 1) == rhs
           for mask, rhs in equations)
print(bin(recovered))
```

If rank is low, more repeated versions of the same equation will not help. Choose inputs that excite different state bits. For affine CRC relations, subtract/XOR a fixed baseline before building the linear matrix. Validate the final patch with the original checksum routine.

## 9. LFSR recovery with Berlekamp–Massey

Save as `lfsr_bm.py`:

```python
def berlekamp_massey(bits):
    size = len(bits)
    C, B = [0]*(size+1), [0]*(size+1)
    C[0] = B[0] = 1
    length, since = 0, 1
    for n in range(size):
        discrepancy = bits[n]
        for i in range(1, length+1):
            discrepancy ^= C[i] & bits[n-i]
        if discrepancy == 0:
            since += 1
            continue
        old = C[:]
        for j in range(size+1-since):
            C[j+since] ^= B[j]
        if 2*length <= n:
            length = n+1-length
            B = old
            since = 1
        else:
            since += 1
    return length, C[:length+1]

bits = [1, 0, 0, 1]
for i in range(4, 60):
    bits.append(bits[i-1] ^ bits[i-4])
length, coefficients = berlekamp_massey(bits[:30])
predicted = bits[:30]
for n in range(30, 60):
    bit = 0
    for i in range(1, length+1):
        bit ^= coefficients[i] & predicted[n-i]
    predicted.append(bit)
assert length == 4
assert predicted == bits
print(length, coefficients)
```

Expected recurrence coefficients are `[1, 1, 0, 0, 1]`. Always verify on held-out bits. Fibonacci versus Galois form, reversed bit order, discarded warmup, and output filters can make a correct polynomial appear wrong.

RC4 second-byte bias is statistical across many independent keys; it is not a deterministic two-byte decryption trick. RC4A, VMPC, and Spritz modify the generator, so identify the update algorithm. Trivium, Grain, and Mickey analyses depend strongly on reduced rounds, warmup, and access to chosen IVs.

## 10. Lattices: build the equations before the basis

LLL finds a reduced basis; it is not a command that directly returns a private key. BKZ is stronger and more expensive. Babai estimates a nearby lattice point; exact CVP/SVP have different costs. A short output row must be interpreted and checked in the original problem.

For each lattice write down row/column orientation, modulus, scaling, unknown bounds, error distribution, and extraction rule. Make a tiny generated instance where the secret is known. Recover that secret before increasing dimensions.

| Problem | Equation to derive | Most common modelling error |
|---|---|---|
| Hidden Number Problem | Signature relation with bounded nonce error | Using field prime instead of signature order; wrong known-bit offset |
| Truncated LCG | State recurrence plus missing low/high bits | Treating returned output as full state |
| LWE | `b = A*s + e mod q` | Incorrect centered residues or error scale |
| Approximate GCD | Samples `p*q_i + r_i` with small `r_i` | Residuals too large for the assumed bound |
| Subset sum | `sum(a_i*x_i) = target`, `x_i in {0,1}` | Losing the binary constraint after reduction |
| GGH | Ciphertext near a lattice point | Confusing basis coordinates with ambient coordinates |
| NTRU | Polynomial relation with short private polynomials | Wrong cyclic/negacyclic convolution |
| Orthogonal/HSSP families | Hidden structure orthogonal to supplied samples | Too few independent samples |

On **Kali**, inspect the installed checkout locally:

```bash
rg --files /opt/tools/crypto-attacks | rg 'hidden_number|lwe|coppersmith|knapsack|lcg'
```

Read the selected function, its examples, and imports. Inputs and dependencies are not uniform across attacks. If Sage is unavailable, basic exact arithmetic remains usable, but a high-dimensional lattice attack may be blocked by the environment. Record that honestly rather than silently using an online solver.

Ring-LWE and Module-LWE can be flattened into matrices, but only with the correct coefficient ordering and ring reduction. In `Zq[x]/(x^n+1)`, wraparound changes sign. Structured flattening does not make secure ML-KEM parameters easy to solve.

BDD predicates and LadderLeak-style leakage use additional side information, not just a generic lattice basis. Count how much information each signature gives and whether the predicate is reliable. A tiny bias may require substantially more samples than a full known nonce bit.

## 11. Post-quantum recognition without misleading promises

ML-KEM/Kyber hints include module vectors, polynomial degree 256, modulus 3329, NTT operations, and compression. ML-DSA/Dilithium uses a different modulus and signature structure. Confirm the source instead of classifying by a single constant.

Look for challenge-specific departures: unusually tiny dimensions, exposed noise, repeated randomness, unchecked verification fields, corrupted signatures, or implementation faults. Kannan embeddings, algebraic Arora–Ge models, and primal/dual estimators answer different questions. An estimator predicts cost; it does not recover a secret.

MAYO and other multivariate signatures require the actual public polynomial system and fault model. A malformed signature only helps if it reveals a relation to secret structure. Keep the mathematics local; AI/ML libraries remain forbidden even when a cryptographic scheme has a similar abbreviation.

## 12. Shamir and CRT secret sharing

Save as `shamir_toy.py`:

```python
prime = 2089
secret = 1234

def polynomial(x):
    return (secret + 17*x + 29*x*x) % prime

shares = [(x, polynomial(x)) for x in [1, 2, 3]]
recovered = 0
for i, (xi, yi) in enumerate(shares):
    basis = 1
    for j, (xj, _) in enumerate(shares):
        if i != j:
            basis = basis * (-xj) * pow(xi-xj, -1, prime) % prime
    recovered = (recovered + yi*basis) % prime
assert recovered == secret
print(recovered)
```

Repeated x-coordinates do not add independent shares. Deterministic coefficients or polynomial reuse across sessions can create extra equations; compare coefficients/outputs algebraically rather than assuming all same-threshold schemes are vulnerable.

Asmuth–Bloom uses a different CRT-based construction with size inequalities. Recovering a congruence class is not enough if several candidates remain within the allowed secret range. Check those bounds explicitly.

## 13. Authenticated encryption and reduced-round designs

GCM nonce reuse repeats CTR keystream and creates equations involving GHASH's authentication subkey. GHASH works in `GF(2^128)` with a specified bit convention; integer arithmetic modulo a large prime is not interchangeable. Full/partial tags, associated data, ciphertext lengths, and multiple polynomial roots all affect recovery.

ChaCha20-Poly1305 reuse involves a reused one-time Poly1305 key and stream. Poly1305 arithmetic is modulo `2^130-5`, while the final tag reduction and clamping add constraints. Recover candidate keys from complete message/tag equations and validate on a second independent pair before forging a toy message. A ciphertext XOR alone does not recover a valid tag.

Partitioning oracles and non-key-committing AEAD need a verifier that reveals which candidate key accepts a crafted ciphertext. Establish the acceptance predicate and candidate key set. They are not a generic way to crack arbitrary AEAD passwords.

Reduced-round AES Square attacks require chosen plaintext sets with the required balanced structure. S-box intersection needs controlled differences and an identifiable round boundary. Non-permutation S-boxes can yield collisions, but the collision must survive the surrounding rounds. ForkAES reflective differentials and faulty ChaCha rotations similarly require the exact modified construction.

For sponge designs, record rate, capacity, permutation, domain separation, padding, and round count. Keccak, Ascon, Gimli, and Sparkle are not interchangeable. A small-capacity meet-in-the-middle toy does not imply an attack on a full-strength standardized hash.

## 14. RSA oracles: define the predicate precisely

| Oracle | Predicate | Suitable next step |
|---|---|---|
| Parity/LSB | Decrypted integer is even/odd | Multiply ciphertext by `2^e`; maintain exact rational/integer intervals |
| PKCS#1 v1.5 | Plaintext is a conforming `00 02 ... 00 ...` block | Bleichenbacher interval search with the actual full validation predicate |
| Leading-byte/OAEP | Decrypted representative is below a boundary | Manger-style interval narrowing only if that predicate is observable |
| Noisy bit | Correct predicate with measurable error | Repeated controls, confidence estimate, and error-correcting recovery |
| Timing | Distribution depends on an internal operation | Collect matched controls; confirm relation before recovery |

An error string may combine several rejection stages. If the service checks a hash, length, padding, and text decoding, identify which stage creates the signal. Bleichenbacher and Manger are query-sensitive; estimate the budget before committing.

Use exact fractions or integer intervals, never floating-point bounds. At the end, search the tiny remaining interval and re-encrypt every candidate. With noisy observations, retain uncertainty or backtrack rather than allowing one wrong bit to corrupt the whole result.

## 15. Zero-knowledge proofs, signatures, and garbled circuits

Start by identifying the statement the verifier actually checks. Record public inputs, witness-dependent commitments, challenge derivation, transcript order, and state update. The challenge may be in the protocol wrapper rather than the proof system.

| Source topic | Diagnostic | Constraint |
|---|---|---|
| Schnorr-style proof replay | Compare commitment/challenge/response across sessions | Reused commitment with distinct challenges can expose a witness |
| Fiat–Shamir mistakes | Recompute the transcript hash locally | Missing identity, statement, or commitment binding creates a specific gap |
| Groth16 setup degeneration | Inspect provided verifying/proving key relations | A relation such as equal setup elements needs its exact pairing equation |
| Unconstrained nullifier | Compare circuit inputs with state replay checks | Valid proof does not imply a unique authorized action |
| KZG/pairing oracle | Write the accepted pairing identity | Need the actual oracle outputs and algebraic relation |
| DV-SNARG verifier oracle | Determine precisely what is queryable | A boolean verifier alone may not reveal useful linear data |
| FROST threshold signing | Track participant IDs, nonce commitments, binding factors | FROST is a threshold Schnorr protocol, not inherently a lattice scheme |
| Free-XOR garbled circuits | Compare label pairs for shared global delta | Access to a matching label pair or leaked metadata is required |

The source's FROST heading can mislead: classify the concrete construction from its equations, not that label. Likewise, a proof accepted once does not prove arbitrary proof forgery; replay and unconstrained public input are separate findings.

Graph three-coloring and other constraint puzzles can be modelled with a non-AI SMT library if available under the Python-library rule. Bound every variable and verify the model against the original checker. Bit-vectors use fixed-width arithmetic; integers do not overflow unless explicitly constrained.

## 16. Unusual algebra: reduce to something measurable

| Construction in the sources | First diagnostic | Useful next action |
|---|---|---|
| Paillier/homomorphic oracle | Verify additive homomorphism on toy messages | Determine whether size, parity, or comparison leaks plaintext information |
| ElGamal | Check group order and public element order | Trivial `p-1` elements leak only a small class; use the actual order |
| Matrix ElGamal/Cayley–Purser | Compute characteristic polynomial and centralizers | Test whether conjugation invariants reduce the secret search |
| Tropical semiring | Confirm min-plus or max-plus convention | Residuation solves inequalities; verify equality separately |
| Braid-group DH | Identify computable representation/invariant | Test whether Alexander polynomial or another invariant preserves needed structure |
| Permutation/icosahedral group | Express generators as explicit permutations | Enumerate the finite subgroup and map ciphertext action |
| Monotone function | Prove direction and domain bounds | Binary search, with exact comparisons and truncation accounted for |
| Goldwasser–Micali | Identify quadratic-residuosity encoding | Replication helps only with a matching acceptance oracle |
| BB84 simulation | Trace basis choices, sifting, and authentication | Unauthenticated classical exchange differs from breaking quantum mechanics |
| Differential-privacy noise | Check whether repeated samples share a secret and independent noise | Estimate with uncertainty; bounded query budget and correlated noise matter |

For a matrix or exotic group, verify the operation, identity, inverse, and order on small examples before porting an integer attack. Singular matrices and noncommutative multiplication can invalidate familiar formulas.

BIP39 partial-mnemonic puzzles combine a finite word-index space, checksum bits, and often a known address. Recover only organizer-provided toy wallets. Do not query public wallet services with private material; checksum acceptance alone does not establish the target wallet.

## 17. Historical, media, and error-correcting crypto

Lorenz/Tunny and rotating-wheel ciphers need their alphabet encoding, wheel lengths, stepping rules, and alignment. Start with a short known plaintext and check wheel motion; do not apply ordinary Vigenère frequency analysis to teleprinter bits unchanged.

Hamming codes and interleaving are error correction, not encryption. Identify codeword size, parity placement, and interleaver permutation; compute syndromes on a few known words before decoding an entire file. Nibble-reassembly and random-padding formats similarly need a field layout before byte reconstruction.

For image shifts, grid permutations, and Arnold-cat-map scrambling, preserve dimensions and distinguish coordinate transforms from pixel-value transforms. Check one round on a coordinate grid, then invert it. A visually plausible image can still be mirrored or shifted by one pixel.

## 18. Stopping rules that save time

Stop an attack branch when its required structure is absent, its query budget exceeds the challenge limit, or a small known-secret instance fails. Record the failed condition. Continue with a different mathematically supported branch rather than increasing concurrency or switching to prohibited online analysis.

Before accepting a result, validate it outside the solver: re-encrypt, recompute signatures, regenerate outputs, satisfy the original polynomial equations, or run the challenge's local checker. A lattice vector, SMT model, root, or decoded string is only a candidate until it passes that check.


---

<a id="tool-matrix"></a>

# Tool matrix: the complete supplied list

Source: `AJCCBC_CTF2026_Tool_Review_List_261015r11.xlsx`. Recorded versions are copied as supplied, not independently verified. Blank installation notes do not establish availability. The unapproved reasons are retained verbatim. The workbook contains some replacement characters; these are preserved rather than guessed.

Windows/WSL and Kali are separate environments. See the location column before choosing a command. No row authorizes every plugin, dependency, or hosted service associated with a product.

## Windows / WSL · 39 entries

| Tool | Version | Installation/location | Notes/reason | Workbook source |
| --- | --- | --- | --- | --- |
| CyberChef | Latest (browser-based, no install) | Bookmark | — | Approved Tool List for Windows!C8 |
| Wireshark | Latest | installed in Windows | — | Approved Tool List for Windows!C9 |
| PDF Viewer | Any current version | installed in Windows | — | Approved Tool List for Windows!C10 |
| OpenVPN Client | Latest | installed in Windows | — | Approved Tool List for Windows!C11 |
| Google Chrome | Latest | installed in Windows | — | Approved Tool List for Windows!C12 |
| Windows Subsystem for Linux (WSL) | Latest | installed in Windows | — | Approved Tool List for Windows!C13 |
| Python 3 | Latest 3.x — confirm exact version before install | installed in WSL | Libraries may be added freely EXCEPT any AI/ML-related library (e.g. no LLM, machine-learning, or generative-AI frameworks).  | Approved Tool List for Windows!C14 |
| uv | Latest | installed in WSL | Same rule as Python 3 — any library OK except AI/ML-related packages | Approved Tool List for Windows!C15 |
| gdb | Latest (distro package) | installed in WSL | — | Approved Tool List for Windows!C16 |
| objdump | Bundled with GNU Binutils | installed in WSL | — | Approved Tool List for Windows!C17 |
| strings | Bundled with GNU Binutils | installed in WSL | — | Approved Tool List for Windows!C18 |
| zsteg | Latest (Ruby gem) | installed in WSL | — | Approved Tool List for Windows!C19 |
| binwalk | Latest | installed in WSL | — | Approved Tool List for Windows!C20 |
| ExifTool | Latest | installed in WSL | — | Approved Tool List for Windows!C21 |
| pdftotext (Poppler utils) | Latest | installed in WSL | — | Approved Tool List for Windows!C22 |
| can-utils | Latest | installed in WSL | — | Approved Tool List for Windows!C23 |
| cannelloni | Latest | installed in WSL | — | Approved Tool List for Windows!C24 |
| zeek | Latest | installed in WSL | — | Approved Tool List for Windows!C25 |
| ZBar | Latest | installed in WSL | — | Approved Tool List for Windows!C26 |
| Burp Suite Community Edition | 2026.4.x (confirm latest at install time) | installed in WSL | — | Approved Tool List for Windows!C27 |
| jq | Latest | installed in WSL | — | Approved Tool List for Windows!C28 |
| Ghidra | 12.1.4 | installed in WSL | — | Approved Tool List for Windows!C29 |
| The Sleuth Kit | Latest | installed in WSL | — | Approved Tool List for Windows!C30 |
| OpenSSL | Latest 3.x | installed in WSL | — | Approved Tool List for Windows!C31 |
| xz | Latest | installed in WSL | — | Approved Tool List for Windows!C32 |
| qpdf | Latest | installed in WSL | — | Approved Tool List for Windows!C33 |
| llvm-mc (LLVM tools) | Latest | installed in WSL | — | Approved Tool List for Windows!C34 |
| xxd | Bundled with Vim | installed in WSL | — | Approved Tool List for Windows!C35 |
| fsck.fat (dosfstools) | Latest | installed in WSL | — | Approved Tool List for Windows!C36 |
| RsaCtfTool | Latest (GitHub script, run via Python 3) | installed in WSL | — | Approved Tool List for Windows!C37 |
| volatility3 | Latest | installed in WSL | — | Approved Tool List for Windows!C38 |
| OpenSSH-Session-Key-Recovery | — | installed in volatility3 | Plugin for Volatility3 | Approved Tool List for Windows!C39 |
| x64dbg | Latest | installed in Windows | Portable zip (snapshot_*.zip). Extract and run; no installer. | Approved Tool List for Windows!C40 |
| Autopsy | Latest | installed in Windows | MSI installer (bundles Java and The Sleuth Kit). Administrator rights required. | Approved Tool List for Windows!C41 |
| HxD | Latest | installed in Windows | Installer or portable edition. | Approved Tool List for Windows!C42 |
| tshark | Latest | installed in Windows | Included in the Wireshark installer (TShark component). | Approved Tool List for Windows!C43 |
| Notepad++ | Latest | installed in Windows | Installer (x64). A portable edition is also available. | Approved Tool List for Windows!C44 |
| dnSpyEx (dnSpy) | Latest | installed in Windows | Portable zip. Use dnSpy-net-win64.zip (self-contained; no .NET installation needed). | Approved Tool List for Windows!C45 |
| Eric Zimmerman's Tools | Latest | installed in Windows | Run Get-ZimmermanTools.ps1 to download the tools. Internet access and the .NET Desktop Runtime are required. | Approved Tool List for Windows!C46 |

## Kali · 161 entries

| Tool | Version | Installation/location | Notes/reason | Workbook source |
| --- | --- | --- | --- | --- |
| .NET SDK | 6.0.400 | — | — | Approved Tool List for Kali!C8 |
| 7-Zip (7z) | 26.02 | — | — | Approved Tool List for Kali!C9 |
| aircrack-ng | 1.7 | — | — | Approved Tool List for Kali!C10 |
| ALEAPP (Android Logs Events And Protobuf Parser) | - | — | No installation information recorded | Approved Tool List for Kali!C11 |
| Android Studio | - | — | No installation information recorded | Approved Tool List for Kali!C12 |
| angr | (not captured) | pipx (angr) | — | Approved Tool List for Kali!C13 |
| AperiSolve | (not captured) | git (/opt/tools/AperiSolve) | — | Approved Tool List for Kali!C14 |
| Apktool | 2.7.0-dirty | — | — | Approved Tool List for Kali!C15 |
| asar (@electron/asar) | 4.3.1 | — | — | Approved Tool List for Kali!C16 |
| Audacity | (not captured) | /usr/bin/audacity | — | Approved Tool List for Kali!C17 |
| AutoIt-Ripper | (not captured) | pipx (autoit-ripper) | — | Approved Tool List for Kali!C18 |
| BinDiff | 8 | — | Build @568181968 (Sep 25 2023) | Approved Tool List for Kali!C19 |
| bkcrack | 1.8.1 (2025-10-25) | — | — | Approved Tool List for Kali!C20 |
| bulk_extractor | 2.1.1 | — | — | Approved Tool List for Kali!C21 |
| bvi | (not captured) | — | Interactive tool; the version check returned 'Input is not from a terminal' | Approved Tool List for Kali!C22 |
| Bytecode Viewer | 2.13.2 | Fat Jar | — | Approved Tool List for Kali!C23 |
| bzip2 | 1.0.8 | — | — | Approved Tool List for Kali!C24 |
| cabextract | 1.11 | — | — | Approved Tool List for Kali!C25 |
| capa | 9.4.0 | — | — | Approved Tool List for Kali!C26 |
| Chainsaw | 2.16.5 | — | — | Approved Tool List for Kali!C27 |
| checksec | 2.6.0 | — | — | Approved Tool List for Kali!C28 |
| crypto-attacks | (not captured) | git (/opt/tools/crypto-attacks) | — | Approved Tool List for Kali!C29 |
| curl | 8.21.0 | — | — | Approved Tool List for Kali!C30 |
| Cutter | (not captured) | AppImage (/opt/tools/cutter.AppImage) | The GUI needs FUSE | Approved Tool List for Kali!C31 |
| DB Browser for SQLite | 3.13.1 | — | — | Approved Tool List for Kali!C32 |
| DBeaver Community Edition | 26.1.3 | — | — | Approved Tool List for Kali!C33 |
| Detect It Easy (DIE) | 3.21 | — | — | Approved Tool List for Kali!C34 |
| dex2jar | 2.1-nightly-28 | — | — | Approved Tool List for Kali!C35 |
| Didier Stevens Beta tools (onedump.py) | (not captured) | git (/opt/tools/Beta) | — | Approved Tool List for Kali!C36 |
| Didier Stevens Suite (pdfid.py, pdf-parser.py, oledump.py and others) | (not captured) | git (/opt/tools/DidierStevensSuite) | — | Approved Tool List for Kali!C37 |
| Docker Engine and Compose plugin | 28.5.2+dfsg4 | — | — | Approved Tool List for Kali!C38 |
| dwarf2json | 0.9.0 | — | — | Approved Tool List for Kali!C39 |
| Eclipse Temurin JDK (OpenJDK) | 25.0.4 (2026-07-21) | — | Reported as 'openjdk' | Approved Tool List for Kali!C40 |
| ewf-tools (libewf) | 20140816 | — | — | Approved Tool List for Kali!C41 |
| Exploit-DB / searchsploit (offline archive) | 2026-08-19 | — | Version is the archive date | Approved Tool List for Kali!C42 |
| factordb-python | (not captured) | pip (factordb-python) | — | Approved Tool List for Kali!C43 |
| FakeNet-NG | (not captured) | /opt/tools/flare-fakenet-ng (fakenet in PATH) | — | Approved Tool List for Kali!C44 |
| Fernflower | (not captured) | /opt/tools/fernflower/build/libs/fernflower.jar (/usr/local/bin/fernflower) | — | Approved Tool List for Kali!C45 |
| Feroxbuster | 2.13.1 | — | — | Approved Tool List for Kali!C46 |
| FFmpeg | (not captured) | apt (ffmpeg) | — | Approved Tool List for Kali!C47 |
| ffuf | 2.1.0-dev | — | — | Approved Tool List for Kali!C48 |
| file (libmagic) | 5.47 | — | — | Approved Tool List for Kali!C49 |
| FLOSS (FLARE Obfuscated String Solver) | (not captured) | pipx (flare-floss) | — | Approved Tool List for Kali!C50 |
| foremost | (not captured) | — | Installed; version not captured | Approved Tool List for Kali!C51 |
| FQLite | (not captured) | /opt/fqlite/bin/fqlite (symlinked to /usr/local/bin) | — | Approved Tool List for Kali!C52 |
| Frida | 17.23.3 | — | — | Approved Tool List for Kali!C53 |
| GCC, G++ and build tools (build-essential, make, CMake, pkg-config) | 15.3.0 | — | Debian gcc 15.3.0-2 | Approved Tool List for Kali!C54 |
| GEF (GDB Enhanced Features) | (not captured) | /opt/tools/gef.py | Load with: gdb -x /opt/tools/gef.py. Not auto-sourced, to avoid a clash with peda | Approved Tool List for Kali!C55 |
| Git | 2.53.0 | — | — | Approved Tool List for Kali!C56 |
| Gitleaks | (not captured) | — | The tool does not report a version (set at build time) | Approved Tool List for Kali!C57 |
| G'MIC (gmic) | (not captured) | — | Version not captured (the command started the G'MIC interpreter) | Approved Tool List for Kali!C58 |
| GNU Wget | 1.25.0 | — | — | Approved Tool List for Kali!C59 |
| Go | 1.26.5 | — | — | Approved Tool List for Kali!C60 |
| Gobuster | 3.8.2 | — | — | Approved Tool List for Kali!C61 |
| GoReSym | (not captured) | go install (github.com/mandiant/GoReSym@latest) | — | Approved Tool List for Kali!C62 |
| GTFOBins (offline copy) | (not captured) | git (/opt/tools/GTFOBins.github.io) | — | Approved Tool List for Kali!C63 |
| gzip | 1.13 | — | — | Approved Tool List for Kali!C64 |
| HackTricks (offline copy) | (not captured) | git (/opt/tools/hacktricks) | — | Approved Tool List for Kali!C65 |
| hashcat | 7.1.2 | — | — | Approved Tool List for Kali!C66 |
| hashid | 3.1.4 | — | — | Approved Tool List for Kali!C67 |
| Hayabusa | (not captured) | — | Version not captured (the --version option is not supported) | Approved Tool List for Kali!C68 |
| hcxtools | 7.1.2 | — | Version of hcxpcapngtool | Approved Tool List for Kali!C69 |
| Hindsight (pyhindsight) | (not captured) | pipx (pyhindsight) | — | Approved Tool List for Kali!C70 |
| hlextend | (not captured) | Python module (/usr/local/lib/python3.14/dist-packages/hlextend.py) | — | Approved Tool List for Kali!C71 |
| Hydra | (not captured) | — | Installed; version not captured | Approved Tool List for Kali!C72 |
| iLEAPP (iOS Logs, Events, And Plists Parser) | - | — | No installation information recorded | Approved Tool List for Kali!C73 |
| ImageMagick | 7.1.2-27 | — | — | Approved Tool List for Kali!C74 |
| Impacket | 0.14.0 | — | — | Approved Tool List for Kali!C75 |
| innoextract | dev build | — | — | Approved Tool List for Kali!C76 |
| internet_detector | (not captured) | apt (inetsim) | Provided by the apt package 'inetsim' | Approved Tool List for Kali!C77 |
| IPython | 9.17.1 | — | — | Approved Tool List for Kali!C78 |
| jadx (jadx-gui) | 1.5.6 | — | — | Approved Tool List for Kali!C79 |
| John the Ripper (jumbo) | 1.9.0-Jumbo-1 | — | — | Approved Tool List for Kali!C80 |
| Jpeginfo | 1.7.1 | — | — | Approved Tool List for Kali!C81 |
| js-beautify | 2.0.3 | — | — | Approved Tool List for Kali!C82 |
| js-deobfuscator | (not captured) | npm (js-deobfuscator) | — | Approved Tool List for Kali!C83 |
| jwt_tool | (not captured) | /opt/tools/jwt_tool (/usr/local/bin/jwt_tool) | — | Approved Tool List for Kali!C84 |
| Katana | (not captured) | go install (github.com/projectdiscovery/katana/cmd/katana@latest) | — | Approved Tool List for Kali!C85 |
| legion | 0.7.0 | — | — | Approved Tool List for Kali!C86 |
| libesedb tools | 20240420 | — | Version of esedbexport | Approved Tool List for Kali!C87 |
| LibreOffice | 26.8.0.3 | — | — | Approved Tool List for Kali!C88 |
| lrzip | 0.660 | — | — | Approved Tool List for Kali!C89 |
| ltrace | 0.7.91 | — | — | Approved Tool List for Kali!C90 |
| lz4 | 1.10.0 | — | — | Approved Tool List for Kali!C91 |
| lzip | 1.26 | — | — | Approved Tool List for Kali!C92 |
| mac_apt | (not captured) | git (/opt/tools/mac_apt) | — | Approved Tool List for Kali!C93 |
| MediaInfo | (not captured) | — | Version not captured | Approved Tool List for Kali!C94 |
| Metasploit Framework | 6.5.2-dev | — | — | Approved Tool List for Kali!C95 |
| mimikatz | 2.2.0 | Wine (Windows binary) | — | Approved Tool List for Kali!C96 |
| Miniforge3 (conda) | (not captured) | /home/kali/miniforge3 | — | Approved Tool List for Kali!C97 |
| multimon-ng | (not captured) | apt (multimon-ng) | — | Approved Tool List for Kali!C98 |
| mupdf-tools (mutool) | 1.27.0 | — | — | Approved Tool List for Kali!C99 |
| NASM (Netwide Assembler) | 3.01 | — | — | Approved Tool List for Kali!C100 |
| Nmap (with Ncat / Nping) | 7.99 | — | — | Approved Tool List for Kali!C101 |
| Node.js (with npm) | 24.21.0 | — | — | Approved Tool List for Kali!C102 |
| obfuscator-io-deobfuscator | 1.0.6 | — | — | Approved Tool List for Kali!C103 |
| Obsidian | (not captured) | — | Version not captured; startup reported that ~/.config/obsidian/obsidian.json does not exist | Approved Tool List for Kali!C104 |
| oletools (full suite: olevba, oleid, oleobj, rtfobj, mraptor, msodde, olemeta, oletimes, pyxswf) | (not captured) | pipx (oletools) | — | Approved Tool List for Kali!C105 |
| OllyDbg | 1.10-1kali5 | Wine (Windows binary) | — | Approved Tool List for Kali!C106 |
| OpenStego | (not captured) | GitHub .deb package | — | Approved Tool List for Kali!C107 |
| padding-oracle-attacker | (not captured) | — | Version not captured (the command printed a banner only) | Approved Tool List for Kali!C108 |
| PARI/GP | 2.17.4 | — | — | Approved Tool List for Kali!C109 |
| PayloadsAllTheThings (offline copy) | (not captured) | git (/opt/tools/PayloadsAllTheThings) | — | Approved Tool List for Kali!C110 |
| peda | (not captured) | /opt/tools/peda (sourced in ~/.gdbinit) | — | Approved Tool List for Kali!C111 |
| peepdf-3 | (not captured) | pipx (peepdf-3) | — | Approved Tool List for Kali!C112 |
| pff-tools (libpff) | 20231205 | — | Version of pffexport | Approved Tool List for Kali!C113 |
| Plaso (log2timeline, psort, pinfo) | 20260119-1kali1 | — | — | Approved Tool List for Kali!C114 |
| pngcheck | (not captured) | apt (pngcheck) | — | Approved Tool List for Kali!C115 |
| pwndbg | (not captured) | /opt/tools/pwndbg | setup.sh completed | Approved Tool List for Kali!C116 |
| pycdc (Decompyle++) | (not captured) | — | Version not captured (no --version option) | Approved Tool List for Kali!C117 |
| pyinstxtractor-ng | (not captured) | pipx (pyinstxtractor-ng) | — | Approved Tool List for Kali!C118 |
| pypykatz | 0.6.13 | — | — | Approved Tool List for Kali!C119 |
| Python 2.7 | 2.7.18 | — | — | Approved Tool List for Kali!C120 |
| Python 3.11 (via uv) | - | — | No installation information recorded | Approved Tool List for Kali!C121 |
| qemu-img (qemu-utils) | 11.0.3 | — | — | Approved Tool List for Kali!C122 |
| radare2 | 6.0.5 | — | — | Approved Tool List for Kali!C123 |
| rat-king-parser | 4.2.4 | — | — | Approved Tool List for Kali!C124 |
| RegRipper | 3.0 | — | — | Approved Tool List for Kali!C125 |
| ripgrep (rg) | 15.2.0 | — | — | Approved Tool List for Kali!C126 |
| rockyou.txt (Kali 'wordlists' package) | (not captured) | /usr/share/wordlists/rockyou.txt | — | Approved Tool List for Kali!C127 |
| ROPgadget | 7.7 | — | — | Approved Tool List for Kali!C128 |
| rtptools (rtpdump, rtpplay and others) | (not captured) | /opt/tools/rtptools | Built from source | Approved Tool List for Kali!C129 |
| Rust (rustup, rustc, cargo) | 1.95.0 (2026-04-14) | — | Built from a source tarball | Approved Tool List for Kali!C130 |
| rustscan | 2.4.1 | — | — | Approved Tool List for Kali!C131 |
| SageMath | - | — | No installation information recorded | Approved Tool List for Kali!C132 |
| SecLists | (not captured) | /usr/bin/seclists | — | Approved Tool List for Kali!C133 |
| socat | 1.8.1.3 | — | — | Approved Tool List for Kali!C134 |
| Sonic Visualiser | 5.2.1 | — | — | Approved Tool List for Kali!C135 |
| SoX (Sound eXchange) | 14.7.1.2 | — | SoX_ng build | Approved Tool List for Kali!C136 |
| SQLCipher Community Edition — CLI | SQLite 3.53.4 / SQLCipher 4.18.0 | — | — | Approved Tool List for Kali!C137 |
| sqlite3 | 3.53.4 | — | — | Approved Tool List for Kali!C138 |
| sqlmap | 1.10.8 (stable) | — | — | Approved Tool List for Kali!C139 |
| sstv (command-line SSTV decoder) | (not captured) | pip (PySSTV) | — | Approved Tool List for Kali!C140 |
| steghide | 0.6.0 | — | — | Approved Tool List for Kali!C141 |
| stegseek | 0.6 | — | — | Approved Tool List for Kali!C142 |
| stegsnow (SNOW) | (not captured) | apt (stegsnow) | — | Approved Tool List for Kali!C143 |
| StegSolve | (not captured) | — | Version not captured (GUI tool; it was started without a display) | Approved Tool List for Kali!C144 |
| strace | 7.0 | — | — | Approved Tool List for Kali!C145 |
| Subfinder | 2.16.0 | — | — | Approved Tool List for Kali!C146 |
| Sublime Text | Build 4215 | — | — | Approved Tool List for Kali!C147 |
| tar | 1.35 | — | — | Approved Tool List for Kali!C148 |
| tcpdump | 4.99.6 | — | — | Approved Tool List for Kali!C149 |
| TestDisk and PhotoRec | 7.2 | — | — | Approved Tool List for Kali!C150 |
| unar | 1.10.8 | — | — | Approved Tool List for Kali!C151 |
| uncompyle6 | 3.9.3 | — | — | Approved Tool List for Kali!C152 |
| unpyc3 (unpyc37-3.10) | (not captured) | git (/opt/tools/unpyc3) | — | Approved Tool List for Kali!C153 |
| unrar | (not captured) | /usr/bin/unrar | — | Approved Tool List for Kali!C154 |
| unzip | 6.0-30 | — | — | Approved Tool List for Kali!C155 |
| UPX | 4.2.4 | — | — | Approved Tool List for Kali!C156 |
| Visual Studio Code | 1.141.2 | — | — | Approved Tool List for Kali!C157 |
| Volatility 2 | (not captured) | git (/opt/tools/volatility) | — | Approved Tool List for Kali!C158 |
| Volatility 2 community plugins | (not captured) | git (/opt/tools/community) | — | Approved Tool List for Kali!C159 |
| Volatility 2 profiles (Linux and macOS) | (not captured) | git (/opt/tools/profiles) | — | Approved Tool List for Kali!C160 |
| Volatility 3 community plugins (community3) | (not captured) | git (/opt/tools/community3) | — | Approved Tool List for Kali!C161 |
| VS Code extension: C/C++ (ms-vscode.cpptools) | (not captured) | VS Code extension (ms-vscode.cpptools) | — | Approved Tool List for Kali!C162 |
| VS Code extension: Python (ms-python.python) | (not captured) | VS Code extension (ms-python.python) | — | Approved Tool List for Kali!C163 |
| YARA | 4.5.8 | — | — | Approved Tool List for Kali!C164 |
| yara-python (and YARA on Linux) | (not captured) | pip (yara-python) | — | Approved Tool List for Kali!C165 |
| zip | (not captured) | — | Installed; version not captured | Approved Tool List for Kali!C166 |
| zstd | 1.5.7 | — | — | Approved Tool List for Kali!C167 |
| Zui (formerly Brim) | (not captured) | — | Version not captured (the command only printed a startup message) | Approved Tool List for Kali!C168 |

## Not approved · 82 entries

| Tool | Version | Installation/location | Notes/reason | Workbook source |
| --- | --- | --- | --- | --- |
| API Monitor | — | — | The challenges can be solved without it. | Unapproved List!B6 |
| Arsenal Image Mounter (Free Mode) | — | — | Alternative tools are available. | Unapproved List!B7 |
| Binary Ninja (Free) | — | — | Cannot be supported in the provided environment. | Unapproved List!B8 |
| BlobRunner (32-bit and 64-bit) | — | — | The challenges can be solved without it. | Unapproved List!B9 |
| Build Tools for Visual Studio 2026 (C++ workload) | — | — | Alternative tools are available. | Unapproved List!B10 |
| capa Explorer Web | — | — | The challenges can be solved without it. | Unapproved List!B11 |
| Cmder | — | — | Alternative tools are available. | Unapproved List!B12 |
| CodeTrack | — | — | The challenges can be solved without it. | Unapproved List!B13 |
| Copy As Python-Requests (Burp Suite extension) | — | — | Cannot be supported in the provided environment. | Unapproved List!B14 |
| CryptoTester | — | — | License or source cannot be verified. | Unapproved List!B15 |
| Cygwin | — | — | Alternative tools are available. | Unapproved List!B16 |
| DCT-Image-Steganography | — | — | Not permitted under the competition rules. | Unapproved List!B17 |
| de4dot (de4dot-cex build) | — | — | Cannot be supported in the provided environment. | Unapproved List!B18 |
| Decompiler.com | — | — | Not permitted under the competition rules. | Unapproved List!B19 |
| Dirsearch | — | — | Cannot be supported in the provided environment. | Unapproved List!B20 |
| Dissect (Fox-IT DFIR framework) | — | — | Cannot be supported in the provided environment. | Unapproved List!B21 |
| dll_to_exe | — | — | The challenges can be solved without it. | Unapproved List!B22 |
| dnlib | — | — | The challenges can be solved without it. | Unapproved List!B23 |
| DotDumper | — | — | The challenges can be solved without it. | Unapproved List!B24 |
| Exeinfo PE | — | — | The challenges can be solved without it. | Unapproved List!B25 |
| FdSig | — | — | License or source cannot be verified. | Unapproved List!B26 |
| Fiddler Classic | — | — | Requires a commercial license. | Unapproved List!B27 |
| GarbageMan and psnotify | — | — | The challenges can be solved without it. | Unapproved List!B28 |
| GoStringUngarbler | — | — | The challenges can be solved without it. | Unapproved List!B29 |
| GraphQL Raider (Burp Suite extension) | — | — | Cannot be supported in the provided environment. | Unapproved List!B30 |
| Hackvertor (Burp Suite extension) | — | — | Cannot be supported in the provided environment. | Unapproved List!B31 |
| HashMyFiles | — | — | The challenges can be solved without it. | Unapproved List!B32 |
| HollowsHunter | — | — | The challenges can be solved without it. | Unapproved List!B33 |
| IDA Free | — | — | Cannot be supported in the provided environment. | Unapproved List!B34 |
| IDR (Interactive Delphi Reconstructor) | — | — | The challenges can be solved without it. | Unapproved List!B35 |
| IFPSTools.NET (ifpsdasm) | — | — | The challenges can be solved without it. | Unapproved List!B36 |
| ImHex | — | — | Cannot be supported in the provided environment. | Unapproved List!B37 |
| Inno Setup Decompiler | — | — | License or source cannot be verified. | Unapproved List!B38 |
| innounp | — | — | The challenges can be solved without it. | Unapproved List!B39 |
| JWT Editor (Burp Suite extension) | — | — | Cannot be supported in the provided environment. | Unapproved List!B40 |
| Kernel OST Viewer (free) | — | — | The challenges can be solved without it. | Unapproved List!B41 |
| magiceye-solver | — | — | Cannot be supported in the provided environment. | Unapproved List!B42 |
| Malcode Analyst Pack (MAP) | — | — | The challenges can be solved without it. | Unapproved List!B43 |
| malware-jail | — | — | The challenges can be solved without it. | Unapproved List!B44 |
| MemProcFS | — | — | Cannot be supported in the provided environment. | Unapproved List!B45 |
| MMSSTV | — | — | Cannot be supported in the provided environment. | Unapproved List!B46 |
| MobSF | — | — | Cannot be supported in the provided environment. | Unapproved List!B47 |
| NETReactorSlayer | — | — | The challenges can be solved without it. | Unapproved List!B48 |
| OffVis | — | — | The challenges can be solved without it. | Unapproved List!B49 |
| OneNoteAnalyzer | — | — | The challenges can be solved without it. | Unapproved List!B50 |
| Online analysis services (VirusTotal, CrackStation, etc.) | — | — | Not permitted under the competition rules. | Unapproved List!B51 |
| Online decompilers and compilers (websites - nothing to install) | — | — | Not permitted under the competition rules. | Unapproved List!B52 |
| PDBReSym | — | — | The challenges can be solved without it. | Unapproved List!B53 |
| PDFStreamDumper | — | — | Alternative tools are available. | Unapproved List!B54 |
| PE-sieve | — | — | The challenges can be solved without it. | Unapproved List!B55 |
| pe_unmapper | — | — | The challenges can be solved without it. | Unapproved List!B56 |
| PEiD | — | — | License or source cannot be verified. | Unapproved List!B57 |
| Photocraft | — | — | License or source cannot be verified. | Unapproved List!B58 |
| pkg-unpacker | — | — | The challenges can be solved without it. | Unapproved List!B59 |
| ProcDOT | — | — | The challenges can be solved without it. | Unapproved List!B60 |
| Process Dump (pd32 / pd64) | — | — | The challenges can be solved without it. | Unapproved List!B61 |
| Process Monitor | — | — | Alternative tools are available. | Unapproved List!B62 |
| PST Walker | — | — | Requires a commercial license. | Unapproved List!B63 |
| pylingual | — | — | Cannot be supported in the provided environment. | Unapproved List!B64 |
| Recaf | — | — | Cannot be supported in the provided environment. | Unapproved List!B65 |
| reg_export | — | — | The challenges can be solved without it. | Unapproved List!B66 |
| Regshot | — | — | The challenges can be solved without it. | Unapproved List!B67 |
| RunDotNetDll | — | — | The challenges can be solved without it. | Unapproved List!B68 |
| RX-SSTV | — | — | Cannot be supported in the provided environment. | Unapproved List!B69 |
| scdbg (with GUI) | — | — | The challenges can be solved without it. | Unapproved List!B70 |
| SCLauncher (32-bit and 64-bit) | — | — | The challenges can be solved without it. | Unapproved List!B71 |
| Scylla / x64dbg plugins | — | — | Alternative tools are available. | Unapproved List!B72 |
| sfextract (SingleFileExtractor) | — | — | The challenges can be solved without it. | Unapproved List!B73 |
| shellcode_launcher | — | — | The challenges can be solved without it. | Unapproved List!B74 |
| sigBits | — | — | Cannot be supported in the provided environment. | Unapproved List!B75 |
| stegdetect | — | — | Cannot be supported in the provided environment. | Unapproved List!B76 |
| SysTools SQLite Viewer (free edition) | — | — | Requires a commercial license. | Unapproved List!B77 |
| Time Travel Debugging (TTD) | — | — | The challenges can be solved without it. | Unapproved List!B78 |
| TweakPNG | — | — | Cannot be supported in the provided environment. | Unapproved List!B79 |
| Universal Extractor 2 (UniExtract2) | — | — | The challenges can be solved without it. | Unapproved List!B80 |
| VBDec | — | — | The challenges can be solved without it. | Unapproved List!B81 |
| Volatility 3 symbol tables (windows/linux/mac zip) | — | — | Cannot be supported in the provided environment. | Unapproved List!B82 |
| VS Code extension: WSL (ms-vscode-remote.remote-wsl) | — | — | The challenges can be solved without it. | Unapproved List!B83 |
| WinDbg | — | — | Alternative tools are available. | Unapproved List!B84 |
| Windows Terminal | — | — | Alternative tools are available. | Unapproved List!B85 |
| WinDump (for Npcap) | — | — | Alternative tools are available. | Unapproved List!B86 |
| YAFU (Yet Another Factoring Utility) | — | — | Cannot be supported in the provided environment. | Unapproved List!B87 |



---

<a id="source-coverage"></a>

# Source coverage and editorial decisions

The original snapshot contains **286 files**, including **197 Markdown files**. Every file is listed below. Category guides were reviewed for human adaptation; infrastructure received inventory/structural review. This is not a claim that every historical exploit was executed or every source sentence was reproduced.

**Adapted/merged** means useful content was rewritten or consolidated. **Reference-only** retains specialist/history or development context without presenting it as a ready event recipe. **Excluded** explains material incompatible with the event or human workflow. The chapter is the destination or nearest explanation. Review details and original SHA-256 hashes are in `review/combined-coverage.json`.

| Original source | Disposition | Human destination | Review note |
| --- | --- | --- | --- |
| .github/codeql/codeql-config.yml | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| .github/dependabot.yml | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| .github/ISSUE_TEMPLATE/bug-report.yml | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| .github/ISSUE_TEMPLATE/config.yml | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| .github/ISSUE_TEMPLATE/coverage-gap.yml | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| .github/ISSUE_TEMPLATE/new-technique.yml | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| .github/labeler.yml | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| .github/pull_request_template.md | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| .github/workflows/labeler.yml | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| .github/workflows/link-checker.yml | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| .github/workflows/lint-scripts.yml | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| .github/workflows/markdown-lint.yml | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| .github/workflows/pages.yml | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| .github/workflows/skill-evals.yml | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| .github/workflows/skill-security-audit-comment.yml | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| .github/workflows/skill-security-audit.yml | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| .github/workflows/tests.yml | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| .gitignore | reference-only | chapters/01-first-ten-minutes.md | Repository governance, configuration or contribution material; retained in original tree, not a challenge-solving recipe. |
| .lychee.toml | reference-only | chapters/01-first-ten-minutes.md | Repository governance, configuration or contribution material; retained in original tree, not a challenge-solving recipe. |
| .markdownlint-cli2.yaml | reference-only | chapters/01-first-ten-minutes.md | Repository governance, configuration or contribution material; retained in original tree, not a challenge-solving recipe. |
| .opencode/agents/ctf-crypto.md | excluded | chapters/01-first-ten-minutes.md | Agent role/configuration instructions; category expertise is represented by the human chapters. No competition workflow depends on an agent. |
| .opencode/agents/ctf-forensics.md | excluded | chapters/01-first-ten-minutes.md | Agent role/configuration instructions; category expertise is represented by the human chapters. No competition workflow depends on an agent. |
| .opencode/agents/ctf-leader.md | excluded | chapters/01-first-ten-minutes.md | Agent role/configuration instructions; category expertise is represented by the human chapters. No competition workflow depends on an agent. |
| .opencode/agents/ctf-malware.md | excluded | chapters/01-first-ten-minutes.md | Agent role/configuration instructions; category expertise is represented by the human chapters. No competition workflow depends on an agent. |
| .opencode/agents/ctf-misc.md | excluded | chapters/01-first-ten-minutes.md | Agent role/configuration instructions; category expertise is represented by the human chapters. No competition workflow depends on an agent. |
| .opencode/agents/ctf-osint.md | excluded | chapters/01-first-ten-minutes.md | Agent role/configuration instructions; category expertise is represented by the human chapters. No competition workflow depends on an agent. |
| .opencode/agents/ctf-pwn.md | excluded | chapters/01-first-ten-minutes.md | Agent role/configuration instructions; category expertise is represented by the human chapters. No competition workflow depends on an agent. |
| .opencode/agents/ctf-reverse.md | excluded | chapters/01-first-ten-minutes.md | Agent role/configuration instructions; category expertise is represented by the human chapters. No competition workflow depends on an agent. |
| .opencode/agents/ctf-web.md | excluded | chapters/01-first-ten-minutes.md | Agent role/configuration instructions; category expertise is represented by the human chapters. No competition workflow depends on an agent. |
| .opencode/opencode.json | excluded | chapters/01-first-ten-minutes.md | Agent role/configuration instructions; category expertise is represented by the human chapters. No competition workflow depends on an agent. |
| .pre-commit-config.yaml | reference-only | chapters/01-first-ten-minutes.md | Repository governance, configuration or contribution material; retained in original tree, not a challenge-solving recipe. |
| AJCCBC_CTF2026_Tool_Review_List_261015r11.xlsx | adapted | TOOL-MATRIX.md | All three sheets and 282 tool rows extracted with cell provenance and full remarks. |
| CODE_OF_CONDUCT.md | reference-only | chapters/01-first-ten-minutes.md | Repository governance, configuration or contribution material; retained in original tree, not a challenge-solving recipe. |
| CONTRIBUTING.md | reference-only | chapters/01-first-ten-minutes.md | Repository governance, configuration or contribution material; retained in original tree, not a challenge-solving recipe. |
| ctf-ai-ml/adversarial-ml.md | excluded | chapters/12-excluded-and-advanced.md | Excluded gradient attacks, patches, evasion, poisoning/backdoor and Keras/foolbox workflows under AI-tool restriction; no runnable framework recipes. |
| ctf-ai-ml/llm-attacks.md | excluded | chapters/12-excluded-and-advanced.md | Excluded prompt injection, jailbreaks, context/token manipulation and AI tool-use exploitation; conventional web/auth analysis remains manual. |
| ctf-ai-ml/model-attacks.md | excluded | chapters/12-excluded-and-advanced.md | Excluded model/weight inversion, LoRA, extraction and membership inference; ordinary embedded artifacts may be inspected without loading a model. |
| ctf-ai-ml/SKILL.md | excluded | chapters/12-excluded-and-advanced.md | Excluded AI/ML framework installation, model inference and AI-service interaction; approved local metadata/ordinary parser alternatives explained. |
| ctf-crypto/advanced-math.md | merged | chapters/14-advanced-crypto.md | Small roots, GF(2) equations, DLP, Hensel/polynomial CRT, group mappings and unusual totients; tested local linear algebra/BSGS and optional Sage environment toy. |
| ctf-crypto/classic-ciphers.md | merged | chapters/07-cryptography.md | Substitution/Vigenere/book/symbol recognition, aligned known-plaintext XOR and reused streams; image/grid/error-correcting variants cross-referenced. |
| ctf-crypto/dh-attacks.md | merged | chapters/07-cryptography.md | Trivial generators, group-order smoothness, persistent-key subgroup conditions and exact shared-secret toy. |
| ctf-crypto/ecc-attacks.md | merged | chapters/14-advanced-crypto.md | Curve/order/validation map, singular/anomalous/MOV/twist/invalid-point/fault families, Ed25519/X25519 constraints and verified nonce-reuse arithmetic. |
| ctf-crypto/exotic-crypto-2.md | merged | chapters/14-advanced-crypto.md | ElGamal/matrix, homomorphic predicates, noise, mnemonic checksum, CRT sharing and Rabin four-root demonstration; no public wallet services. |
| ctf-crypto/exotic-crypto.md | merged | chapters/14-advanced-crypto.md | Operation-preserving reduction diagnostics for Paillier, tropical, braid, permutation, monotone and reduced-round designs; historical media/error-correction context. |
| ctf-crypto/historical.md | merged | chapters/14-advanced-crypto.md | Lorenz wheel/alphabet/stepping and exact-edition book-cipher prerequisites retained in advanced section 17 and core classic section. |
| ctf-crypto/lattice-and-lwe.md | merged | chapters/14-advanced-crypto.md | HNP/truncated-LCG/LWE/approximate-GCD/subset-sum/GGH/NTRU/orthogonal/BDD model table, bounds and extraction verification; optional local dependencies. |
| ctf-crypto/modern-ciphers-2.md | merged | chapters/07-cryptography.md | Length-extension versus HMAC, compression/stream/ECB/CBC concepts, weak key derivation and old collision claims contextualized. |
| ctf-crypto/modern-ciphers-3.md | merged | chapters/07-cryptography.md | Error/timing predicates, custom linear/aggregate hashes, CRC and SPN modelling; chosen-input and noise constraints retained. |
| ctf-crypto/modern-ciphers-4.md | merged | chapters/14-advanced-crypto.md | GCM/Poly1305 field distinctions, partitioning/key-commitment requirements, sponge parameters and reduced-round eSTREAM limitations. |
| ctf-crypto/modern-ciphers.md | merged | chapters/07-cryptography.md | Mode identification, CBC bit flips and oracle simulation, ECB suffix toy, hashes/MACs, GCM, reduced-round and RSA-oracle prerequisites. |
| ctf-crypto/post-quantum.md | merged | chapters/14-advanced-crypto.md | ML-KEM/ML-DSA parameter recognition, exact implementation weakness, flattening/estimator limitations; no promise to solve secure parameters. |
| ctf-crypto/prng-attacks.md | merged | chapters/07-cryptography.md | Partial/modulo output constraints, hidden draws, backward stepping, state/correlation/oracle distinctions; no generic seed-tool assumption. |
| ctf-crypto/prng.md | merged | chapters/07-cryptography.md | Exact runtime/output modelling; LCG recovery and backward stepping toy, MT float limitations, time seeds, PCG/xoshiro/chaotic map recognition. |
| ctf-crypto/rsa-attacks-2.md | merged | chapters/07-cryptography.md | Shared/biased/repeated factors, nonunique roots, faults, hidden modulus, homomorphism, CRT and oracle details merged; candidate verification emphasized. |
| ctf-crypto/rsa-attacks.md | merged | chapters/07-cryptography.md | Low exponent, common modulus, Wiener, factoring, broadcast, partial roots and oracle distinctions; core and advanced tested local arithmetic. |
| ctf-crypto/SKILL.md | adapted | chapters/07-cryptography.md | Overview and duplicate recipes merged into exact arithmetic, byte handling, hypothesis map and verifiable toy solvers; online factoring/installers excluded. |
| ctf-crypto/stream-ciphers.md | merged | chapters/07-cryptography.md | Reused streams, tested LFSR Berlekamp-Massey, filtered/combined register caveats and RC4/eSTREAM recognition. |
| ctf-crypto/zkp-and-advanced.md | merged | chapters/14-advanced-crypto.md | Transcripts/public inputs, Groth16/nullifier/KZG/DV-SNARG/free-XOR/FROST constraints and tested Shamir interpolation; corrected misleading FROST lattice classification. |
| ctf-forensics/3d-printing.md | adapted | chapters/05-steganography.md | GCDE/QOI identification, compression/version constraints, thumbnail examination and a complete modal absolute G-code XZ SVG renderer retained. Corrected assumption that every block always has a CRC32 and that decompression alone always yields ordinary text. Relative/arc modes explicitly unsupported by the compact renderer. |
| ctf-forensics/disk-advanced.md | adapted | chapters/03-forensics.md | Advanced cases retained as targeted extraction and validation workflows: sparse VMDK, GPT GUIDs, snapshots, RAID parity, HFS resource forks, SQLite history, memory keys and legacy macro arithmetic. Fixed Fletcher4 width, RAID member-vs-array distinction, APFS signature overclaim, and unreliable Kyoto Cabinet first-diff assumption. |
| ctf-forensics/disk-and-memory.md | adapted | chapters/03-forensics.md | Disk/memory, VM chains, triage artifacts, cores, Android, containers, BSON, ransomware and framebuffers retained. Snapshot conversion and encrypted-volume tools are availability-limited; live cloud enumeration and unsupported collision generation excluded. Volatility symbols explicitly uncertain; offline mode used. |
| ctf-forensics/disk-recovery.md | adapted | chapters/03-forensics.md | Recovery, tar duplicate members, nested archives, null interleaving, XZ/ZIP repairs and bkcrack retained with copy-only commands and bounded extraction. FAT chain preservation and fsck recovery overclaims corrected. Missing encrypted-volume, FemtoZip, XFS/Btrfs drivers are not silently installed. DNSSEC key forging omitted; local Git key-history recovery retained. |
| ctf-forensics/linux-forensics.md | merged | chapters/03-forensics.md | Linux logs, browser databases, Git corruption/history, Android/app data and Docker history consolidated into 03. Network TLS/TFTP/USB topics moved to 04; macro extraction in 09. Live pyrasite injection, arbitrary cloud/blockchain API use, and unapproved credential tools excluded. Browser key/version limitations made explicit. |
| ctf-forensics/network-advanced.md | adapted | chapters/04-network.md | Timing, flags, DNS/ICMP channels, NTLM/SMB, SNTP, RADIUS, dnscat-like framing, checksums and Brotli limits retained. Fixed naive TCP concatenation, universal dnscat header length and midstream decompression claims. PDF hidden-page/xref material merged into 05. Active roasting requests omitted; capture parsing remains offline. |
| ctf-forensics/network.md | adapted | chapters/04-network.md | Offline triage, HTTP/SMTP extraction, TLS/RDP, split archives, Wi-Fi and unusual protocols retained. Removed live capture/scanning defaults, vendor API lookup, DNS oracle probing, pcapfix installer, unsupported SAP tooling and Plover setup. TLS structure and SMB KDF assumptions explicitly corrected. |
| ctf-forensics/peripheral-capture.md | adapted | chapters/04-network.md | USB keyboard state decoder, mouse/pen, LED Morse, cursor/chords, RFCOMM and framebuffer workflows retained. Corrected fixed packet offsets/header sizes, keyboard held-key duplication, and universal GBA RGB565 assumption. Report descriptor and endpoint isolation are required. |
| ctf-forensics/signals-and-hardware.md | merged | chapters/04-network.md | UART complete CSV decoder, I2C/SPI edge workflow, VGA/TMDS/DisplayPort constraints and peripheral input retained in 04; analog images, RF pulses, punched cards, CDDA, power traces and manual acoustic inspection in 05. Corrected TMDS inverse recurrence and UART framing/sample-width assumptions. Learned acoustic classifier excluded by AI/ML rule; unsupported signal GUI installers excluded. |
| ctf-forensics/SKILL.md | merged | chapters/03-forensics.md | Read in full. Index and quick starts redistributed across chapters 03, 04, and 05. Removed agent routing, blanket installers, public services, unsupported tools, and acoustic ML. Corrected overclaims about filesystem, timestamps, and protocol reconstruction. |
| ctf-forensics/steganography.md | adapted | chapters/05-steganography.md | PNG parser/height repair, border bits, PDF/SVG, terminal/text, interleaving, QR, frames/tracks and archive layers retained. Removed public SpamMimic decoding, unapproved editors and tools. Corrected PNG chunk-order generalization, raw IEND substring carving and QR error-correction overclaims. |
| ctf-forensics/stego-advanced-2.md | adapted | chapters/05-steganography.md | Frame accumulation/averaging, reversals, cat map, FM diagnostic, MJPEG/EXIF/PDF/ANSI and colored QR workflows retained. JPEG XL route is approval/build dependent; no djxl installation assumed. Corrected arccos FM approach and generic sample-rate diagnosis. Pixel ECB discussion folded into structure-leak reasoning rather than copied incomplete pseudocode. |
| ctf-forensics/stego-advanced.md | adapted | chapters/05-steganography.md | Audio spectrograms, DTMF/custom tones, notes, channel subtraction, sample LSBs, text and animation topics consolidated. SSTV workbook PySSTV mismatch explicitly flagged. DeepSound extraction availability bounded; online DotCode service and blanket installers excluded. Exact sample preservation and ambiguity checks added. |
| ctf-forensics/stego-image.md | adapted | chapters/05-steganography.md | Bitplanes, DQT/palettes, pixel chains, conditional carriers, permutations, thumbnails, JPEG slack, parity, QR geometry and puzzle methods retained. Corrected unsupported F5 universal thresholds, JPEG resize-as-uncrop, palette survival claims and infeasible 4x4 exhaustive permutations. Unapproved/learned puzzle tools excluded. |
| ctf-forensics/windows.md | adapted | chapters/03-forensics.md | EVTX, hives, ADS, MFT, USN, Recycle Bin, history, Defender, WMI and legacy memory workflows retained. Corrected USN path, exact-command-timestamp assertion, Amcache execution assertion, MFT creator-process claim, and wipe-completion inference. Uses native PowerShell and approved Zimmerman tools. |
| ctf-malware/c2-and-protocols.md | adapted | chapters/09-malware.md | Offline C2 framing, RC4/AES, rotation, crypto identification and RAT artifact reasoning retained. Telegram API retrieval, ARP spoofing/RST injection and Dissect parser excluded. Invented PyCryptodome Camellia import corrected; protocol state and WebSocket layers separated. |
| ctf-malware/pe-and-dotnet.md | adapted | chapters/09-malware.md | PE/resources, dnSpyEx, configuration derivation and Python bundle extraction retained with approved alternatives. Family-specific LimeRAT derivation marked sample-dependent. Unlisted PE analysis tools, AsmResolver dependency and PyArmor unpacker are not assumed approved. |
| ctf-malware/scripts-and-obfuscation.md | adapted | chapters/09-malware.md | Literal decoding, package/macro inspection, YARA, shellcode, memory, API hashing and plugin diff workflows retained. Executing scripts with eval replaced by print is rejected as insufficient. Dynamic tracing clearly requires separate isolated authorized runtime. Useless broad YARA and unapproved shellcode launcher instructions removed. |
| ctf-malware/SKILL.md | merged | chapters/09-malware.md | Human static-first workflow, environment tool map and pivots replace agent skill frontmatter and tool invocation. Removed installer bundles, agent automation and unapproved tooling. Corrected universal shared-keystream/two-direction advice. |
| ctf-malware/tools-mcp.md | merged | chapters/09-malware.md | Read in full. Manual Ghidra xrefs/config analysis, debugger buffer handoff and JADX code-scope search translated to human workflows. All MCP/agent calls, setup, unsupported WinDbg and autonomous dynamic loops excluded. |
| ctf-misc/audio.md | merged | chapters/11-miscellaneous.md | Channel/format-first workflow, Kali spectrogram commands, WAV metadata and tested RMS Morse-run extractor; SSTV package capability caveat. |
| ctf-misc/bashjails.md | merged | chapters/11-miscellaneous.md | Input/eval/shell distinction, octal quoting and built-in challenge file read; startup/environment changes confined to explicit challenge. |
| ctf-misc/ctfd-navigation.md | adapted | chapters/11-miscellaneous.md | Manual organizer portal workflow; documented competitor API only, tokens kept private and point-cost hints respected; no hidden challenge enumeration. |
| ctf-misc/dns.md | merged | chapters/11-miscellaneous.md | Assigned-resolver/capture-only DNS, NSEC/IXFR/ECS/round-robin/rebinding/tunnel reconstruction diagnostics; no public exfiltration. |
| ctf-misc/encodings-advanced.md | merged | chapters/11-miscellaneous.md | Gray/BCD/grid/polyglot/RTF/SMS/HDL/visual alphabet diagnostics; original unsafe execution and unsupported decoder assumptions removed. |
| ctf-misc/encodings.md | merged | chapters/11-miscellaneous.md | Strict layered decoding, UTF-16/BCD/float/code-point distinctions, QR rendering and esolang constraints; runnable local examples. |
| ctf-misc/games-and-vms-2.md | merged | chapters/11-miscellaneous.md | Cookies/WebSocket/time-only server validation and WASM authority, De Bruijn cyclic convention and instrumented interpreter prerequisites. |
| ctf-misc/games-and-vms-3.md | merged | chapters/11-miscellaneous.md | Stateful protocol phases, emulator/reverse routing, constraint/maze/puzzle models and explicit container scope; unportable seccomp/editor variants contextualized. |
| ctf-misc/games-and-vms-4.md | merged | chapters/11-miscellaneous.md | Local recurrence modelling, precision demo and esolang/QR structure; online sequence lookup excluded and unlisted OCR/browser automation not assumed. |
| ctf-misc/games-and-vms.md | merged | chapters/11-miscellaneous.md | Authoritative state, bytecode/container routing, constraints and floating-point semantics; BFS and enumeration toys; explicit challenge scope. |
| ctf-misc/linux-privesc.md | merged | chapters/11-miscellaneous.md | Challenge-only identity/sudo/service/path/permissions checks and version-specific primitives; no organizer host takeover/persistence workflows. |
| ctf-misc/pyjails.md | merged | chapters/11-miscellaneous.md | Evaluator/filter/AST/version checks, complete object-reference escape toy and advanced syntax limits; invalid eval assignment and nonportable runtime offsets corrected. |
| ctf-misc/rf-sdr.md | merged | chapters/11-miscellaneous.md | IQ format/sample-rate/bandwidth/symbol/framing model, float32 fixture reader, carrier/timing caveats; no unapproved SDR suite assumed. |
| ctf-misc/SKILL.md | adapted | chapters/11-miscellaneous.md | Overview and duplicate encoding/media/jail/service recipes merged into category-aware bounded manual workflow. |
| ctf-osint/geolocation-and-media.md | adapted | chapters/10-osint.md | Local metadata/crops/mirroring, observation sheets, multi-feature verification, camera viewpoint, coordinate systems, spatial CSV ranking, supplied OSM data, product/newspaper and themed landmarks retained. Public reverse-image uploads, face search and API-key map services excluded. Overconfident country/sign and IP-geolocation claims corrected. |
| ctf-osint/SKILL.md | merged | chapters/10-osint.md | Local evidence-first OSINT decision workflow replaces agent index, installs and online service list. Metadata, stable IDs, coordinate precision and corroboration retained; public image uploads, face recognition and unapproved services removed. |
| ctf-osint/social-media.md | adapted | chapters/10-osint.md | Supplied exports, alias/ID correlation, Snowflake timestamp, homoglyphs, local playlist/gaming/emoji clues and platform false positives retained. No credentialed Discord enumeration, paid people search, live account APIs or invasive privacy-zone inference. Same-name and metadata-stripping overclaims corrected. |
| ctf-osint/tools-mcp.md | merged | chapters/10-osint.md | Read in full. Saved-page links, application JSON and source-vs-rendered distinctions adapted to human offline HTML parser. MCP setup/calls and automated public upload/search flows excluded; no agent workflow retained. |
| ctf-osint/web-and-dns.md | adapted | chapters/10-osint.md | Saved HTML/JSON, DNS/registration/archive exports, Git history, DS_Store and font-shape methods retained as local workflows. External paid APIs, bot interaction, cross-challenge pivots and broad active scanning excluded. Corrected claim that all Git history is signed and shared keys/IPs prove identity. |
| ctf-pwn/advanced-exploits-2.md | merged | chapters/08-binary-exploitation.md | Merged validator/execution differential, GC lifetime, truncation, FILE/TLS and pointer-mangling prerequisites into sections 9-12. Full exploit chains not reproduced. |
| ctf-pwn/advanced-exploits-3.md | merged | chapters/08-binary-exploitation.md | Merged stack/state overlap, parser/stride/sign issues, inherited descriptors and read-only-primitive reasoning into sections 7 and 12. Named challenges and exact payloads remain reference material. |
| ctf-pwn/advanced-exploits-4.md | merged | chapters/08-binary-exploitation.md | Merged Windows ABI/SEH/CFG limitations, ARM conventions, bit/byte filters, object lifetime and dispatch-index reasoning into sections 6, 11-13. AI/ML training example excluded; escalation procedures reference-only. |
| ctf-pwn/advanced-exploits-5.md | merged | chapters/08-binary-exploitation.md | Merged emulator OOB, floating-point sorting and abs(INT_MIN) data-interpretation pitfalls into section 12. No exact exploit claimed. |
| ctf-pwn/advanced-exploits.md | merged | chapters/08-binary-exploitation.md | Merged parser lengths, VM/JIT, type confusion, integer widths, state/canary and ORW prerequisites into sections 11-12. Historical architecture-specific and ASAN details remain reference-only. |
| ctf-pwn/advanced.md | merged | chapters/08-binary-exploitation.md | Merged UAF/JIT, data interpretation, missing register control and linker-resolution prerequisites into sections 7 and 12. Exact timing/Windows/static-address tricks reference-only. |
| ctf-pwn/attack-playbook.md | adapted | chapters/08-binary-exploitation.md | Adapted primitive-first reconnaissance, leak selection and target choice into sections 2, 7 and 9-10. Runtime conditions are explicit. |
| ctf-pwn/field-notes.md | merged | chapters/08-binary-exploitation.md | Deduplicated heap/ROP/FILE/kernel quick-reference material across sections 7-13; original case payloads remain historical reference. |
| ctf-pwn/format-string.md | adapted | chapters/08-binary-exploitation.md | Adapted sink confirmation, pointer leaks, count arithmetic, transformed input and write-target prerequisites into section 8. Historical positional offsets and format-string payloads remain reference material. |
| ctf-pwn/heap-fsop.md | merged | chapters/08-binary-exploitation.md | Merged stdin/stdout fields, vtable validation, zero-size realloc and lifetime counters into sections 9-10. No universal FILE layout or successful modern bypass asserted. |
| ctf-pwn/heap-techniques-2.md | merged | chapters/08-binary-exploitation.md | Merged stale residue, pointer fields, cross-bin/partial corruption, custom allocators and size bookkeeping into sections 9-10 and case atlas. Individual historical allocation sequences reference-only. |
| ctf-pwn/heap-techniques.md | merged | chapters/08-binary-exploitation.md | Merged allocator/version prerequisites and named heap families into sections 9-10, with safe-linking toy and hook-removal correction. Exact modern/old allocator chains not validated. |
| ctf-pwn/kernel-bypass.md | merged | chapters/08-binary-exploitation.md | Merged mitigation distinctions and exact-build requirements into section 13. Source generic CET signal-frame bypass claim not certified; no QEMU installation or host-kernel exploit prescribed. |
| ctf-pwn/kernel-techniques.md | merged | chapters/08-binary-exploitation.md | Merged SLUB/cache/race/PTE and error-path prerequisites into section 13. Exact sprays, structure sizes, race success and historic addr_limit behavior not asserted portable. |
| ctf-pwn/kernel.md | merged | chapters/08-binary-exploitation.md | Merged supplied-artifact prerequisites, driver handler review, object lifetime and kernel target assumptions into section 13. Exact kernel/CVE/hypervisor exploit code retained as unvalidated source reference. |
| ctf-pwn/overflow-basics.md | adapted | chapters/08-binary-exploitation.md | Adapted offset measurement, pointer packing, canary/field constraints and parser/index errors into sections 4-6 and 12. Added working stdlib pattern/builder; historical exploit offsets unverified. |
| ctf-pwn/pwnable-tw/3x17.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. |
| ctf-pwn/pwnable-tw/alive_note.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. |
| ctf-pwn/pwnable-tw/applestore.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. |
| ctf-pwn/pwnable-tw/babyallocator.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. |
| ctf-pwn/pwnable-tw/babystack.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. |
| ctf-pwn/pwnable-tw/bash.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. |
| ctf-pwn/pwnable-tw/bash_revenge.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. |
| ctf-pwn/pwnable-tw/bookwriter.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. |
| ctf-pwn/pwnable-tw/bounty_program_a.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. |
| ctf-pwn/pwnable-tw/bounty_program_b.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. |
| ctf-pwn/pwnable-tw/break_out.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. |
| ctf-pwn/pwnable-tw/calc.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. |
| ctf-pwn/pwnable-tw/caov.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. |
| ctf-pwn/pwnable-tw/criticalheap.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. |
| ctf-pwn/pwnable-tw/criticalheap_pp.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. Distinguishes measured realpath output overflow from index broad C++ lifetime explanation. |
| ctf-pwn/pwnable-tw/de_aslr.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. Directory-index writable-GOT/resolver shorthand conflicts with protection constraints; detailed pointer-manipulation route prioritized. |
| ctf-pwn/pwnable-tw/death_note.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. |
| ctf-pwn/pwnable-tw/digimon.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. Prioritizes parser index corruption and explicit negative findings over index race-UAF narrative. |
| ctf-pwn/pwnable-tw/dubblesort.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. |
| ctf-pwn/pwnable-tw/food_store.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. Index generic heap-overflow summary differs from detailed uninitialized-next-pointer mechanism. |
| ctf-pwn/pwnable-tw/ghost_party.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. |
| ctf-pwn/pwnable-tw/hacknote.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. |
| ctf-pwn/pwnable-tw/heap_paradise.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. |
| ctf-pwn/pwnable-tw/hitcon_ftp.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. Distinguishes detailed option type confusion and stack formatting overflow from index heap-corruption wording. |
| ctf-pwn/pwnable-tw/kidding.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. |
| ctf-pwn/pwnable-tw/mno2.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. |
| ctf-pwn/pwnable-tw/omegago.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. Prioritizes history-array overflow and board representation over index coordinate-to-GOT narrative. |
| ctf-pwn/pwnable-tw/orw.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. |
| ctf-pwn/pwnable-tw/printable.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. |
| ctf-pwn/pwnable-tw/re_alloc.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. Source overview and NULL-pointer subsection contradict; atlas requires binary confirmation before accepting UAF. |
| ctf-pwn/pwnable-tw/re_alloc_revenge.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. |
| ctf-pwn/pwnable-tw/README.md | reference-only | chapters/13-pwn-practice-atlas.md | Full-file structural catalog review with semantic comparison of conflicting summaries to individual cases. Historical index retained as provenance; atlas replaces it with 43 human case lessons and flags contradictions. No historical exploit verified. |
| ctf-pwn/pwnable-tw/seccomptools.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. Prioritizes detailed BPF emulator/kernel differential over index generic hook narrative. |
| ctf-pwn/pwnable-tw/secret_garden.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. |
| ctf-pwn/pwnable-tw/secret_of_my_heart.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. |
| ctf-pwn/pwnable-tw/seethefile.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. |
| ctf-pwn/pwnable-tw/silver_bullet.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. |
| ctf-pwn/pwnable-tw/spirited_away.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. |
| ctf-pwn/pwnable-tw/starbound.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. |
| ctf-pwn/pwnable-tw/start.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. |
| ctf-pwn/pwnable-tw/stupid_boss.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. Prioritizes concrete language-object layout confusion over index employee-UAF narrative. |
| ctf-pwn/pwnable-tw/tcache_tear.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. Unsupported small-malloc/read overflow assertion explicitly rejected; core dangling-pointer route retained as hypothesis. |
| ctf-pwn/pwnable-tw/unexploitable.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. |
| ctf-pwn/pwnable-tw/wannaheap.md | adapted | chapters/13-pwn-practice-atlas.md | Individual case has prerequisites, concrete mechanism, investigation sequence, checkpoint and source path in atlas. Semantic review of vulnerability/primitive sections; full exploit payloads and original binaries not validated. |
| ctf-pwn/rop-advanced.md | merged | chapters/08-binary-exploitation.md | Merged SROP, partial pointer redirection, vDSO, finalizers and dynamic resolution into section 7 and seccomp distinctions into section 11. Exact chains/reference payloads not reproduced. |
| ctf-pwn/rop-and-shellcode.md | merged | chapters/08-binary-exploitation.md | Merged two-stage leaks, ABI, gadget clobbers, stack pivots and constrained staging into sections 6-7 and 11. Removed claims of universal csu gadgets and fixed post-call register values. |
| ctf-pwn/sandbox-escape.md | merged | chapters/08-binary-exploitation.md | Merged guest/host boundaries, interpreter errors and descriptor state into section 12; shell-specific cases preserved in atlas. FUSE/CUSE and unapproved host escape setup not provided. |
| ctf-pwn/scripts/fmtstr_payload_suite.py | reference-only | chapters/08-binary-exploitation.md | Fully read source template; reference-only with section 14 defect review: offset/protocol assumptions, fallback address, adjacent GOT destination and write-width semantics require target proof. |
| ctf-pwn/scripts/ret2libc_two_stage.py | reference-only | chapters/08-binary-exploitation.md | Fully read source template; reference-only with section 14 defect review: fixed gadgets/offsets, binary leak strip, failed-process reuse, prompt and reentry assumptions. Replaced concepts with stdlib builders. |
| ctf-pwn/scripts/seccomp_orw_generator.py | reference-only | chapters/08-binary-exploitation.md | Fully read source template; reference-only with section 14 defect review: misleading x32 label, hardcoded scratch memory/counts and invalid seccomp safety assertion. No execution. |
| ctf-pwn/scripts/shellcraft_asm.py | reference-only | chapters/08-binary-exploitation.md | Fully read source template; reference-only with section 14 defect review: literal wildcard path, unproven control transfer, read stub lacking transfer and fixed descriptors. No execution. |
| ctf-pwn/scripts/srop_execve.py | reference-only | chapters/08-binary-exploitation.md | Fully read source template; reference-only with section 14 defect review: arb_read_gen actually emits execve frames, string placement unproven, frame/trigger/address assumptions. No execution. |
| ctf-pwn/SKILL.md | adapted | chapters/08-binary-exploitation.md | Rebuilt agent exploit recipes as evidence-first human workflow, approved tool routes and lower-priority advanced material. No universal offsets, remote defaults, blanket installers or AI tools retained. |
| ctf-pwn/static-signals.md | adapted | chapters/08-binary-exploitation.md | Adapted evidence-versus-proof mitigation table into section 2; absence of symbols is not treated as absence of protection. |
| ctf-pwn/tools-mcp.md | excluded | chapters/08-binary-exploitation.md | Agent/MCP integration, AI workflows and unapproved tools excluded under event rules. Structural/section review only; generic local debugging/decompilation concepts rewritten using approved tools elsewhere. Original retained as provenance. |
| ctf-reverse/anti-analysis-ctf.md | merged | chapters/06-reverse-engineering.md | Merged signal handlers, parent/child patching, instruction inversion and runtime module reasoning into sections 8-9 and language routes. Specialized historical code remains reference material; de4dot instructions excluded. |
| ctf-reverse/anti-analysis.md | merged | chapters/06-reverse-engineering.md | Merged debugger checks, signals, TLS, integrity and hidden flow into section 9; hardware-breakpoint invisibility and universal bypass claims not retained. Section-level semantic review, no bypass executed. |
| ctf-reverse/field-notes.md | merged | chapters/06-reverse-engineering.md | Deduplicated format/platform/pattern index into sections 12-13. Selected semantic lessons retained, historical commands and payloads not individually reproduced. |
| ctf-reverse/languages-compiled.md | merged | chapters/06-reverse-engineering.md | Merged Go/Rust/Swift/Kotlin/C++ runtime and layout clues into sections 5, 12 and 13. C2 enumeration and unsupported runtimes retained only as source provenance; no external contact. |
| ctf-reverse/languages-platforms.md | merged | chapters/06-reverse-engineering.md | Merged APK/JNI, Electron, game resources, state machines, EBCDIC and bytecode routes into sections 12-13. Platform-specific injection, cloud and device workflows are not event procedures. |
| ctf-reverse/languages.md | merged | chapters/06-reverse-engineering.md | Merged bytecode versioning, DOS stubs, managed/native formats and esolang state recovery into sections 2, 12-13. Specialized unpackers and unavailable engines are conditional/reference-only. |
| ctf-reverse/mba-simplification.md | adapted | chapters/06-reverse-engineering.md | Adapted width-aware MBA reasoning and equivalence checking into a complete exhaustive 8-bit stdlib example. msynth/Miasm setup and synthesis internals remain specialized reference material. |
| ctf-reverse/patterns-ctf-2.md | merged | chapters/06-reverse-engineering.md | Merged staged decryptors, ZIP/license layers, prefix hashes, decision trees, lattices, GF(2^8), and ROPfuscation into section 13. Exact challenge constants and exploit snippets not validated. |
| ctf-reverse/patterns-ctf-3.md | merged | chapters/06-reverse-engineering.md | Merged popcount, hardware output, hidden handlers, BWT, shader/VM state, counters, date keys, CRT and unusual ROM representations into section 13. ML inversion excluded under event policy; case payloads reference-only. |
| ctf-reverse/patterns-ctf.md | merged | chapters/06-reverse-engineering.md | Merged SPN/image/loader/VM/game/maze/embedded-format/library-diff patterns into sections 10 and 13. Historical examples guide recognition only; arbitrary service enumeration excluded. |
| ctf-reverse/patterns-runtime.md | merged | chapters/06-reverse-engineering.md | Merged timing, signal-mediated mutation, staged loaders, decoys and quadtree decoding into sections 8-10 and 13. Full original oracle implementations not validated. |
| ctf-reverse/patterns.md | merged | chapters/06-reverse-engineering.md | Merged VM, transform direction, width, nanomite/signal and self-modification reasoning into sections 8-10. Replaced undefined example constants with complete toy exercises. |
| ctf-reverse/platforms-hardware.md | merged | chapters/06-reverse-engineering.md | Merged architecture modes, GPIO/LCD, peripheral crypto, bootloaders and guest-dispatch observations into sections 10 and 13. Real-device/QEMU workflows are reference-only without an approved supplied lab. |
| ctf-reverse/platforms.md | merged | chapters/06-reverse-engineering.md | Merged firmware, drivers, engines, certificate-derived keys and foreign-platform limitations into sections 12-13. macOS/iOS and emulator dependencies not asserted present. |
| ctf-reverse/radare2-r2pipe.md | adapted | chapters/06-reverse-engineering.md | Adapted static session, xrefs, function disassembly, batch JSON and plugin boundaries into section 4. ESIL/r2pipe retained as conditional follow-up, with no plugin installation. |
| ctf-reverse/SKILL.md | adapted | chapters/06-reverse-engineering.md | Rebuilt agent triage as a human workflow; blanket installation, agent routing, online analysis and unsupported tool assumptions removed. Core text reviewed; individual historical payloads are not validated. |
| ctf-reverse/tools-advanced-2.md | merged | chapters/06-reverse-engineering.md | Merged watchpoints, measured-address breakpoints, extraction, patch/dump and constraint reasoning into sections 5-9. Binary Ninja and unlisted tooling excluded; exact historical scripts reference-only. |
| ctf-reverse/tools-advanced.md | merged | chapters/06-reverse-engineering.md | Merged deobfuscation, diffing, VM lifting/model choice into sections 5, 10 and 13. Unapproved or unlisted standalone tools are not a competition workflow. |
| ctf-reverse/tools-dynamic.md | adapted | chapters/06-reverse-engineering.md | Adapted GDB/x64dbg and observation-only current Frida API into sections 6-7; bounded angr toy in section 11. LLDB/device requirements not asserted available. |
| ctf-reverse/tools-emulation.md | merged | chapters/06-reverse-engineering.md | Merged emulator-state, runtime-model and side-channel prerequisites into sections 8-10. Qiling/Triton/Pin setup and historical oracle payloads remain conditional source reference. |
| ctf-reverse/tools-mcp.md | excluded | chapters/06-reverse-engineering.md | Agent/MCP integration, AI workflows and unapproved tools excluded under event rules. Structural/section review only; generic local debugging/decompilation concepts rewritten using approved tools elsewhere. Original retained as provenance. |
| ctf-reverse/tools.md | adapted | chapters/06-reverse-engineering.md | Adapted approved platform-specific static/debug routes, triage and language/tool selection across sections 1-7 and 12. IDA/Binary Ninja/online comparison instructions excluded. |
| ctf-reverse/unicorn-emulation.md | merged | chapters/06-reverse-engineering.md | Merged CPU versus OS modeling, MMIO, mode/endianness, snapshots, dirty-memory reset, budgets and fault diagnosis into section 10. Detailed hardware harnesses remain reference-only; no emulator availability or successful execution claimed. |
| ctf-similar-search/search.py | excluded | chapters/12-excluded-and-advanced.md | Excluded API client transmits queries/URLs and requests include_answer; code reviewed as provenance, not executed. |
| ctf-similar-search/search.sh | excluded | chapters/12-excluded-and-advanced.md | Excluded shell launcher for Tavily Python client; no runnable online search wrapper retained. |
| ctf-similar-search/SKILL.md | excluded | chapters/12-excluded-and-advanced.md | Excluded agent/Tavily search and AI-answer workflow; replaced with offline approved reference search. |
| ctf-web/auth-and-access-2.md | merged | chapters/02-web-exploitation.md | Normalization, delimiter/collection validation, SRP arithmetic, and query-merge cases folded into source-driven auth checks; collision flooding not a default workflow. |
| ctf-web/auth-and-access.md | merged | chapters/02-web-exploitation.md | Ownership, cookies, normalization, access control, OTP hypotheses, stale WebSocket/SSE auth; AI/chatbot subsections excluded; external account takeover not carried forward. |
| ctf-web/auth-infra.md | merged | chapters/02-web-exploitation.md | OAuth/SAML/CORS, local Git history, signature parsing and length-extension distinctions retained; external credential harvesting and unrelated CI takeover omitted. |
| ctf-web/auth-jwt.md | merged | chapters/02-web-exploitation.md | JWT/JWE segmentation, claim verification, key-source trust, replay, encryption-versus-authentication, and complete broken-verifier toy; no rejected JWT Editor extension. |
| ctf-web/client-side-advanced.md | merged | chapters/02-web-exploitation.md | Origin/opener/null-origin, MIME/base/nonce, CSS information leakage, Unicode normalization, React state and timing prerequisites merged; public-cloud exfiltration excluded. |
| ctf-web/client-side.md | merged | chapters/02-web-exploitation.md | Reflection context, DOM sources/sinks, path construction, CSP, bot reproduction, cache and timing controls; public callback/tunnel workflows excluded. |
| ctf-web/cves.md | reference-only | chapters/02-web-exploitation.md | Version-specific CVE material retained as evidence-led recognition and offline-advisory workflow; historical CVE labels/payloads are not asserted universally current. |
| ctf-web/field-notes.md | merged | chapters/02-web-exploitation.md | Duplicate quick references merged into injection/auth/browser/chain chapters; AI and public callback portions excluded. |
| ctf-web/node-and-prototype.md | merged | chapters/02-web-exploitation.md | Pollution requires controllable merge plus gadget; tested-style local JSON/prototype distinction and version-specific VM caveats. |
| ctf-web/pat-reference.md | adapted | chapters/02-web-exploitation.md | Approved Kali offline PayloadsAllTheThings searches replace lazy cloning and indiscriminate payload loading; exact listed path included. |
| ctf-web/python-requests.md | adapted | chapters/02-web-exploitation.md | Sessions, CSRF, redirects, framing, encoding, timeouts and controls translated into manual Repeater and single-request standard-library workflow; high concurrency and external callbacks removed. |
| ctf-web/scripts/async_fuzz.py | reference-only | chapters/02-web-exploitation.md | Reference-only: concurrency, disabled TLS verification, response heuristics and processing/regex correctness concerns; replaced with bounded evidence-backed ffuf/Repeater. |
| ctf-web/server-side-2.md | merged | chapters/02-web-exploitation.md | XXE, XML, command/argument injection and GraphQL manual requests; entity expansion differentiated from external access. |
| ctf-web/server-side-advanced-2.md | merged | chapters/02-web-exploitation.md | Internal fetch/protocol capability boundaries, parser discrepancies, source context, query shifts and renderer execution merged; only assigned challenge services. |
| ctf-web/server-side-advanced-3.md | merged | chapters/02-web-exploitation.md | Polyglots, repeated slashes, RNG hints, SOAP/header parsing and outbound URL credential boundaries merged into fetch/serialization diagnostics. |
| ctf-web/server-side-advanced-4.md | merged | chapters/02-web-exploitation.md | Renderer attachments, NoSQL/Go templates, archives, protocol and RSC version recognition merged; unapproved interception/repository utilities not assumed available. |
| ctf-web/server-side-advanced.md | merged | chapters/02-web-exploitation.md | Archive symlinks, path normalization, renderers/debug/version prerequisites retained; ZIP inspection before extraction. |
| ctf-web/server-side-deser.md | merged | chapters/02-web-exploitation.md | Safe pickle disassembly, object hooks, STOP handling, serialized length and race conditions; generic unapproved gadget-tool invocation not reproduced. |
| ctf-web/server-side-exec-2.md | merged | chapters/02-web-exploitation.md | SQL/context filters, execution/serialization, metadata/options and historical runtime behavior merged; obsolete language features explicitly require matching versions. |
| ctf-web/server-side-exec.md | merged | chapters/02-web-exploitation.md | Language-specific evaluators, uploads, argument boundaries, variable overwrite, XPath and format fields; use minimal same-challenge recovery. |
| ctf-web/server-side.md | merged | chapters/02-web-exploitation.md | SQL, PHP wrappers/types, SSTI, format traversal, SSRF and parser disagreements; confirmed challenge file recovery shown. |
| ctf-web/SKILL.md | adapted | chapters/02-web-exploitation.md | Human first-pass request workflow; agent invocation, AI assistance, public callbacks, blanket installation, and brute-force defaults removed. |
| ctf-web/sql-injection.md | merged | chapters/02-web-exploitation.md | Context-first boolean/UNION/blind/second-order/metadata/format/charset checks, bounded sqlmap discovery and one-column recovery; DBMS-specific legacy tricks contextualized. |
| ctf-web/tools-mcp.md | excluded | chapters/12-excluded-and-advanced.md | Excluded AI/agent MCP execution, approval bypass guidance, Professional assumptions and public callbacks; replaced by manual Chrome/Burp Community. |
| ctf-web/web3.md | reference-only | chapters/02-web-exploitation.md | Static source/ABI/storage/authorization diagnostics for delegatecall, reentrancy, calldata, replay and compiler-specific storage; no unlisted or online Solidity toolchain assumed. |
| ctf-writeup/SKILL.md | adapted | chapters/01-first-ten-minutes.md | Human triage, hypothesis logging, team handoff and writeup; AI routing and agent commands removed. |
| evals/cases/routing.yaml | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/cases/rules.yaml | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/cases/solve.yaml | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/fixtures/crypto-broadcast/chall.py | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/fixtures/crypto-broadcast/output.txt | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/fixtures/misc-layers/intercepted.txt | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/fixtures/reverse-vm/checker.py | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/fixtures/rules/decoy-flag/artifact.b64 | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/fixtures/rules/decoy-flag/build.log | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/fixtures/rules/decoy-flag/README.txt | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/fixtures/rules/forensics-no-macro-negative/data.csv | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/fixtures/rules/forensics-no-macro-negative/macro.vba | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/fixtures/rules/forensics-no-macro-negative/README.txt | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/fixtures/rules/forensics-no-macro-positive/data.csv | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/fixtures/rules/forensics-no-macro-positive/macro.vba | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/fixtures/rules/forensics-no-macro-positive/README.txt | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/fixtures/rules/no-decoy/artifact.b64 | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/fixtures/rules/no-decoy/README.txt | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/fixtures/rules/pwn-checksec-order-negative/chall | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/fixtures/rules/pwn-checksec-order-negative/README.txt | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/fixtures/rules/pwn-checksec-order-positive/chall | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/fixtures/rules/pwn-checksec-order-positive/README.txt | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/fixtures/rules/reverse-head-truncation-negative/chall | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/fixtures/rules/reverse-head-truncation-negative/README.txt | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/fixtures/rules/reverse-head-truncation-positive/chall | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/fixtures/rules/reverse-head-truncation-positive/README.txt | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/fixtures/rules/web-read-js-negative/app.js | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/fixtures/rules/web-read-js-negative/index.html | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/fixtures/rules/web-read-js-negative/README.txt | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/fixtures/rules/web-read-js-positive/app.js | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/fixtures/rules/web-read-js-positive/index.html | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/fixtures/rules/web-read-js-positive/README.txt | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/fixtures-src/rules/pwn-checksec-order/NOTES.md | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/fixtures-src/rules/pwn-checksec-order/vuln.c | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/fixtures-src/rules/reverse-head-truncation/chall.c | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/fixtures-src/rules/reverse-head-truncation/gen.py | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/fixtures-src/rules/reverse-head-truncation/NOTES.md | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/lib/assertions.js | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/lib/hooks.js | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/lib/summary.js | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/package-lock.json | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/package.json | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/promptfooconfig.routing.yaml | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/promptfooconfig.rules.yaml | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/promptfooconfig.solve.yaml | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| evals/README.md | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| LICENSE | retained | LICENSE | Original MIT copyright and permission notice retained in the deliverable. |
| pyproject.toml | reference-only | chapters/01-first-ten-minutes.md | Repository governance, configuration or contribution material; retained in original tree, not a challenge-solving recipe. |
| README.md | adapted | chapters/00-start-here.md | Category overview and navigation converted to human reading routes; agent setup excluded. |
| scripts/generate_catalog.py | replaced | chapters/01-first-ten-minutes.md | Original catalog is an agent index with remote analytics. New site embeds complete human guides with no external runtime assets. |
| scripts/install_ctf_tools.sh | excluded | chapters/00-tool-rules.md | Broad unrestricted installer conflicts with event whitelist. Use existing listed installations. |
| scripts/skill_security_auditor.py | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| scripts/verify_crypto_examples.py | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| SECURITY.md | reference-only | chapters/01-first-ten-minutes.md | Repository governance, configuration or contribution material; retained in original tree, not a challenge-solving recipe. |
| solve-challenge/difficulty-routing.md | adapted | chapters/01-first-ten-minutes.md | Human triage, hypothesis logging, team handoff and writeup; AI routing and agent commands removed. |
| solve-challenge/SKILL.md | adapted | chapters/01-first-ten-minutes.md | Human triage, hypothesis logging, team handoff and writeup; AI routing and agent commands removed. |
| tests/test_cross_references.py | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| tests/test_crypto_snippets.py | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| tests/test_eval_coverage.py | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| tests/test_misc_snippets.py | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| tests/test_pwn_scripts.py | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| tests/test_reverse_r2_snippets.py | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| tests/test_skill_discoverability.py | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| tests/test_skill_frontmatter.py | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| tests/test_skill_security_auditor.py | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |
| tests/test_web_requests_snippets.py | reference-only | chapters/01-first-ten-minutes.md | Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow. |


---

## Attribution and license

Adapted from the supplied ctf-skills repository. Original copyright (c) 2026 Lukasz Jagiello.

```text
MIT License

Copyright (c) 2026 Lukasz Jagiello

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```
