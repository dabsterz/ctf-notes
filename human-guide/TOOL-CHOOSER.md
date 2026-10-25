# Choose a tool by the job

Start with the **first choice** for your category. The tables compare useful approved options; the [complete matrix](TOOL-MATRIX.md) retains all 282 workbook entries, including exclusions. A program appearing on Kali's website does not establish event approval: the environment below comes from your workbook.

**Location key:** Windows = native Windows; WSL = Linux inside Windows; Kali = the separate supplied Kali machine. **W29** means `Approved Tool List for Windows!C29`; **K123** means `Approved Tool List for Kali!C123`. Blank installation notes still require a local availability check. Tool names link to documentation where useful; these links are optional and are not needed to read this guide offline.

Examples use files in the current directory. Replace `challenge.example`, filenames and uppercase placeholders with the challenge's values. `words.txt` is a small list you prepared from the clues. GUI rows give an actual click path. Bash commands belong in the row's Linux environment.

## Web

**First choice:** inspect one request with Burp Repeater or curl. For hidden paths, choose ffuf for flexible filtering or Gobuster for a straightforward directory scan.

| Tool / event environment | Strong at | Weakness / when to switch | First action |
| --- | --- | --- | --- |
| [Burp Community](https://portswigger.net/burp/documentation/desktop/tools/repeater) · WSL · W27 | Editing one captured request and comparing responses | Community is a manual workflow; do not assume Pro scanning or unapproved extensions | HTTP history → right-click request → Send to Repeater → edit one field → Send |
| [curl](https://curl.se/docs/manpage.html) · Kali · K30 | Reproducible HTTP requests, headers and cookies | Does not execute browser JavaScript; use Chrome for client behavior | `curl -i 'http://challenge.example/'` |
| [ffuf](https://github.com/ffuf/ffuf) · Kali · K48 | Fuzzing paths, parameters, headers and bodies; filtering responses | Needs a meaningful wordlist and baseline; automatic filters can hide hits | `ffuf -u 'http://challenge.example/FUZZ' -w words.txt -ac -rate 20 -maxtime 60` |
| [Gobuster](https://github.com/OJ/gobuster) · Kali · K61 | Directory/file, DNS and virtual-host discovery | Wildcard responses produce false hits; less convenient for complex request mutations | `gobuster dir -u 'http://challenge.example/' -w words.txt -t 5` |
| [Feroxbuster](https://www.kali.org/tools/feroxbuster/) · Kali · K46 | Recursively finding content beneath discovered directories | Recursion expands the scan quickly; cap depth and request rate | `feroxbuster -u 'http://challenge.example/' -w words.txt --depth 1 --rate-limit 10` |
| [sqlmap](https://www.kali.org/tools/sqlmap/) · Kali · K139 | Testing a suspected SQL injection with the original request | Does not solve access-control or business-logic bugs; stale cookies/CSRF tokens break tests | Save request as `request.txt`; `sqlmap -r request.txt -p id --batch --level=1 --risk=1` (replace `id`) |
| Google Chrome · Windows · W12 | Browser-only behavior, storage and JavaScript requests | DevTools showing a value is not proof the server trusts it | F12 → Network → reload → select request → Headers / Response |

**These are different jobs:** ffuf/Gobuster discover or vary web inputs. They are not offline password-hash crackers. ffuf can send login guesses, but correctly detecting login success, tokens and rate limits needs a separate workflow. Use the next table to choose deliberately.

## Passwords and hashes

**First choice:** John for an offline hash/file format you can identify; hashcat when the mode and a working compute backend are known. Hydra is for attempts against a live login service, not a hash file.

| Tool / event environment | Strong at | Weakness / when to switch | First action |
| --- | --- | --- | --- |
| [John the Ripper jumbo](https://www.openwall.com/john/doc/EXAMPLES.shtml) · Kali · K80 | Many hash formats, rules and archive-to-hash workflows | Format detection can be ambiguous; guessing the wrong format wastes time | For known raw MD5: `john --format=raw-md5 --wordlist=words.txt hashes.txt`; then `john --show --format=raw-md5 hashes.txt` |
| [hashcat](https://hashcat.net/wiki/doku.php?id=example_hashes) · Kali · K66 | Fast offline candidate testing with suitable hardware; masks and rules | Requires the right hash mode and usable backend; Supplied t3.large Kali has 2 vCPU and no GPU; verify backend support | `hashcat -I`; for raw MD5: `hashcat -m 0 -a 0 hashes.txt words.txt`; then `hashcat -m 0 hashes.txt --show` |
| [Hydra](https://github.com/vanhauser-thc/thc-hydra) · Kali · K72 | Online username/password testing across supported protocols | Network latency, lockouts, CSRF and misleading success markers; cannot crack offline hashes | For a challenge-authorized SSH login: `hydra -l USER -P words.txt -t 1 -f ssh://challenge.example` |
| [hashid](https://www.kali.org/tools/hashid/) · Kali · K67 | Suggesting formats from hash shape | A 32-hex-character value could be MD5, NTLM or another format; shape is not identification | `hashid hashes.txt`; confirm from source or hash prefix before choosing a cracker |
| John jumbo archive extractors · Kali · K80 | Converting protected archives into crackable records | Extraction is format-specific; not every encryption variant is supported | `zip2john locked.zip > zip.hash`; then `john --wordlist=words.txt zip.hash`; inspect with `john --show zip.hash` |
| [bkcrack](https://github.com/kimci86/bkcrack) · Kali · K20 | Known-plaintext attacks on legacy ZipCrypto | Not a general ZIP AES cracker; requires suitable known plaintext bytes | `bkcrack -L locked.zip` to inspect encryption/members, then follow the [archive chapter](chapters/03-forensics.md) |
| rockyou.txt / SecLists · Kali · K127, K133 | Candidate passwords / task-specific discovery lists | Lists are data, not cracking tools; a huge wrong list is slower than a small relevant one | `ls /usr/share/wordlists/rockyou.txt`; `find /usr/share /usr/bin/seclists -iname '*common*.txt' 2>/dev/null` |

After recovering a password, verify it with the challenge file or login. A “no hashes loaded” error means parsing/format needs attention; an exhausted list means those candidates did not match. Neither proves that the password is uncrackable.

## Forensics

**First choice:** choose the artifact: disk → Sleuth Kit/Autopsy; memory → Volatility; Windows logs → named fields and timeline.

| Tool / event environment | Strong at | Weakness / when to switch | First action |
| --- | --- | --- | --- |
| [The Sleuth Kit](https://www.sleuthkit.org/sleuthkit/man/fls.html) · WSL · W30 | File systems, deleted entries and extraction without mounting | Needs the correct partition offset; carving is a separate task | `mmls disk.img`; then `fls -r -o START_SECTOR disk.img` using the reported start sector |
| [Autopsy](https://sleuthkit.org/autopsy/docs/user-docs/4.22.0/) · Windows · W41 | Browsing a disk image and correlating many artifacts in a GUI | Ingest/indexing can take time; a single known file may be faster with Sleuth Kit | New Case → Add Data Source → Disk Image → choose relevant ingest modules |
| [Volatility 3](https://volatility3.readthedocs.io/en/latest/getting-started-windows-tutorial.html) · WSL · W38 | Processes, command lines and other structures in memory dumps | Requires matching symbols/layers; cannot create missing memory evidence | If installed entry point is `vol`: `vol -f memory.raw windows.info`; then `vol -f memory.raw windows.pslist` |
| [Eric Zimmerman's Tools](https://github.com/EricZimmerman/evtx) · Windows · W46 | Windows artifact parsers producing useful CSV timelines | Suite contains many executables; field meaning and timezone still need interpretation | From its installed folder: `.\EvtxECmd.exe -f .\Security.evtx --csv .\out` |
| [7-Zip](https://www.kali.org/tools/7zip/) · Kali · K9 | Listing/testing many archive formats before extraction | Ordinary extraction can overwrite duplicate names; encrypted content needs a password | `7z l evidence.zip`; `7z t evidence.zip` |
| [sqlite3](https://sqlite.org/cli.html) · Kali · K138 | Fast inspection of browser/app databases | Deleted rows and WAL recovery require more than a normal query | `sqlite3 -readonly evidence.db '.tables'`; then `sqlite3 -readonly evidence.db '.schema'` |
| [ExifTool](https://www.kali.org/tools/libimage-exiftool-perl/) · WSL · W21 | Metadata across images, media and documents | Metadata can be absent, altered or misleading | `exiftool -a -G1 -s evidence.jpg` |

Do not confuse Volatility 3 in WSL with the Kali Volatility 2 rows. A parser's output is evidence to interpret, not an automatic conclusion. [Process-event quick card](QUICKSTART.md#process-event).

## Network

**First choice:** Wireshark for understanding one conversation; TShark/Zeek for repeatable summaries. Nmap is active service discovery, not analysis of a PCAP.

| Tool / event environment | Strong at | Weakness / when to switch | First action |
| --- | --- | --- | --- |
| [Wireshark](https://www.wireshark.org/docs/wsug_html_chunked/ChAdvFollowStreamSection.html) · Windows · W9 | Interactive packet dissection, streams and object export | TLS application data stays encrypted without suitable secrets | [Conversation/filter/stream click path](QUICKSTART.md#network-conversation) |
| [TShark](https://www.wireshark.org/docs/man-pages/tshark.html) · Windows · W43 | Terminal filters, field export and repeatable summaries | Display/capture filters have different syntax; Windows executable path may need quoting | PowerShell: `& 'C:\Program Files\Wireshark\tshark.exe' -r .\capture.pcapng -q -z conv,tcp` |
| [Zeek](https://docs.zeek.org/en/current/quickstart.html) · WSL · W25 | Turning a capture into connection, DNS and HTTP logs | Summaries omit some packet-level detail; encrypted content is still hidden | In a fresh output folder: `zeek -r ../capture.pcapng`; inspect `conn.log` |
| [tcpdump](https://www.tcpdump.org/manpages/tcpdump.1.html) · Kali · K149 | Small terminal packet views with capture-filter syntax | Limited application reconstruction compared with Wireshark | `tcpdump -nn -r capture.pcapng -c 30` |
| [Nmap](https://nmap.org/book/man.html) · Kali · K101 | Identifying open ports and service versions on designated targets | Service banners are hints; scans do not establish exploitability | `nmap -sT -sV -p 80,443,8080 challenge.example` |
| can-utils · WSL · W23 | Reading CAN bus frames and supplied automotive traces | Requires CAN-specific interpretation; it is not an Ethernet decoder | For a prepared challenge CAN interface: `candump -L can0`; for a supplied text log, inspect it without transmitting |

## Steganography and audio

**First choice:** metadata and file structure before password guessing. PNG/BMP bit planes → zsteg; suspected steghide carrier → steghide/stegseek; sound/image-like tones → spectrogram.

| Tool / event environment | Strong at | Weakness / when to switch | First action |
| --- | --- | --- | --- |
| [zsteg](https://github.com/zed-0xff/zsteg) · WSL · W19 | Common PNG/BMP bit-plane patterns | Random channels produce plausible text; does not analyze JPEG compression stego | `zsteg -a carrier.png`; validate a promising extraction before accepting it |
| [binwalk](https://www.kali.org/tools/binwalk/) · WSL · W20 | Finding embedded signatures/offsets | Signatures can be false positives; extraction helpers vary by version | `binwalk carrier.bin`; inspect a candidate offset before extracting |
| [pngcheck](https://www.kali.org/tools/pngcheck/) · Kali · K115 | PNG structure, CRC and chunk errors | Does not reveal arbitrary hidden pixel payloads | `pngcheck -v carrier.png` |
| [steghide](https://www.kali.org/tools/steghide/) · Kali · K141 | Extracting its own JPEG/BMP/WAV/AU carriers with a passphrase | Not a general PNG/LSB tool; wrong carrier family will not work | `steghide info carrier.jpg`; `steghide extract -sf carrier.jpg` (enter supplied passphrase) |
| [stegseek](https://github.com/RickdeJager/stegseek) · Kali · K142 | Fast steghide password guessing with a wordlist | Does not crack every steganography method; list must contain a useful candidate | `stegseek carrier.jpg words.txt recovered.bin` |
| [Audacity](https://manual.audacityteam.org/man/spectrogram_view.html) · Kali · K17 | Listening, channel inspection and spectrograms | A spectrogram is a visual clue, not an automatic modem decoder | Open audio → track menu → Spectrogram; zoom the suspicious time range |
| [FFmpeg](https://ffmpeg.org/ffmpeg.html) · Kali · K47 | Converting media and selecting audio/video streams | Lossy conversion can destroy evidence; preserve the original | `ffmpeg -i input.wav -c:a pcm_s16le working.wav` |
| ZBar · WSL · W26 | Local barcode/QR decoding | Damaged or stylized codes may need image repair | `zbarimg --raw code.png` |

No trailer found? Try metadata or a relevant bit-plane technique, not every stego tool. [PNG trailer card](QUICKSTART.md#png-trailer).

## Reverse engineering

**First choice:** Ghidra for readable native-code structure; radare2 for terminal inspection; choose a format-specific decompiler for .NET or Android.

| Tool / event environment | Strong at | Weakness / when to switch | First action |
| --- | --- | --- | --- |
| [Ghidra](https://ghidra.re/ghidra_docs/GhidraClass/Beginner/Introduction_to_Ghidra_Student_Guide.html) · WSL · W29 | Native decompilation, cross-references and data flow | Decompiler output can misrepresent types; verify critical operations in disassembly | Import → Analyze → Search for Strings → references to success/failure text |
| [radare2](https://book.rada.re/refcard/intro.html) · Kali · K123 | Terminal disassembly, strings and scripting | Dense command language; automatic function discovery can be wrong | `r2 -A challenge.bin`; inside: `iz`, `afl`, `pdf @ main` |
| objdump · WSL · W17 | Quick headers and disassembly without a project | No high-level decompiler; architecture/flavor flags matter | `objdump -f challenge.bin`; for x86: `objdump -d -M intel challenge.bin` |
| strings · WSL · W18 | Quick hints: error strings, URLs and paths | Misses decoded/encrypted runtime strings; strings are not proof of behavior | `strings -a -n 6 challenge.bin` |
| [GDB](https://sourceware.org/gdb/current/onlinedocs/gdb/) · WSL · W16 | Register/memory inspection and breakpoints on compatible targets | Running a target changes state; wrong architecture/OS may not run | `gdb -nx ./challenge`; inside: `break main`, `run`, `info registers` |
| x64dbg · Windows · W40 | Debugging native Windows executables with a GUI | Not a .NET source decompiler; executing malware needs an isolated lab | File → Open → challenge EXE → set a breakpoint at the identified comparison → Run |
| [dnSpyEx](https://github.com/dnSpyEx/dnSpy) · Windows · W45 | Browsing/decompiling .NET assemblies | Obfuscation/native components need other techniques | File → Open assembly → expand types → find entry point and comparison method |
| [jadx](https://www.kali.org/tools/jadx/) · Kali · K79 | Android DEX/APK decompilation and searching usages | Recovered Java may be incomplete; native `.so` logic needs native reversing | `jadx-gui challenge.apk`; search the success string and its usages |

Already extracted the checker constants? Use the [complete XOR/rotation card](QUICKSTART.md#xor-and-rotation) or [small-VM card](QUICKSTART.md#small-vm).

## Cryptography

**First choice:** identify the math/format from source. Encoding, password hashes and public-key encryption are different problems.

| Tool / event environment | Strong at | Weakness / when to switch | First action |
| --- | --- | --- | --- |
| Python 3 standard library · WSL · W14 | Exact integers, modular arithmetic and custom transformations | Does not automatically identify attacks or factor a strong RSA modulus | `python3 recipes/rsa.py rsa.json` for the [documented raw-RSA case](QUICKSTART.md#rsa) |
| [OpenSSL](https://docs.openssl.org/3.0/man1/openssl-pkey/) · WSL · W31 | Inspecting standard keys/certificates and known cipher formats | Wrong mode/padding/KDF produces nonsense; it is not a generic crypto solver | `openssl pkey -pubin -in public.pem -text -noout` |
| [RsaCtfTool](https://github.com/RsaCtfTool/RsaCtfTool) · WSL · W37 | Trying known weak-RSA structures against supplied keys | Fermat needs close primes; remote-backed attacks can violate event restrictions | `RsaCtfTool --publickey public.pem --attack fermat --private`; if unavailable, use the [bounded Python recipe](QUICKSTART.md#rsa) with n/e/c |
| [SageMath](https://doc.sagemath.org/html/en/tutorial/) · Kali · K132 | Algebra, finite fields, polynomial and lattice calculations | Startup/dependencies and mathematical modeling can dominate solve time | `sage -c 'print(factor(3233))'` is a small availability check, not proof large moduli are factorable |
| [PARI/GP](https://pari.math.u-bordeaux.fr/gp.html) · Kali · K109 | Number theory and exact arithmetic at a prompt | GP syntax differs from Python/Sage; does not choose the cryptographic weakness | Run `gp`; enter `factor(3233)` |
| CyberChef · Windows browser bookmark · W8 | Seeing byte encodings and chaining simple transforms visually | Bookmark does not establish offline availability; optional operations/services may send data | In the organizer-approved local/client-side instance: From Base64 → inspect output; use the [local decoder](QUICKSTART.md#decode-layers) if availability/data handling is unclear |

For advanced crypto, start with the [advanced chapter](chapters/14-advanced-crypto.md) only after identifying the required mathematical relation. The approved `crypto-attacks` checkout (K29) is reference code requiring assumptions/dependencies, not a universal `solve` command. No FactorDB upload is implied by local package approval.

## Binary exploitation

**First choice:** establish the bug and mitigations, then use a debugger. A gadget list or mitigation report is not an exploit.

| Tool / event environment | Strong at | Weakness / when to switch | First action |
| --- | --- | --- | --- |
| [checksec](https://github.com/slimm609/checksec) · Kali · K28 | Summarizing ELF mitigations | Syntax differs across releases; flags describe defenses, not a vulnerability | Try `checksec --file=challenge`; if help shows subcommands, use `checksec file ./challenge` |
| GDB · WSL · W16 | Inspecting the crash and verifying overwrite effects | Local addresses differ with ASLR/PIE; debugger state can differ from remote | `gdb -nx ./challenge`; inside: `run < pattern.bin`, then `info registers` |
| pwndbg / GEF · Kali · K116, K55 | Rich debugger context, heap views and exploitation helpers | Plugin compatibility varies; don't load competing extensions together | **GEF route:** in an existing Kali GDB, `source /opt/tools/gef.py`. **pwndbg:** use its already configured debugger; otherwise use WSL plain GDB |
| [ROPgadget](https://github.com/JonathanSalwan/ROPgadget) · Kali · K128 | Finding instruction sequences in a binary/library | A listed gadget may have side effects or a relocated address | `ROPgadget --binary challenge --only 'pop\|ret'` |
| Ncat (Nmap suite) · Kali · K101 | Manually interacting with a challenge TCP service | Text terminals can alter binary input; protocol framing still matters | `ncat challenge.example 31337` |
| [strace](https://strace.io/) · Kali · K145 | Seeing Linux syscalls, file opens and denied operations | Does not show every internal function or Windows API call; executes the target | `strace -f -o trace.txt ./challenge` |

The [crash-offset card](QUICKSTART.md#crash-offset) provides an exact pattern generator. Historical pwn examples remain in the practice atlas; allocator/version assumptions must match your target.

## Malware

**First choice:** static strings, file structure and scripts. Only execute samples in the supplied isolated analysis environment when the task calls for it.

| Tool / event environment | Strong at | Weakness / when to switch | First action |
| --- | --- | --- | --- |
| [FLOSS](https://github.com/mandiant/flare-floss) · Kali · K50 | Recovering some obfuscated/stack strings from executables | Heuristics miss unsupported code; recovered strings do not prove execution | `floss suspect.exe` |
| [capa](https://github.com/mandiant/capa) · Kali · K26 | Suggesting capabilities from static patterns | Rule matches need supporting code; packing can hide behavior | `capa suspect.exe` |
| [oletools](https://www.kali.org/tools/oletools/) · Kali · K105 | Inspecting Office macros and embedded objects | Not every document exploit is a macro; never enable macros just to inspect them | `oleid suspect.docm`; `olevba suspect.docm` |
| [YARA](https://www.kali.org/tools/yara/) · Kali · K164 | Finding files matching supplied/custom byte rules | Match quality depends on rules; no match does not mean benign | `yara -r rules.yar samples/` |
| [UPX](https://upx.github.io/) · Kali · K156 | Recognizing/unpacking supported UPX-packed executables | Modified packers may fail; not a universal unpacker | `upx -t suspect.exe`; if confirmed, unpack a copy: `upx -d -o unpacked.exe suspect.exe` |
| Ghidra / x64dbg · WSL W29 / Windows W40 | Following decoded logic / observing runtime behavior | Static analysis can miss runtime state; debugging executes the sample | Use the [reverse table](#reverse-engineering) for the matching native format |

## OSINT

**First choice:** extract clues from the supplied material, then corroborate. Public analysis upload services remain excluded; a browser is not blanket permission for every service.

| Tool / event environment | Strong at | Weakness / when to switch | First action |
| --- | --- | --- | --- |
| ExifTool · WSL · W21 | Metadata/GPS/timezone clues in supplied media | Values can be edited or stripped; corroborate independently | `exiftool -a -G1 -s clue.jpg` |
| Google Chrome · Windows · W12 | Reading permitted public sources and comparing visible details | Search results are leads, not evidence; do not upload challenge files | Search a distinctive quoted phrase; open the original page and record URL/date |
| [ripgrep](https://github.com/BurntSushi/ripgrep) · Kali · K126 | Searching supplied websites, exports and source folders locally | Binary or compressed content must be decoded first | `rg -n -i 'distinctive phrase' supplied/` |
| pdftotext · WSL · W22 | Extracting searchable text from a supplied PDF | Scanned images may contain no text layer | `pdftotext -layout clue.pdf clue.txt`; inspect `clue.txt` |
| [Git](https://git-scm.com/docs/git-log) · Kali · K56 | Investigating history in a supplied repository | A shallow/exported copy may lack history; don't contact unrelated remotes | `git -C supplied log --all --oneline`; `git -C supplied show COMMIT` |

## Miscellaneous

**First choice:** identify the representation before choosing a tool. Reuse the steganography/audio and password tables when those fit the clue.

| Tool / event environment | Strong at | Weakness / when to switch | First action |
| --- | --- | --- | --- |
| Python 3 · WSL · W14 | Small parsers, encodings, arithmetic and exact byte transformations | Requires correct input assumptions; generic brute force grows quickly | For Base64/compression: `python3 recipes/layers.py message.txt --out decoded` |
| [jq](https://jqlang.org/manual/) · WSL · W28 | Inspecting/filtering JSON without writing a parser | JSON only; malformed text or binary formats need another route | `jq . challenge.json`; once fields are known: `jq '.key' challenge.json` |
| xxd · WSL · W35 | Inspecting byte offsets and converting plain hex | Hex views do not identify the hidden format by themselves | `xxd -l 128 challenge.bin`; for plain hex: `xxd -r -p hex.txt > decoded.bin` |
| HxD · Windows · W42 | Visual byte/offset inspection and careful edits to a copy | Easy to corrupt offsets with edits; no semantic decoder | File → Open → Search → Find (hex-values tab); keep the original unchanged |
| [file](https://www.darwinsys.com/file/) · Kali · K49 | Initial type/magic identification | Extensions/magic can be forged; embedded files need further inspection | `file challenge.bin` |
| [7-Zip](https://www.kali.org/tools/7zip/) · Kali · K9 | Recognizing/listing unfamiliar containers | A listed member may be encrypted; duplicate names need preservation | `7z l challenge.bin`; for tar duplicates use [the preserving extractor](QUICKSTART.md#duplicate-tar-files) |

AI/ML tools and agent workflows are excluded by the event rules, so there is no recommended AI-tool table. [Exclusions and alternatives](chapters/12-excluded-and-advanced.md).

## If a tool fails to start

Check the environment first, then its recorded path in the [full matrix](TOOL-MATRIX.md). A missing `r2` in WSL is expected from this list: use Kali or WSL Ghidra. A missing GPU backend makes hashcat a poor first choice; try the supported John format. Use [targeted non-AI package setup](chapters/00-tool-rules.md#non-ai-python-package-checks) only when needed. Unlisted standalone apps require approval; [machine limits](COMPETITION.md#choose-the-machine-before-the-tool) favor short candidate lists and one heavy Kali job at a time.
